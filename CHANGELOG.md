# Changelog

All notable changes to this project will be documented in this file.
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
