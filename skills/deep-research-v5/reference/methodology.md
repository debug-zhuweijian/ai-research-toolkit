# Deep Research Methodology V5 — Subagent-First Pipeline

## P0: Environment Detection

Detect capabilities before anything else.

| Check | Result | Impact |
|-------|--------|--------|
| Subagent dispatch available? | Yes → full architecture | No → degraded sequential mode |
| web_search? | Required | Stop if absent |
| web_fetch? | Required for DEEP tasks | SCAN-only if absent |
| Filesystem writable? | Notes to files | Notes to conversation context |

Mode selection (first matching rule):
- Lightweight: query < 30 words AND single entity/concept
- Standard: multi-entity comparison, historical analysis, or user says "深入"/"comprehensive"
- Default: Standard

Status: `[P0 complete] Subagent: {yes/no}. Mode: {standard/lightweight}. {N} tasks planned.`

---

## P1: Research Task Board

The lead agent breaks the research question into 4-6 investigation tasks.
Each task is a complete assignment for one subagent.

### Task Board Format

```
# Research Task Board
Topic: {research question}
Mode: Standard
Subagent: Yes

## Group A (parallel — no dependencies)

### Task A: {Expert Role Name}
Objective: {one-sentence investigation goal}
Queries:
  - "{search_query_1}"
  - "{search_query_2}"
Depth: DEEP
Output: workspace/research-notes/task-a.md

### Task B: {Expert Role Name}
...

## Group B (depends on Group A)

### Task D: {Expert Role Name}
Objective: {synthesis/comparison that needs Group A data}
Queries: ...
Reads: task-a.md, task-b.md (for cross-reference)
Output: workspace/research-notes/task-d.md
```

### Task Decomposition Rules

1. Each task covers one coherent sub-topic that a specialist would own
2. Tasks in Group A must be independent — no cross-references needed
3. Group B tasks can read Group A notes for comparative analysis
4. Max 3 tasks per parallel group (ref: DeerFlow concurrency limit)
5. Standard mode: 5-6 tasks total. Lightweight: 3-4 tasks.
6. Every task gets 2 pre-planned search queries (lead agent designs these)
7. Mark DEEP (fetch full articles) or SCAN (snippets sufficient)

### Role Assignment

| Topic type | Typical roles |
|-----------|---------------|
| Historical comparison | Period Expert per era, Comparative Analyst |
| Technology survey | Architecture Analyst, Ecosystem Mapper, Benchmark Reviewer |
| Competitive analysis | Per-player Researcher, SWOT Synthesizer |
| Policy analysis | Policy Historian, Stakeholder Mapper, Impact Assessor |
| Scientific review | Methodology Reviewer, Evidence Mapper, Debate Analyst |

Status: `[P1 complete] {N} tasks in {M} groups. Dispatching Group A.`

---

## P2: Dispatch + Investigate

### With subagents (Claude Code / Cowork / DeerFlow)

1. For each task, construct the subagent prompt using `reference/subagent-prompt.md` template
2. Dispatch Group A tasks in parallel (max 3 concurrent)
3. Each subagent independently: searches, fetches, writes task-{id}.md
4. Wait for Group A completion
5. Dispatch Group B (can read Group A notes)
6. Report completion per task

**Subagent prompt:** See `reference/subagent-prompt.md` for the exact template.
**Notes format:** See `reference/research-notes-format.md` for the file structure.

Each subagent's output file must contain:
- Sources section (with URLs from actual search results)
- Findings section (max 15 one-sentence facts with source numbers)
- Leads Discovered section (named entities worth follow-up)
- Deep Read Notes (for DEEP tasks: 2-3 sources read in full)
- Gaps section (what could not be found)

**Iterative Deepening (CRITICAL):**
Subagents MUST chase leads. When initial searches reveal a specific named
entity (product, trial, system, dataset, regulatory approval), the subagent
runs additional targeted searches on that entity. This is the difference
between surface coverage and genuine depth.

Tool budget per subagent:
- DEEP task: 4-8 searches + 2-4 web_fetch
- SCAN task: 2-4 searches + 0-1 web_fetch

### Without subagents (Claude.ai degraded mode)

Lead agent executes each task sequentially, acting as each specialist in turn.

```
For each task in the task board:
  1. Adopt the expert role mentally
  2. Run the pre-planned searches (web_search)
  3. For DEEP tasks: web_fetch top 2-3 results
  4. CHASE LEADS: if you find a named product/trial/system, do 1-2 extra
     targeted searches on it before moving on
  5. Write findings in notes format (visible in conversation)
  6. Move to next task

After ALL tasks complete, proceed to P3.
```

The notes format is identical to the subagent version. The only difference
is that notes appear in conversation context instead of files.

**Critical rule for degraded mode:** After writing a task's notes, mentally
treat the raw search results as discarded. In P5, reference ONLY the notes
content. This simulates the context isolation that subagents provide natively.

Status per task: `[P2 task-{id} complete] {N} sources, {M} findings. {topic} covered.`
Status all: `[P2 complete] {N} tasks done, {M} total sources. Scanning for leads.`

---

## P2.5: Gap-Filling Dispatch (Lead Reads Notes, Chases Leads)

This is the step that separates good research from great research.
After ALL initial tasks complete, the lead agent reads all task notes
and looks for two things:

### 1. Leads Discovered (from subagent notes)

Each subagent's `## Leads Discovered` section contains named entities
they encountered but did not fully investigate. The lead agent collects
all leads across all tasks and decides which are worth pursuing.

**Decision rule:** A lead is worth a follow-up subagent if:
- It's a specific named product/trial/system/regulation (not vague)
- It appears in 2+ tasks' leads (multiple signals)
- OR it sounds like a potential breakthrough (FDA approval, landmark RCT, etc.)
- AND it's not already covered deeply in an existing task's findings

### 2. Cross-task gaps

Read all `## Gaps` sections. If multiple tasks flag the same gap
(e.g., "no data on pediatric patients"), that's a signal for a
targeted follow-up.

### Action: Dispatch 1-3 follow-up subagents

```
For each high-value lead or gap:
  1. Create a SCAN-depth task with 2-3 targeted queries
  2. Dispatch as subagent (or execute sequentially in degraded mode)
  3. The follow-up subagent writes to task-f1.md, task-f2.md, etc.
```

**Budget:** Max 3 follow-up subagents. Each gets 2-4 searches + 1 fetch.
Total additional tool budget: 6-15 calls.

**Skip condition:** If no leads were flagged and no cross-task gaps
overlap, skip P2.5 entirely and proceed to P3.

### Example

```
Initial tasks found:
  task-a leads: "Glean™ System — FDA approved wireless bladder sensor"
  task-b leads: "FUTURE trial — Lancet 2025 RCT on non-invasive vs invasive"
  task-c leads: None
  task-d leads: "Glean™" (also mentioned)

Lead triage:
  Glean™: mentioned in task-a AND task-d → HIGH priority, dispatch follow-up
  FUTURE trial: mentioned in task-b → sounds like landmark RCT → dispatch follow-up

Follow-up dispatch:
  task-f1: [Device Specialist] "Glean urodynamics FDA Cleveland Clinic wireless"
  task-f2: [Trial Analyst] "FUTURE trial Lancet 2025 urodynamics results"
```

Status: `[P2.5 complete] {N} leads triaged, {M} follow-ups dispatched. Proceeding to registry.`
Status (skip): `[P2.5 skipped] No actionable leads. Proceeding to registry.`

---

## P3: Citation Registry

Lead agent reads all task-{id}.md files and builds a unified registry.

### Process

1. Read every task file's `## Sources` section
2. Merge all sources into one list
3. Deduplicate: if two tasks found the same URL, keep once with higher authority
4. Assign final [n] numbers (sequential, by first appearance across tasks)
5. Drop sources below authority threshold (< 5 for Standard, < 4 for Lightweight)
6. Check diversity: unique domains >= 5, no single domain > 25%
7. Write registry.md (or output visible registry)

### Registry Output (MANDATORY — visible to user)

```
CITATION REGISTRY

Approved:
[1] National Geographic — Luddites | https://... | Auth: 8 | task-a
[2] Cambridge — Rage against machine | https://... | Auth: 8 | task-a
[3] Microsoft — Day Horse Lost Job | https://... | Auth: 8 | task-b
...

Dropped:
x Quora answer | Auth: 3 | Reason: below threshold
x Study.com | Auth: 4 | Reason: superseded by better sources

Stats: {approved}/{total evaluated}, {N} unique domains, diversity {pass/fail}
```

### Registry Enforcement (carried from V4)

- These [n] numbers are FINAL through P5/P7/P8
- P5 may ONLY cite [n] from the Approved list
- Dropped sources must NEVER reappear
- If P5 needs a source not in registry, mark `[source needed]` for P6

Status: `[P3 complete] {approved}/{total} sources. {N} domains. Diversity: {pass/fail}.`

---

## P4: Outline

Lead agent reads notes + registry to build an evidence-mapped outline.

### Process

1. Identify cross-task patterns (e.g., "all three historical cases show X")
2. Design report sections that follow logical flow, not task order
3. Map each section to specific findings from specific tasks
4. Identify gaps: sections with < 2 source support need flagging

### Outline Format (MANDATORY visible output)

```
## 1. {Section Title}
Sources: [1][3][7] from tasks a, b
Claims: {claim from task-a finding 3}, {claim from task-b finding 1}

## 2. {Section Title}
Sources: [4][5][8] from tasks b, c
Claims: ...

Gaps: {section N has only 1 source — flag in P6}
```

### Flexible Section Design

Adapt to topic type. Do NOT use fixed templates. See report-assembly.md
for topic-specific section recommendations.

Status: `[P4 complete] {N} sections, {M} sources mapped. Gaps: {none/list}.`

---

## P5: Draft

Write the report section by section. Every claim must trace to notes.

### Rules

1. Write body sections in outline order, Executive Summary LAST
2. Per section: re-read the mapped task notes, then write
3. Every factual claim gets a citation [n] from the registry
4. Every [n] must exist in the P3 Approved list
5. No new sources may be introduced (flag as `[source needed]` for P6)
6. End each section with confidence marker: High/Medium/Low + reason
7. Standard: 500-1000 words per section. Lightweight: 300-600.

### Citation Discipline

Good: `The transition took approximately 50 years (1760s-1850s) [4].`
(Source [4] is in registry, claim matches task-a finding about timeline)

Bad: `Studies show the transition was lengthy [4].`
(Vague, and need to verify [4] actually says this in the task notes)

Forbidden: `According to a 2024 study, AI affects 80% of jobs [17].`
(If [17] doesn't exist in registry, this is a hallucination)

Status: `[P5 in progress] {done}/{total} sections, ~{words} words.`
Status: `[P5 complete] {N} sections, ~{words} words, {M} sources cited.`

---

## P6: Critique

Systematically audit the draft against the task notes.

### Mandatory checks (must find 3+ issues)

1. **Notes traceability:** For each specific claim, can you point to the
   task note finding it came from? Flag any untraceable claims.
2. **Registry compliance:** Any [n] not in the Approved list? Any dropped source?
3. **Gap acknowledgment:** Any task's Gaps section raised something the report
   claims to cover confidently?
4. **Balance:** Any section relying on a single task's findings?
5. **Hallucination scan:** Any numbers/dates not in any task note?

### Output (must be visible)

```
Critique:
1. Section 3 claims "690M net new jobs" — verified in task-b finding 4. OK.
2. Section 4 states "AI affects 80% of workforce" — NOT in any task note. REMOVE or mark [unverified].
3. Section 2 relies entirely on task-b — need cross-reference with task-a.
4. [Minor] Section 5 confidence should be Medium, not High — task-d gaps section noted missing data.
```

Status: `[P6 complete] {N} issues found: {critical} critical, {minor} minor.`

---

## P7: Verify

### Step 0: Registry cross-check

List every [n] in the report. Compare to registry. Any violations = critical.

### Step 1: Notes traceability spot-check (5 claims minimum)

Pick 5 specific claims from the report and trace each to its task note origin:

```
Spot-check:
[1] "Luddites began March 11, 1811 in Arnold" → task-a finding 1, source [3]. Match.
[2] "690M net new jobs in auto industry" → task-b finding 3, source [3]. Match.
[3] "Operators dropped 50-80% after cutover" → task-c finding 2, source [1]. Match.
[4] "AI affects 80% of workforce" → NOT FOUND in any task note. VIOLATION.
[5] "AI transition may take 10-20 years" → task-d finding 4, source [2]. Match.
Result: 4/5 pass. 1 violation fixed.
```

### Step 2: Fix protocol

- Claim not in notes → REMOVE or mark [unverified]
- [n] not in registry → REMOVE citation
- Dropped source cited → REMOVE immediately

Status: `[P7 complete] {N} spot-checks, {M} violations fixed.`

---

## P8: Polish

1. Write Executive Summary (now that body is final)
2. Format references from registry (numbered, with full URLs)
3. Add metadata: date, source count, word count, mode
4. Consistency pass: terminology, tone, citation format
5. Save report file

Status: `[DONE] ~{N} words, {M} sources, {K} citations. Mode: {mode}.`
