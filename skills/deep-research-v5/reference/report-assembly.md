# Report Assembly V5 — Draft from Notes

## Core Rule

The report is written from task notes and the citation registry.
The lead agent never references raw search results — only the distilled
findings in `task-{id}.md` files and the approved sources in `registry.md`.

## Section Design

Adapt to topic type. Do NOT use a fixed template.

| Topic Type | Recommended Sections |
|------------|---------------------|
| Historical comparison | Background per case, Cross-case patterns, Modern parallel, Speed analysis |
| Technology survey | Background, Architecture, Key features, Ecosystem, Comparison, Outlook |
| Competitive analysis | Market overview, Player profiles, Comparison matrix, Strategic insights |
| Policy analysis | Context, Current framework, Stakeholder views, Impact, Recommendations |
| Scientific review | Background, Methods landscape, Evidence, Debates, Open questions |

Rename sections to be topic-specific. "Core Mechanism" for a DeerFlow report,
"Displacement patterns" for a labor history report.

## Generation Order

1. Body sections (in outline order from P4)
2. Key Findings (synthesize from body)
3. Limitations (what wasn't covered — draw from task Gaps sections)
4. Executive Summary (compress whole report)
5. References (from registry)
6. Metadata header

Never write the summary first.

## Per-Section Protocol

```
For each section:
  1. Re-read mapped task notes for this section (from P4 outline)
  2. Write section (Standard: 500-1000 words, Lightweight: 300-600)
  3. Insert [n] citations — ONLY from registry Approved list
  4. Checkpoint: any uncited factual claims? Any [n] not in registry?
  5. Add confidence marker
  6. Next section
```

## Citation Rules

- [n] numbers from P3 registry are final — no renumbering
- Each source gets one [n], reuse for multiple citations
- Sequential order not required (registry order is the order)
- Cross-check: every [n] in text has matching entry in References
- Every References entry is cited at least once

## Final Report Structure

```markdown
# {Title}

> Date: YYYY-MM-DD | Sources: N | Words: ~XXXX | Mode: Standard/Lightweight

## Executive Summary
{200-400 words, written LAST}

## {Section 1 — topic-specific title}
{content with [n] citations}
Confidence: High/Medium/Low — {reason}

## {Section 2}
...

## Key Findings
- Finding 1 [n][m]
- Finding 2 [n]
...

## Limitations
- {from task Gaps sections}
- {methodological limitations}

## References
[1] Author/Org. Title. URL. Accessed YYYY-MM-DD.
[2] ...
```

## Limitations Section Best Practice

Draw directly from subagent Gaps sections. Each task's gaps tell you
what the research couldn't find. Honest limitations build credibility.

```
Example:
- No Chinese-language academic sources found for the Luddite period (task-a gap)
- Quantitative AI job displacement projections vary widely across studies (task-d gap)
- Limited to web-accessible sources; paywalled academic journals not accessible
```
