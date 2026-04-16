<div align="center">

# AI Research Toolkit

**Full-pipeline AI-assisted academic research workflow powered by Claude Code**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.2.0--alpha-orange.svg)](CHANGELOG.md)

[English](README.md) | [中文](README.zh-CN.md)

</div>

A comprehensive academic research toolkit covering the full pipeline from literature discovery to publication. 42 skills, 16 agents, 10 MCP servers, organized into 7 research phases.

## 7-Phase Pipeline

| Phase | Module | Skills | Agents | Description |
|-------|--------|--------|--------|-------------|
| 01 | [Discovery](modules/01-discovery/README.md) | 5 | 2 | Literature search & management |
| 02 | [Processing](modules/02-processing/README.md) | 2 | — | Document parsing (PDF/DOCX/PPTX/XLSX) |
| 03 | [Analysis](modules/03-analysis/README.md) | 9 | 5 | Paper review & deep research |
| 04 | [Writing](modules/04-writing/README.md) | 9 | 7 | Academic writing & publication |
| 05 | [Knowledge](modules/05-knowledge/README.md) | 10 | 2 | Knowledge graphs & Obsidian workflows |
| 06 | [Presentation](modules/06-presentation/README.md) | 7 | — | Slides, figures & infographics |
| 07 | [Pipeline](modules/07-pipeline/README.md) | — | — | Cross-phase orchestration (planned) |
| **Total** | | **42** | **16** | |

## Quick Start

### Prerequisites

- [Claude Code](https://claude.ai/code) installed
- Python 3.10+ (Anaconda recommended)
- Node.js 18+
- Git 2.30+

### Install

```bash
# Clone
git clone https://github.com/debug-zhuweijian/ai-research-toolkit.git
cd ai-research-toolkit

# Install with profile
./scripts/install.sh --profile researcher    # Recommended for researchers
./scripts/install.sh --profile writer        # For paper writing
./scripts/install.sh --profile full          # Everything
./scripts/install.sh --module 03-analysis    # Or install individual phases

# Configure MCP servers
# Edit ~/.claude.json and merge configs/mcp-servers-full.json
```

### Profile Presets

| Profile | Modules | Skills | Best For |
|---------|---------|--------|----------|
| `minimal` | 01, 02 | 7 | Literature search & document processing |
| `writer` | 04, 06 | 16 | Academic writing & presentations |
| `researcher` | 01-04 | 25 | Full research workflow |
| `knowledge` | 05, 06 | 17 | Knowledge management & Obsidian |
| `full` | 01-06 | 42 | Complete toolkit |

## MCP Servers

| Server | Phase | Purpose |
|--------|-------|---------|
| paper-search-mcp | 01 | 20+ database paper search |
| zotero-mcp | 01 | Zotero local management |
| arxiv-latex-mcp | 01 | arXiv LaTeX source retrieval |
| mineru-mcp | 02 | PDF to Markdown conversion |
| pdf-mcp | 02 | PDF manipulation |
| mempalace | 05 | Knowledge graph memory |

Global servers (web-search-prime, web-reader, zread, zai-mcp-server, GitKraken) configured via `configs/mcp-servers-full.json`.

## Documentation

- [Installation Guide](docs/installation-guide.md)
- [Prerequisites](docs/prerequisites.md)
- [API Keys Guide](docs/api-keys-guide.md)
- [Pipeline Overview](docs/pipeline-overview.md)
- [Troubleshooting](docs/troubleshooting.md)

## Experimental

See [experimental/README.md](experimental/README.md) for DeepScientist agents (require separate platform).

## What's New in v0.2

- **Phase-based module structure** — organized into 7 research phases
- **29 NEW skills** — brainstorming, ML paper writing, Obsidian workflows, and more
- **15 NEW agents** — literature reviewers, LaTeX specialists, rebuttal writers
- **5 profile presets** — install only what you need
- **14 DeepScientist agents** moved to experimental/
- **5 kb-* empty shells** removed

See [CHANGELOG.md](CHANGELOG.md) for full details.

## License

MIT
