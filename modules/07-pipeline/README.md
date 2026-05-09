---
phase: 07-pipeline
title: Pipeline Orchestration
status: active-beta
---

# Phase 07: Pipeline Orchestration

Phase 07 coordinates the earlier AI Research Toolkit phases with a Paperclip-style multi-agent workflow. It turns discovery, processing, analysis, writing, knowledge management, and presentation tasks into explicit agent assignments with handoff packets and verification gates.

## Status

Active beta in `v0.3.0-beta.1`.

This phase provides public workflow protocols and sanitized templates. It does not include private Paperclip deployment details or a production connector to a private Paperclip service.

## Components

### Skills

| Skill | Purpose | Status |
| --- | --- | --- |
| `paperclip-pipeline` | Multi-agent orchestration, handoff contracts, verification gates, and release-safe outputs | active-beta |

### Configs

| Config | Purpose |
| --- | --- |
| `configs/paperclip.example.json` | Placeholder-only Paperclip pipeline configuration template |

## Workflow

```text
01-discovery -> 02-processing -> 03-analysis
                                      |
                                      v
06-presentation <- 05-knowledge <- 04-writing
                                      |
                                      v
07-pipeline: decompose -> dispatch -> handoff -> verify -> sanitize -> release
```

## Design Goals

- Coordinate work across Phase 01-06 without replacing those tools.
- Require explicit handoff packets for multi-agent work.
- Verify files, diffs, and command outputs instead of trusting summaries alone.
- Keep public outputs free of real paths, accounts, tokens, private URLs, logs, and runtime state.
- Support debug-to-release synchronization through whitelist and security gates.

## Verification

Run:

```bash
./scripts/verify-paperclip-config.sh
```

Expected:

```text
[PASS] Paperclip template files are public-safe
[PASS] Paperclip references are present
[PASS] Paperclip skill files verified
```
