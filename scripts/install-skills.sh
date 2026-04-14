#!/bin/bash
# install-skills.sh — Copy skills and agents to ~/.claude/
# Usage: ./scripts/install-skills.sh [--skills-path ~/.claude/skills] [--agents-path ~/.claude/agents]

SKILLS_DIR="$HOME/.claude/skills"
AGENTS_DIR="$HOME/.claude/agents"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# Parse args
while [[ $# -gt 0 ]]; do
  case $1 in
    --skills-path) SKILLS_DIR="$2"; shift 2 ;;
    --agents-path) AGENTS_DIR="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

echo "=== AI Research Toolkit — Install Skills & Agents ==="
echo "Skills target: $SKILLS_DIR"
echo "Agents target: $AGENTS_DIR"
echo ""

# Create directories
mkdir -p "$SKILLS_DIR" "$AGENTS_DIR"

# Copy skills (no-clobber to preserve existing)
echo "--- Installing Skills ---"
SKILL_COUNT=0
for skill_dir in "$REPO_ROOT"/skills/*/; do
  skill_name="$(basename "$skill_dir")"
  if [ -d "$SKILLS_DIR/$skill_name" ]; then
    echo "  [SKIP] $skill_name (already exists, use --force to overwrite)"
  else
    cp -r "$skill_dir" "$SKILLS_DIR/"
    echo "  [INSTALLED] $skill_name"
    ((SKILL_COUNT++))
  fi
done
echo "Installed $SKILL_COUNT new skills."

# Copy agents (no-clobber)
echo ""
echo "--- Installing Agents ---"
AGENT_COUNT=0
for agent_file in "$REPO_ROOT"/agents/*.md; do
  agent_name="$(basename "$agent_file")"
  if [ -f "$AGENTS_DIR/$agent_name" ]; then
    echo "  [SKIP] $agent_name (already exists)"
  else
    cp "$agent_file" "$AGENTS_DIR/"
    echo "  [INSTALLED] $agent_name"
    ((AGENT_COUNT++))
  fi
done
echo "Installed $AGENT_COUNT new agents."

echo ""
echo "=== Important: Path Placeholders ==="
echo "Some skills contain placeholder paths that you need to customize:"
echo ""
echo "  <PAPER_SEARCH_MCP_PATH>  → Path to paper-search-mcp installation"
echo "  <KB_SCRIPTS_PATH>        → Path to knowledge base scripts directory"
echo "  <KNOWLEDGE_BASE_PATH>    → Path to your knowledge base directory"
echo "  <OBSIDIAN_VAULT>         → Path to your Obsidian vault"
echo ""
echo "Run these commands to replace placeholders:"
echo ""
echo "  # Example (adjust paths to your system):"
echo "  sed -i 's|<PAPER_SEARCH_MCP_PATH>|/c/Users/you/paper-search-mcp|g' $SKILLS_DIR/paper-search/SKILL.md"
echo "  sed -i 's|<KB_SCRIPTS_PATH>|/c/Users/you/scripts/knowledge-base|g' $SKILLS_DIR/knowledge-base/SKILL.md"
echo "  sed -i 's|<OBSIDIAN_VAULT>|/c/Users/you/obsidian-vault|g' $SKILLS_DIR/Geek-skills-mineru-pdf-parser/SKILL.md"
echo ""
echo "Done! Run ./scripts/verify-setup.sh to verify installation."
