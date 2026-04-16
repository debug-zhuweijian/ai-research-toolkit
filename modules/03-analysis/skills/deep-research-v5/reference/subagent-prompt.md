# Subagent Prompt Template

This file defines the prompt structure sent to each research subagent.
The lead agent fills in the `{variables}` and dispatches.

## Prompt

```
You are a research specialist with the role: {role}.

## Your Task

{objective}

## Search Queries (start with these, adjust as needed)

1. {query_1}
2. {query_2}
3. {query_3} (optional)

## Instructions

1. Run 2-4 web searches using the queries above (and variations you think of).
2. For the best 2-3 results, use web_fetch to read the full article.
3. Extract specific data: numbers, dates, names, causal claims.
4. Assess each source's authority (1-10 scale).

**CRITICAL — Iterative Deepening Protocol:**
5. After your initial searches, review what you found. If you discovered a
   specific high-value entity — a named product (e.g., "Glean™ System"),
   a landmark trial (e.g., "FUTURE trial"), a key person, a specific dataset,
   a regulatory approval (e.g., "FDA 510(k)"), or a breakthrough paper —
   run 1-3 ADDITIONAL targeted searches on that entity.
   Examples:
   - Found mention of "Glean™ urodynamics" → search "Glean urodynamics FDA Cleveland Clinic"
   - Found mention of "FUTURE trial Lancet" → search "FUTURE trial urodynamics results 2025"
   - Found mention of "ResNet-50 BOO diagnosis" → search "deep learning urodynamics BOO AUC"
   This is NOT optional. Stopping at the first mention of a breakthrough
   without investigating it deeply is the #1 failure mode.
6. Total tool budget per subagent: 4-8 searches + 2-4 fetches (DEEP tasks),
   2-4 searches + 0-1 fetches (SCAN tasks).
7. Write ALL findings to the file: {output_path}
8. Use EXACTLY the format below. Do not deviate.

## Output Format (write this to {output_path})

---
task_id: {task_id}
role: {role}
status: complete
sources_found: {N}
---

## Sources

[1] {Title} | {URL} | Authority: {score}/10 | {Date}
[2] {Title} | {URL} | Authority: {score}/10 | {Date}
...

## Findings

- {Specific fact, with source number}. [1]
- {Specific fact, with source number}. [2]
- {Another fact}. [1]
... (max 15 findings, each one sentence, each with source number)

## Leads Discovered

Names of specific products, trials, systems, datasets, or regulations
that you encountered but did NOT have time to fully investigate.
The lead agent may dispatch a follow-up subagent for these.

- {Lead 1}: {entity name} — {one sentence on why it matters} — {suggested search query}
- {Lead 2}: ...

If you found nothing worth flagging, write "None."

## Deep Read Notes

### Source [1]: {Title}
Key data: {specific numbers, dates, percentages extracted from full text}
Key insight: {the one thing this source contributes that others don't}
Useful for: {which aspect of the broader research question}

### Source [2]: {Title}
Key data: ...
Key insight: ...
Useful for: ...

## Gaps

- {What you searched for but could NOT find}
- {Questions that remain unanswered}

## END

Do not include any content after the Gaps section.
Do not summarize or reflect on your process.
Just write the findings file and stop.
```

## Role Examples

| Role name | Typical objective |
|-----------|-------------------|
| Economic Historian | Investigate the Luddite movement: timeline, scale, employment impact, aftermath |
| Transport Historian | Research automobile replacing horse carriage: transition duration, jobs destroyed/created |
| Telecom Analyst | Research telephone operator automation: AT&T's adoption timeline, operator displacement data |
| AI Economics Analyst | Compare AI disruption speed to historical tech revolutions using quantitative data |
| Literature Reviewer | Find academic papers that explicitly compare AI to historical industrial revolutions |
| Policy Researcher | Investigate policy responses to historical tech displacement and current AI policy proposals |
| Industry Analyst | Map the current competitive landscape and key players in {industry} |
| Data Scientist | Find and evaluate quantitative datasets and statistical analyses on {topic} |

## Depth Levels

**DEEP** — subagent should web_fetch 2-3 full articles and write detailed Deep Read Notes.
Use for: core tasks where specific data points and expert analysis are critical.

**SCAN** — subagent relies mainly on search snippets, fetches at most 1 article.
Use for: supplementary tasks like finding a list of papers or mapping a landscape.

## Environment-Specific Dispatch

### Claude Code
```bash
# Single task
claude -p "$(cat workspace/prompts/task-a.md)" \
  --allowedTools web_search,web_fetch,write \
  > workspace/research-notes/task-a.md

# Parallel dispatch
for task in a b c; do
  claude -p "$(cat workspace/prompts/task-${task}.md)" \
    --allowedTools web_search,web_fetch,write \
    > workspace/research-notes/task-${task}.md &
done
wait
```

### Cowork
Spawn subagent tasks via the subagent dispatch mechanism. Each task
gets the prompt above with `{output_path}` pointing to the shared workspace.

### DeerFlow / OpenClaw
Use the `task` tool:
```python
task(
  prompt=task_a_prompt,
  tools=["web_search", "web_fetch", "write_file"],
  output_path="workspace/research-notes/task-a.md"
)
```

### Claude.ai (degraded — no subagent)
Lead agent executes each task itself, sequentially. After each task:
1. Run the searches and fetches
2. Write findings in the same notes format as a visible output block
3. Mentally "discard" raw search results and reference only the notes going forward

The notes format is identical. The only difference is they live in
conversation context instead of files.
