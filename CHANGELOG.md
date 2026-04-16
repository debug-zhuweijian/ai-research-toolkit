# Changelog

All notable changes to this project will be documented in this file.

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

## [unreleased]

### 🚀 Features

- Initial release of ai-research-toolkit
- Add paper-proofread skill + remove Anthropic key requirement
- Upgrade paper-proofread skill with full reference checklists

### 🐛 Bug Fixes

- Replace all hardcoded local paths with placeholders in docs
- Remove spurious dot in Mermaid diagram (.deep-research-v5 → deep-research-v5)
- Translate Chinese text in EN README + dark mode Mermaid theme
- Correct Python version check regex, update stale env var names and paths

### ♻️ Refactor

- Deduplicate XSD schemas into shared-schemas/

### 📚 Documentation

- Complete paper-search-mcp API key configuration guide
- Add GitHub links to all phase tool tables
- Replace domain-specific examples with generic ones
- Add comprehensive installation guide (8-step, 2-3 hours)
- Fix README quality issues (hardcoded paths, missing tools, TOC)
- Add bilingual README with language toggle (EN + 中文)
- Add DeepWiki badge to bilingual READMEs
- Add MIT license badge to bilingual READMEs
- Center title with badges and language toggle
- Add Zread badge to bilingual READMEs
- Update paper-proofread description in bilingual READMEs
- Add version control design spec (git-cliff + SemVer)
- Add version control implementation plan (6 tasks)

### 🔧 Miscellaneous

- Add git-cliff configuration for CHANGELOG generation
