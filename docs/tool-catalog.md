# AI Research Toolkit Public Tool Catalog

This catalog covers the public repository surface for `v0.3.0-beta.2`. It lists only modules, skills, agents, scripts, templates, and public integrations included in this repository or documented as upstream dependencies.

This repository is not a mirror of a private local Claude environment. Private local skills, private agents, plugin caches, credentials, API keys, private URLs, runtime IDs, logs, databases, and machine-specific paths are intentionally excluded.

## Research Discovery

Public module: [`modules/01-discovery`](../modules/01-discovery/)

Skills included:

- `0-autoresearch-skill`
- `academic-pipeline`
- `daily-paper-generator`
- `paper-search`
- `zotero-obsidian-bridge`

Public upstream integrations documented by the repo:

- `paper-search-mcp`
- `zotero-mcp`
- `arxiv-latex-mcp`
- Zotero, Jasminum, and `translators_CN`

## Document, PDF, And Office Processing

Public module: [`modules/02-processing`](../modules/02-processing/)

Skills included:

- `document-skills`
- `Geek-skills-mineru-pdf-parser`

Public upstream integrations documented by the repo:

- MinerU / OpenXLab
- `pdf-mcp`
- MarkItDown
- LibreOffice and Poppler for Office/PDF conversion support

## Literature Review And Evidence Analysis

Public module: [`modules/03-analysis`](../modules/03-analysis/)

Skills included:

- `academic-paper-reviewer`
- `brainstorming-research-ideas`
- `confidence-check`
- `content-research-writer`
- `creative-thinking-for-research`
- `deep-research-v5`
- `paper-proofread`
- `paper-review`
- `research-ideation`

Public upstream integrations documented by the repo:

- Sequential Thinking MCP
- Web search and web reader MCP patterns

## Writing And Revision

Public module: [`modules/04-writing`](../modules/04-writing/)

Skills included:

- `academic-paper`
- `academic-writing`
- `ml-paper-writing`
- `post-acceptance`
- `results-analysis`
- `results-report`
- `review-response`
- `systems-paper-writing`
- `writing-anti-ai`

## Knowledge Graph, Obsidian, Graphify, And MemPalace

Public module: [`modules/05-knowledge`](../modules/05-knowledge/)

Skills included:

- `graphify`
- `knowledge-base`
- `knowledge-distillation`
- `obsidian-bases`
- `obsidian-cli`
- `obsidian-experiment-log`
- `obsidian-literature-workflow`
- `obsidian-markdown`
- `obsidian-project-bootstrap`
- `obsidian-project-memory`

Public scripts and integrations:

- [`modules/05-knowledge/skills/graphify/rebuild_graph.py`](../modules/05-knowledge/skills/graphify/rebuild_graph.py)
- Graphify
- MemPalace
- ChromaDB
- Obsidian workflow conventions

## Presentation And Figures

Public module: [`modules/06-presentation`](../modules/06-presentation/)

Skills included:

- `academic-plotting`
- `academic-pptx`
- `drawio`
- `group-meeting-slides`
- `notion-infographic`
- `presenting-conference-talks`
- `publication-chart-skill`

Public upstream integrations documented by the repo:

- draw.io MCP
- Playwright MCP patterns for visual verification

## Pipeline Orchestration

Public module: [`modules/07-pipeline`](../modules/07-pipeline/)

Active beta skill:

- `paperclip-pipeline`

Public templates and verification:

- [`modules/07-pipeline/configs/paperclip.example.json`](../modules/07-pipeline/configs/paperclip.example.json)
- [`scripts/verify-paperclip-config.sh`](../scripts/verify-paperclip-config.sh)
- [`scripts/verify-paperclip-config.ps1`](../scripts/verify-paperclip-config.ps1)

The public Paperclip surface contains workflow contracts, handoff packet conventions, and sanitized configuration templates. It does not include a private Paperclip service connector or deployment details.

## Verification And Handoff Governance

Public scripts:

- [`scripts/install.sh`](../scripts/install.sh)
- [`scripts/install.ps1`](../scripts/install.ps1)
- [`scripts/verify-setup.sh`](../scripts/verify-setup.sh)
- [`scripts/verify-profiles.py`](../scripts/verify-profiles.py)
- [`scripts/scan-public-safety.py`](../scripts/scan-public-safety.py)
- [`scripts/verify-paperclip-config.sh`](../scripts/verify-paperclip-config.sh)
- [`scripts/verify-paperclip-config.ps1`](../scripts/verify-paperclip-config.ps1)

Supported install profiles:

- `minimal`: Phase 01 and Phase 02
- `researcher`: Phase 01 through Phase 04
- `writer`: Phase 04 and Phase 06
- `knowledge`: Phase 05 and Phase 06
- `full`: Phase 01 through Phase 07

The profile verifier recalculates skills from module contents and checks JSON profile definitions, Bash installer support, and PowerShell installer support.

## Experimental Agents

Public experimental area: [`experimental/`](../experimental/)

The experimental directory documents DeepScientist-style agents that require a separate platform. They are not installed by the standard profile installers and are not treated as part of the default public runtime surface.

## Private And Local Integrations Boundary

The public repo may describe integration categories such as Claude Code, MCP servers, Obsidian, Graphify, MemPalace, Zotero, MinerU, and BigModel. It must not include:

- Real API keys, access tokens, refresh tokens, cookies, or private keys.
- Private VPS URLs, private OpenAI-compatible endpoints, private base URLs, or private model defaults.
- Local authentication JSON files, `.env` files, logs, databases, coverage output, caches, or runtime exports.
- Local-only `.claude`, `.codex`, `.agents`, or plugin-cache skill and agent bodies.
- Machine-specific absolute paths except placeholder examples.

Use placeholder values such as `<ANTHROPIC_API_KEY>`, `<BIGMODEL_API_KEY>`, `<MINERU_API_KEY>`, `<BASE_URL>`, and `<ANTHROPIC_COMPATIBLE_BASE_URL>` in public docs and templates.
