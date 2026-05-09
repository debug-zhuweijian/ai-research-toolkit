# Paperclip Pipeline Workflow

The Paperclip pipeline coordinates research work across AI Research Toolkit phases without replacing the tools in those phases.

## Flow

1. Intake the research goal and constraints.
2. Map the goal to phases `01-discovery` through `06-presentation`.
3. Split work into independent agent tasks.
4. Assign each task a required output path and evidence requirement.
5. Run agents in parallel when tasks do not share mutable state.
6. Collect handoff packets.
7. Verify key files, diffs, and command outputs directly.
8. Synthesize final deliverables.
9. Run security checks before public release or sync.
10. Produce release-safe docs, modules, configs, scripts, README updates, or changelog entries.

## Phase Mapping

| Phase | Example agent work |
| --- | --- |
| 01 Discovery | Search papers, classify sources, export candidate lists. |
| 02 Processing | Convert PDFs to Markdown and check extraction quality. |
| 03 Analysis | Review methods, evidence, citations, and limitations. |
| 04 Writing | Draft sections, polish prose, prepare rebuttal material. |
| 05 Knowledge | Ingest notes, update graph views, maintain reusable knowledge. |
| 06 Presentation | Prepare slides, figures, diagrams, and meeting summaries. |
| 07 Pipeline | Coordinate the above work, enforce handoffs, verify evidence, and guard release boundaries. |

## Checkpoints

Use checkpoints after:

- Initial task decomposition.
- First agent handoff batch.
- Synthesis draft.
- Security scan.
- Release repository sync.

A checkpoint must include current files, open risks, verification evidence, and the next action.
