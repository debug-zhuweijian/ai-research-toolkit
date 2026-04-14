#!/bin/bash
# verify-setup.sh — Health check for ai-research-toolkit
# Run from the repo root: ./scripts/verify-setup.sh

PASS=0
FAIL=0

check() {
  local name="$1"
  local cmd="$2"
  if eval "$cmd" &>/dev/null; then
    echo "  [PASS] $name"
    ((PASS++))
  else
    echo "  [FAIL] $name"
    ((FAIL++))
  fi
}

echo "=== AI Research Toolkit — Setup Verification ==="
echo ""

echo "--- Core Dependencies ---"
check "Python 3.10+" "python --version | grep -E '3\.1[0-9]|3\.[2-9]'"
check "Node.js 18+" "node --version | grep -E 'v(1[8-9]|[2-9][0-9])'"
check "Git" "git --version"
check "uv" "uv --version"
check "Claude Code" "claude --version"

echo ""
echo "--- MCP Servers ---"
check "mineru-mcp-server" "which mineru-mcp-server || pip show mineru-mcp-server"
check "pdf-mcp directory" "test -d ~/.claude/mcp-servers/pdf-mcp"
check "npx available" "which npx"

echo ""
echo "--- Claude Code Skills ---"
for skill in paper-search paper-review academic-writing deep-research-v5 knowledge-base graphify academic-pptx; do
  check "skill: $skill" "test -d ~/.claude/skills/$skill"
done

echo ""
echo "--- Claude Code Agents ---"
check "agent: deep-research" "test -f ~/.claude/agents/deep-research.md"
check "agent: deepscientist-scout" "test -f ~/.claude/agents/deepscientist-scout.md"

echo ""
echo "--- Optional Tools ---"
check "Graphify" "graphify --version 2>/dev/null || pip show graphifyy"
check "MemPalace" "python -c 'import mempalace' 2>/dev/null"
check "Obsidian CLI" "which obsidian 2>/dev/null || test -d /c/Users/*/AppData/Local/Obsidian 2>/dev/null"

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="

if [ $FAIL -gt 0 ]; then
  echo ""
  echo "Some checks failed. See docs/troubleshooting.md for help."
  exit 1
else
  echo ""
  echo "All checks passed! Your research toolkit is ready."
  exit 0
fi
