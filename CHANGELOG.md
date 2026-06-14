# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

- Future changes go here.

## [0.3.0-beta.2] - 2026-06-15

### Added

- Added `scripts/scan-public-safety.py` for tracked-tree, staged-index, and release-note safety scans.
- Added `scripts/verify-profiles.py` to validate profile JSON, module availability, Bash installer support, and PowerShell installer support.
- Added public tool catalogs in `docs/tool-catalog.md` and `docs/tool-catalog.zh-CN.md`.

### Changed

- Updated the GitHub release workflow so `*-alpha`, `*-beta`, and `*-rc` tags publish as prereleases and do not become Latest.
- Added release-note safety scanning after `git-cliff` generates `CHANGELOG.md` for GitHub release bodies.
- Reconciled the five supported profiles: `minimal`, `researcher`, `writer`, `knowledge`, and `full`.
- Updated the `full` profile to cover Phase 01 through Phase 07, including `paperclip-pipeline`.
- Kept the `skills_count` profile field for compatibility while verifying it against dynamic module contents.
- Refreshed README files with current beta, profile, public/private boundary, and catalog facts.
- Cleaned API key examples so public docs use placeholders such as `<ANTHROPIC_API_KEY>`, `<BIGMODEL_API_KEY>`, `<MINERU_API_KEY>`, and `<ANTHROPIC_COMPATIBLE_BASE_URL>`.

### Security

- Added staged and public-tree checks for secrets, private URLs, local machine paths, sensitive runtime files, logs, databases, caches, and release body leakage.
- Documented that this public repository is not a mirror of a private local Claude environment and does not include local-only `.claude`, `.codex`, `.agents`, or plugin-cache skill/agent bodies.

## [0.3.0-beta.1] - 2026-06-14

### Added

- Phase 07 Paperclip pipeline orchestration module as an active beta.
- `paperclip-pipeline` skill for multi-agent academic research coordination, handoff contracts, direct verification, and release-safe output handling.
- Paperclip reference protocols for workflow, handoff packets, security boundaries, and debug-to-release synchronization.
- Placeholder-only `paperclip.example.json` public config template.
- `verify-paperclip-config` scripts for checking public templates without contacting a private Paperclip service.

### Changed

- Updated README family to describe Phase 07 as Paperclip-style orchestration instead of a planned pipeline stage.
- Documented sanitized debug-to-release sync boundaries for public GitHub publishing.

## [0.2.0-alpha] - 2026-04-17

### Added

- Phase-based module structure under `modules/01-discovery/` through `modules/07-pipeline/`.
- New skills across discovery, processing, analysis, writing, knowledge, presentation, and pipeline phases.
- New agents for analysis, writing, and knowledge management workflows.
- Profile presets for installing only selected workflow slices.
- Module READMEs for all seven phases.
- Experimental directory for DeepScientist agents.

### Changed

- Restructured from flat `skills/` and `agents/` directories to the phase-based `modules/` layout.
- Rewrote README content for the v0.2 public workflow.

### Removed

- Removed the `kb-scan`, `kb-apply`, `kb-lint`, `kb-stats`, and `kb-sync` empty shell entries.
- Removed the old flat `skills/` and `agents/` directories in favor of phase modules.

### Moved

- Moved DeepScientist agents to `experimental/deepscientist/`.
- Moved the old `deep-research.md` agent to `experimental/`.

## [0.1.x history]

### Added

- Initial release of `ai-research-toolkit`.
- Added `paper-proofread` skill and removed the Anthropic key requirement from that workflow.
- Upgraded `paper-proofread` with full reference checklists.
- Added `git-cliff` configuration for changelog generation.

### Fixed

- Replaced hardcoded local paths with placeholders in public docs.
- Removed a spurious dot in the Mermaid diagram.
- Translated Chinese text in the English README and switched Mermaid examples to a dark-mode-safe theme.
- Corrected Python version check regex and updated stale environment variable names and paths.

### Changed

- Deduplicated XSD schemas into `shared-schemas/`.
- Added GitHub links to phase tool tables.
- Replaced domain-specific examples with generic ones.
- Added the installation guide, bilingual README support, DeepWiki badge, MIT license badge, Zread badge, and version-control planning docs.
