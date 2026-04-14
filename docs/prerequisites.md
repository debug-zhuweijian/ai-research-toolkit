# Prerequisites

## Required Software

### Python 3.10+

```bash
# Recommended: Install Anaconda
# Download from https://www.anaconda.com/download
# Verify:
python --version    # Should show 3.10+
conda --version
```

### Node.js 18+

```bash
# Download LTS from https://nodejs.org/
# Verify:
node --version      # Should show v18+
npm --version
```

### Git

```bash
# Download from https://git-scm.com/
# Verify:
git --version
```

### uv (Python Package Manager)

```bash
# Windows (PowerShell):
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify:
uv --version
```

### Claude Code

```bash
# Install:
npm install -g @anthropic-ai/claude-code

# First run (will prompt for API key):
claude

# Verify:
claude --version
```

Claude Code requires an Anthropic API key. See [API Keys Guide](api-keys-guide.md) for registration.

## Optional Software

### Obsidian

Desktop note-taking app for knowledge vault management.
Download from [obsidian.md](https://obsidian.md)

### Zotero

Reference manager for CNKI/Chinese academic papers.
Download from [zotero.org](https://www.zotero.org)

## Environment Setup

### Conda Environments

```bash
# Base environment (already exists if you have Anaconda)
conda activate base

# MemPalace environment (Phase 4)
conda create -n mempalace python=3.12
conda activate mempalace
pip install mempalace
```

### Directory Structure

Create the following directories:

```bash
# Claude Code config directory (usually auto-created)
mkdir -p ~/.claude/skills
mkdir -p ~/.claude/agents
mkdir -p ~/.claude/mcp-servers

# Working directories (choose your own paths)
mkdir -p ~/research/papers        # Downloaded papers
mkdir -p ~/research/knowledge     # Knowledge base
mkdir -p ~/obsidian-vault/base    # Obsidian vault for notes
```

## Verify Everything

After installing all prerequisites, run:

```bash
python --version   # 3.10+
node --version     # 18+
git --version
uv --version
claude --version
```

All commands should return version numbers without errors.
