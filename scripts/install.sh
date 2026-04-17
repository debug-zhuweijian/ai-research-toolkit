#!/usr/bin/env bash
# install.sh — Install skills and agents from selected modules/profile.

set -euo pipefail
shopt -s nullglob

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
MODULES_ROOT="$REPO_ROOT/modules"

SKILLS_DIR="${HOME}/.claude/skills"
AGENTS_DIR="${HOME}/.claude/agents"
FORCE=false
LIST_ONLY=false
PROFILE=""
REQUESTED_MODULES=()

usage() {
  cat <<'EOF'
Usage:
  ./scripts/install.sh [--profile <minimal|knowledge|full>]
  ./scripts/install.sh [--module <module-id> ...]
  ./scripts/install.sh --list

Options:
  --profile <name>     Install modules from a profile preset.
  --module <module-id> Install one module. Can be repeated.
  --skills-path <dir>  Override destination skills directory.
  --agents-path <dir>  Override destination agents directory.
  --force              Overwrite existing installed skills/agents.
  --list               Show available profiles and installable modules.
  -h, --help           Show this help message.

Notes:
  - --profile and --module are mutually exclusive.
  - If neither is provided, the default is --profile full.
EOF
}

profile_modules() {
  case "$1" in
    minimal) echo "01-discovery 02-processing" ;;
    knowledge) echo "05-knowledge 06-presentation" ;;
    full) echo "01-discovery 02-processing 03-analysis 04-writing 05-knowledge 06-presentation" ;;
    *)
      echo "Unknown profile: $1" >&2
      return 1
      ;;
  esac
}

list_installable_modules() {
  local module_dir module_name skill_count agent_count

  echo "Profiles:"
  echo "  minimal   -> 01-discovery, 02-processing"
  echo "  knowledge -> 05-knowledge, 06-presentation"
  echo "  full      -> 01-discovery, 02-processing, 03-analysis, 04-writing, 05-knowledge, 06-presentation"
  echo
  echo "Modules:"

  for module_dir in "$MODULES_ROOT"/*; do
    [[ -d "$module_dir" ]] || continue
    module_name="$(basename "$module_dir")"
    skill_count=0
    agent_count=0

    if [[ -d "$module_dir/skills" ]]; then
      for path in "$module_dir"/skills/*; do
        [[ -d "$path" ]] && ((skill_count+=1))
      done
    fi
    if [[ -d "$module_dir/agents" ]]; then
      for path in "$module_dir"/agents/*.md; do
        [[ -f "$path" ]] && ((agent_count+=1))
      done
    fi

    echo "  $module_name (skills: $skill_count, agents: $agent_count)"
  done
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile)
      [[ $# -ge 2 ]] || { echo "Missing value for --profile" >&2; exit 1; }
      PROFILE="$2"
      shift 2
      ;;
    --module)
      [[ $# -ge 2 ]] || { echo "Missing value for --module" >&2; exit 1; }
      REQUESTED_MODULES+=("$2")
      shift 2
      ;;
    --skills-path)
      [[ $# -ge 2 ]] || { echo "Missing value for --skills-path" >&2; exit 1; }
      SKILLS_DIR="$2"
      shift 2
      ;;
    --agents-path)
      [[ $# -ge 2 ]] || { echo "Missing value for --agents-path" >&2; exit 1; }
      AGENTS_DIR="$2"
      shift 2
      ;;
    --force)
      FORCE=true
      shift
      ;;
    --list)
      LIST_ONLY=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if $LIST_ONLY; then
  list_installable_modules
  exit 0
fi

if [[ -n "$PROFILE" && ${#REQUESTED_MODULES[@]} -gt 0 ]]; then
  echo "Error: --profile and --module cannot be used together." >&2
  exit 1
fi

if [[ -z "$PROFILE" && ${#REQUESTED_MODULES[@]} -eq 0 ]]; then
  PROFILE="full"
fi

if [[ -n "$PROFILE" ]]; then
  read -r -a REQUESTED_MODULES <<<"$(profile_modules "$PROFILE")"
fi

declare -A seen_modules=()
ORDERED_MODULES=()
for module_name in "${REQUESTED_MODULES[@]}"; do
  module_dir="$MODULES_ROOT/$module_name"
  if [[ ! -d "$module_dir" ]]; then
    echo "Unknown module: $module_name" >&2
    echo "Run ./scripts/install.sh --list to see valid modules." >&2
    exit 1
  fi
  if [[ -z "${seen_modules[$module_name]+x}" ]]; then
    seen_modules["$module_name"]=1
    ORDERED_MODULES+=("$module_name")
  fi
done

mkdir -p "$SKILLS_DIR" "$AGENTS_DIR"

echo "=== AI Research Toolkit — Install Skills & Agents ==="
echo "Repo root: $REPO_ROOT"
if [[ -n "$PROFILE" ]]; then
  echo "Profile: $PROFILE"
else
  echo "Modules: ${ORDERED_MODULES[*]}"
fi
echo "Skills target: $SKILLS_DIR"
echo "Agents target: $AGENTS_DIR"
echo "Force overwrite: $FORCE"
echo

skills_installed=0
skills_skipped=0
agents_installed=0
agents_skipped=0

for module_name in "${ORDERED_MODULES[@]}"; do
  module_dir="$MODULES_ROOT/$module_name"
  skill_dirs=()
  agent_files=()

  if [[ -d "$module_dir/skills" ]]; then
    for path in "$module_dir"/skills/*; do
      [[ -d "$path" ]] && skill_dirs+=("$path")
    done
  fi
  if [[ -d "$module_dir/agents" ]]; then
    for path in "$module_dir"/agents/*.md; do
      [[ -f "$path" ]] && agent_files+=("$path")
    done
  fi

  if [[ ${#skill_dirs[@]} -eq 0 && ${#agent_files[@]} -eq 0 ]]; then
    echo "Module $module_name has no installable skills or agents." >&2
    exit 1
  fi

  echo "--- $module_name ---"

  for skill_dir in "${skill_dirs[@]}"; do
    skill_name="$(basename "$skill_dir")"
    dest="$SKILLS_DIR/$skill_name"
    if [[ -e "$dest" ]]; then
      if $FORCE; then
        rm -rf "$dest"
        cp -R "$skill_dir" "$dest"
        echo "  [UPDATED] skill: $skill_name"
        ((skills_installed+=1))
      else
        echo "  [SKIP] skill: $skill_name"
        ((skills_skipped+=1))
      fi
    else
      cp -R "$skill_dir" "$dest"
      echo "  [INSTALLED] skill: $skill_name"
      ((skills_installed+=1))
    fi
  done

  for agent_file in "${agent_files[@]}"; do
    agent_name="$(basename "$agent_file")"
    dest="$AGENTS_DIR/$agent_name"
    if [[ -e "$dest" ]]; then
      if $FORCE; then
        cp -f "$agent_file" "$dest"
        echo "  [UPDATED] agent: $agent_name"
        ((agents_installed+=1))
      else
        echo "  [SKIP] agent: $agent_name"
        ((agents_skipped+=1))
      fi
    else
      cp "$agent_file" "$dest"
      echo "  [INSTALLED] agent: $agent_name"
      ((agents_installed+=1))
    fi
  done

  echo
done

echo "=== Summary ==="
echo "Skills installed/updated: $skills_installed"
echo "Skills skipped: $skills_skipped"
echo "Agents installed/updated: $agents_installed"
echo "Agents skipped: $agents_skipped"
echo
echo "Skills with path placeholders may still require customization:"
echo "  <PAPER_SEARCH_MCP_PATH>"
echo "  <OBSIDIAN_VAULT>"
echo "  <KNOWLEDGE_BASE_PATH>"
echo "  <KB_SCRIPTS_PATH>"
echo "  <DRAWIO_OUTPUT_DIR>"
echo
echo "Run ./scripts/verify-setup.sh to verify core dependencies and install targets."
