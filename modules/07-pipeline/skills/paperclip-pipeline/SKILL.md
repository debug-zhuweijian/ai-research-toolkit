---
name: paperclip-pipeline
description: Coordinate multi-agent academic research workflows with sanitized Paperclip-style handoffs, verification gates, and release-safe outputs.
---

# Paperclip Pipeline

Use this skill when a research task spans multiple AI Research Toolkit phases and needs multiple agents, explicit handoff contracts, verification evidence, and release-safe output handling.

## When to Use

Use this skill for:

- Literature review projects that require search, PDF processing, analysis, writing, and knowledge-base updates.
- Multi-agent research tasks where work must be split across independent reviewers, writers, auditors, or curators.
- Release preparation tasks that must separate local debug work from public, sanitized GitHub output.
- Long-running research workflows that need checkpointing, handoff packets, and evidence-based acceptance.

Do not use this skill for:

- A single-paper quick summary.
- A one-file editing task.
- Directly connecting to a private Paperclip deployment.
- Publishing private runtime state, tokens, local paths, or account details.

## Inputs

Before starting, collect:

1. Research goal.
2. Target phases from `01-discovery` through `06-presentation`.
3. Source material location or public links.
4. Privacy boundary: public, private, and excluded outputs.
5. Required deliverables.
6. Verification commands or acceptance evidence.

## Workflow

1. Map the request to phases.
2. Split the work into independent agent tasks.
3. Assign each task a concrete output path and acceptance criteria.
4. Require each agent to return a handoff packet.
5. Verify key files and command outputs directly.
6. Synthesize final research artifacts.
7. Run the security boundary check before producing public outputs.
8. Prepare release-safe summaries, docs, or module changes.

## Handoff Contract

Every handoff must include:

- Task objective.
- Files read.
- Files modified.
- Commands run.
- Evidence produced.
- Assumptions made.
- Open risks.
- Next recommended step.

If a handoff omits evidence, treat it as incomplete.

## Verification Rule

Do not trust agent summaries blindly. Verify the final file tree, relevant diffs, and critical command outputs before marking a task complete.

## Security Boundary

Public outputs must not include:

- API keys, tokens, cookies, passwords, private keys, or secrets.
- Real service URLs, internal URLs, IP addresses, ports, database strings, OAuth values, team IDs, workspace IDs, or job IDs.
- Local absolute paths, user home directories, private Obsidian vault paths, private Zotero paths, or private Paperclip paths.
- Runtime logs, cache files, coverage artifacts, local task records, or private deployment configs.

Use placeholders such as `<PAPERCLIP_API_URL>` and `<PUBLIC_WORKSPACE_NAME>` in public templates.

## Phase Integration

Paperclip Pipeline coordinates the existing toolkit phases:

| Phase | Role in pipeline |
| --- | --- |
| 01 Discovery | Find papers, collect metadata, prepare Zotero intake. |
| 02 Processing | Convert PDFs and documents into Markdown. |
| 03 Analysis | Review papers, synthesize evidence, audit citations. |
| 04 Writing | Draft sections, polish prose, prepare responses or manuscripts. |
| 05 Knowledge | Ingest notes, update graph views, maintain research memory. |
| 06 Presentation | Produce slides, figures, diagrams, and meeting artifacts. |
| 07 Pipeline | Decompose tasks, coordinate agents, verify handoffs, and prepare release-safe outputs. |

## References

- `references/workflow.md` — end-to-end orchestration workflow.
- `references/handoff-contract.md` — required handoff packet schema.
- `references/security-boundary.md` — public/private output boundary.
- `references/release-sync.md` — debug-to-release synchronization protocol.
