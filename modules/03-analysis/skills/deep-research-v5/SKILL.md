---
name: deep-research
description: 基于子代理的深度研究流水线，生成带引用、可验证的长篇报告。主代理规划与综合，子代理并行调查并写入结构化笔记
compatibility: "Requires web_search and web_fetch. Optimal with subagent dispatch (Claude Code, Cowork, DeerFlow). Degrades gracefully to single-thread on Claude.ai."
---
# Deep Research V5

Lead agent plans. Subagents investigate. Notes bridge the gap.

## Architecture

```
Lead Agent (coordinator — never searches)
  |
  P1: Research Task Board (roles, queries, parallel groups)
  |
  Dispatch ──→ Subagent A ──→ writes task-a.md ──┐
           ──→ Subagent B ──→ writes task-b.md ──┤ (parallel)
           ──→ Subagent C ──→ writes task-c.md ──┘
  |                                               |
  |     workspace/research-notes/  <──────────────┘
  |
  P3: Read notes → build Citation Registry
  P4: Outline from notes
  P5: Draft from notes (never from raw search results)
  P6: Critique (claims traceable to notes?)
  P7: Verify (every [n] in registry? every claim in notes?)
  P8: Polish → final report
```

**Context savings:** Subagents' raw search results (15-30K tokens) stay in their
own context and are discarded on exit. Lead agent sees only distilled notes
(~3K tokens total). Estimated 60-70% context reduction on lead agent.

## P0: Environment Detection

```
1. Subagent capable?
   - Claude Code / Cowork: YES (use `claude -p` or subagent dispatch)
   - DeerFlow / OpenClaw: YES (use task tool)
   - Claude.ai: NO → degraded mode (lead executes tasks sequentially)
2. web_search available? web_fetch available?
3. Filesystem writable? (for notes files)
4. Select mode: Standard (5-6 tasks) / Lightweight (3-4 tasks)
```

Report: `[P0 complete] Subagent: {yes/no}. Mode: {standard/lightweight}.`

## P1: Research Task Board

**Read `reference/methodology.md` for full task board generation rules.**

Lead agent decomposes the research question into 4-6 investigation tasks.
Each task has: expert role, objective, pre-planned queries, depth level, output path, parallel group.

```
# Research Task Board
Topic: {question}

## Group A (parallel)
Task A: [Economic Historian] — Luddite movement timeline and impact
Task B: [Transport Historian] — Automobile replacing horse carriage
Task C: [Telecom Analyst] — Telephone operator automation
## Group B (depends on A)
Task D: [Comparative Analyst] — AI speed vs historical revolutions
```

## P2: Dispatch + Investigate

**Read `reference/subagent-prompt.md` for the prompt given to each subagent.**
**Read `reference/research-notes-format.md` for the notes file format.**

Each subagent receives a scoped prompt and writes findings to its own notes file.
Subagents search, fetch full articles, extract findings, assess authority.
Max 3 concurrent subagents (ref: DeerFlow SubagentLimitMiddleware).

**Iterative Deepening (the #1 quality lever):**
When a subagent discovers a named entity during search — a product (Glean™),
a trial (FUTURE trial), a regulatory event (FDA 510k), a dataset — it MUST
chase that lead with 1-3 additional targeted searches. Stopping at first
mention is the primary cause of missing critical findings.

Tool budget per subagent: DEEP 4-8 searches + 2-4 fetches, SCAN 2-4 searches.

**Degraded mode (Claude.ai):** Lead agent executes each task sequentially,
writing notes blocks to conversation after each task. Same format, same
iterative deepening requirement, just inline.

## P3-P8: Synthesis Pipeline

**P3 Citation Registry:** Read all task notes. Merge sources, deduplicate,
assign final [n] numbers, drop low-quality. Lead agent builds registry from
notes — never from memory of search results it didn't see.

**Before P3, P2.5 Gap-Filling Dispatch:** Lead reads all task notes, collects
`Leads Discovered` entries, and dispatches 1-3 follow-up subagents for
high-value leads not fully investigated (specific products, landmark trials,
FDA approvals, etc.). This is what prevents missing breakthroughs like
Glean™ or FUTURE trial that a subagent mentioned but didn't deep-dive.

**P4 Outline:** Map findings from notes to report sections. Cross-reference
patterns across tasks (e.g., "all three historical cases show displacement hump").

**P5 Draft:** Write from notes only. Every claim must trace to a specific
task note finding. Citations only from P3 registry.

**P6 Critique:** Must find 3+ issues. Check: any claim not in any task note?

**P7 Verify:** Cross-check every [n] against registry. Spot-check 5 claims
against their source task notes with visible output.

**P8 Polish:** Final formatting, executive summary, save report.

**Read `reference/methodology.md` for full P3-P8 instructions.**
**Read `reference/quality-gates.md` for validation thresholds.**
**Read `reference/report-assembly.md` for report structure.**

## Anti-Hallucination Rules

1. Lead agent never invents URLs — it only uses URLs from subagent notes
2. Lead agent never fabricates data — if a number isn't in any task note, mark [unverified]
3. Subagents never invent URLs — only from actual search results
4. Dropped sources in P3 registry must never reappear in P5
5. No [n] in P5 that doesn't exist in P3 registry
6. Subagents never stop at first mention — if a search reveals a specific named
   product, trial, dataset, or regulatory event, the subagent MUST chase it with
   additional targeted searches. A finding that says "X system exists" without
   a dedicated source on X is incomplete.

## Progress Reporting

One-line status after each phase. Terse, factual, no decoration.
```
[P0 complete] Subagent: yes. Standard mode. 5 tasks planned.
[P1 complete] Task board: 5 tasks in 2 groups. Dispatching Group A (3 tasks).
[P2 task-a complete] 4 sources, 6 findings. Luddite movement covered.
[P2 task-b complete] 3 sources, 5 findings. Horse-to-car transition covered.
[P2 all complete] 5 tasks done, 18 sources total. Scanning leads.
[P2.5 complete] 2 leads triaged (Glean™, FUTURE trial), 2 follow-ups dispatched.
[P3 complete] Registry: 14 approved, 4 dropped. 10 unique domains.
[P5 in progress] 3/5 sections drafted, ~2800 words.
[P7 complete] 5 spot-checks passed. 0 registry violations.
[DONE] ~5000 words, 14 sources, 42 citations.
```
