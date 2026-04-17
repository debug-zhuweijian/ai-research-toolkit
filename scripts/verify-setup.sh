#!/usr/bin/env bash
# verify-setup.sh — Health check for ai-research-toolkit installs.

set -euo pipefail

SKILLS_DIR="${HOME}/.claude/skills"
AGENTS_DIR="${HOME}/.claude/agents"
PASS=0
FAIL=0

usage() {
  cat <<'EOF'
Usage:
  ./scripts/verify-setup.sh [--skills-path <dir>] [--agents-path <dir>]
EOF
}

check() {
  local name="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    echo "  [PASS] $name"
    PASS=$((PASS + 1))
  else
    echo "  [FAIL] $name"
    FAIL=$((FAIL + 1))
  fi
}

check_optional() {
  local name="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    echo "  [PASS] $name"
  else
    echo "  [INFO] $name not found"
  fi
}

check_python_version() {
  python - <<'PY'
import sys
raise SystemExit(0 if sys.version_info >= (3, 10) else 1)
PY
}

check_node_version() {
  node -e "const [major] = process.versions.node.split('.').map(Number); process.exit(major >= 18 ? 0 : 1)"
}

count_skill_dirs() {
  find "$SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d '[:space:]'
}

count_agent_files() {
  find "$AGENTS_DIR" -mindepth 1 -maxdepth 1 -type f -name '*.md' | wc -l | tr -d '[:space:]'
}

check_nonempty_skills_dir() {
  [[ -d "$SKILLS_DIR" ]] && [[ "$(count_skill_dirs)" -gt 0 ]]
}

while [[ $# -gt 0 ]]; do
  case "$1" in
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

echo "=== AI Research Toolkit — Setup Verification ==="
echo "Skills path: $SKILLS_DIR"
echo "Agents path: $AGENTS_DIR"
echo

echo "--- Core Dependencies ---"
check "Python 3.10+" check_python_version
check "Node.js 18+" check_node_version
check "Git" command -v git
check "uv" command -v uv
check "Claude Code" command -v claude

echo
echo "--- Runtime Commands ---"
check "npx available" command -v npx
check "mineru-mcp-server available" command -v mineru-mcp-server

echo
echo "--- Install Targets ---"
check "Skills directory has installed skills" check_nonempty_skills_dir
check "Agents directory exists" test -d "$AGENTS_DIR"

if [[ -d "$SKILLS_DIR" ]]; then
  echo "  [INFO] Installed skills: $(count_skill_dirs)"
fi
if [[ -d "$AGENTS_DIR" ]]; then
  echo "  [INFO] Installed agents: $(count_agent_files)"
fi

echo
echo "--- Optional Integrations ---"
check_optional "Graphify CLI" command -v graphify
check_optional "MemPalace import" python -c "import mempalace"
check_optional "Obsidian CLI" command -v obsidian

echo
echo "=== Results: $PASS passed, $FAIL failed ==="

if [[ $FAIL -gt 0 ]]; then
  echo
  echo "Some checks failed. See docs/troubleshooting.md for help."
  exit 1
fi

echo
echo "Core checks passed."
