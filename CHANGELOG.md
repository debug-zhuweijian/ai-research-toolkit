# Changelog

All notable changes to this project will be documented in this file.

## [unreleased]

### Added

- rebuild_graph.py: GraphRAG-inspired semantic extraction pipeline (LLM entity extraction, incremental caching, Louvain community detection, gleaning)
- Updated all 4 READMEs with rebuild_graph.py in Phase 05 table, description, and What's New section
- Restructured Acknowledgments into 4 categories (Skill Sources, MCP Servers, Zotero Ecosystem, Special Thanks)
- Added 9 missing upstream project credits (AI-Research-SKILLs, academic-research-skills, anthropics/skills, a-evolve, writing-anti-ai, DeerFlow, drawio-mcp, Context7, langsmith-fetch-skill)
- Full audit of 26 git-project repos against README credits (10 credited, 1 missing fixed, 15 unrelated)

### Fixed

- Reordered CHANGELOG to follow Keep a Changelog convention (`[unreleased]` at top)

## [0.2.0-beta] - 2026-04-17

### Added

- Japanese (README.ja.md) and Korean (README.ko.md) README translations
- Complete README rewrite (EN + ZH) with detailed usage walkthrough, tool map, API keys guide
- Mermaid 7-phase pipeline diagram
- LibreOffice and Poppler to prerequisites
- International alternatives for non-Chinese users (Tavily, Brave Search, etc.)
- `uvx paper-search-mcp` recommendation for dependency isolation

### Fixed

- Restored missing badges (GitHub Release, DeepWiki, Zread)
- Restored detailed sections lost in alpha rewrite (Acknowledgments, Contributing, Recommended Resources)

## [0.2.0-alpha] - 2026-04-17

### Added

- Phase-based module structure (`modules/01-discovery/` through `modules/07-pipeline/`)
- 29 NEW skills across all phases
- 15 NEW agents for analysis, writing, and knowledge management
- 5 profile presets (minimal, writer, researcher, knowledge, full)
- Module READMEs for all 7 phases
- Experimental directory for DeepScientist agents

### Changed

- Restructured from flat `skills/` and `agents/` to phase-based `modules/` layout
- README completely rewritten for v0.2

### Removed

- 5 kb-* empty shells (kb-scan, kb-apply, kb-lint, kb-stats, kb-sync)
- Flat `skills/` and `agents/` directories (replaced by modules/)

### Moved

- 14 DeepScientist agents → `experimental/deepscientist/`
- Old `deep-research.md` agent → `experimental/`

### Added

- Initial release of ai-research-toolkit
- Add paper-proofread skill + remove Anthropic key requirement
- Upgrade paper-proofread skill with full reference checklists
- Complete paper-search-mcp API key configuration guide
- Add GitHub links to all phase tool tables
- Replace domain-specific examples with generic ones
- Add comprehensive installation guide (8-step, 2-3 hours)
- Add bilingual README with language toggle (EN + 中文)
- Add DeepWiki, MIT license, Zread badges to bilingual READMEs
- Center title with badges and language toggle
- Add version control design spec (git-cliff + SemVer)
- Add version control implementation plan (6 tasks)
- Add git-cliff configuration for CHANGELOG generation

### Fixed

- Replace all hardcoded local paths with placeholders in docs
- Remove spurious dot in Mermaid diagram (.deep-research-v5 → deep-research-v5)
- Translate Chinese text in EN README + dark mode Mermaid theme
- Correct Python version check regex, update stale env var names and paths
- Fix README quality issues (hardcoded paths, missing tools, TOC)
- Update paper-proofread description in bilingual READMEs

### Changed

- Deduplicate XSD schemas into shared-schemas/
