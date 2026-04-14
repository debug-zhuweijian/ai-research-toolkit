---
name: paper-proofread
description: LaTeX 论文审校：两阶段工作流，先检测所有问题再选择性修复。基于 ICRA/CVPR 级审稿标准。
---

# Paper Proofreading (LaTeX)

Two-phase LaTeX paper proofreading system based on real conference review standards (ICRA, RSS, CVPR, NeurIPS, RA-L, T-RO).

Source: [awesome-claudecode-paper-proofreading](https://github.com/LimHyungTae/awesome-claudecode-paper-proofreading) by Hyungtae Lim (ICRA 2025 Outstanding Reviewer).

## When To Use

Invoke when the user asks to:
- proofread a LaTeX paper
- check LaTeX workspace for submission errors
- review paper before conference submission
- audit LaTeX preamble, references, labels, figures
- find grammar/notation/claim issues in a paper

## Required Input

Ask the user for:
1. **Root `.tex` file** (e.g., `main.tex`) — mandatory
2. **Compiled PDF** (optional, for content proofreading pass)
3. **Mode selection** (ask if unclear):
   - `workspace` — LaTeX infrastructure audit only
   - `content` — paper content proofreading only
   - `full` — workspace audit first, then content proofreading (recommended before submission)

## File Reading Protocol

Before running any checks, **silently** read the full workspace:

1. Read the root `.tex` file
2. Resolve every `\input{...}` and `\include{...}` recursively
3. Read shared preamble/macro files: `shortcuts.tex`, `macros.tex`, `commands.tex`, `preamble.tex`
4. Read every referenced `.bib` file
5. Check referenced figures for missing assets (workspace mode)
6. If PDF is provided, use it for figure placement and leftover annotations (content mode)

**Never review only the top-level file** unless the user explicitly narrows scope.

## Two-Phase Protocol

### Phase 1: Detection Only

**CRITICAL: Do NOT modify any files in Phase 1.**

- Report all findings with unique IDs: `[1]`, `[2]`, `[3]`...
- For each finding include: severity, location (file + line), diagnosis, impact, fix direction
- Severity levels: `CRITICAL` | `MAJOR` | `MINOR` | `STYLE`
- If nothing is wrong, say so clearly

After Phase 1 output, **stop and wait** for user decision.

### Phase 2: Approved Fixes Only

Only edit files after explicit user approval such as:
- `fix safe` — typos, duplicate words, clear grammar errors only
- `fix all critical` — CRITICAL issues only
- `fix 1, 3, 5` — specific issue numbers
- `fix all` — everything
- `discard 3, 7` — skip specific issues

When fixing:
- Apply only approved fixes
- Keep edits minimal and localized
- Preserve meaning, notation, and LaTeX structure
- Do NOT silently fix unapproved neighboring issues

## Workspace Audit Checklist

Run these checks in `workspace` or `full` mode:

### C1 — Preamble Configuration
- Duplicate/conflicting/unused/missing packages
- `cleveref` setup: `[nameinlink,capitalize]` options
- `hyperref` setup: `colorlinks=true, allcolors=blue`
- `caption` setup: consistent `font=footnotesize` and label format
- Math packages: `amsmath`, `mathtools`, `bm`
- Algorithm environment conflicts

### C2 — Package Load Order
- `hyperref` before `cleveref`
- `amsmath` before `mathtools`
- `xcolor` before `tikz`
- `caption` before `subcaption`
- Flag `subfig` + `subcaption` conflict, `epsfig` redundancy

### C3 — Macro Safety & Naming Consistency
- `\methodname`, `\ours` defined exactly once, used consistently
- No hardcoded method names alongside macros
- `\xspace` on text-mode macros
- `\etalcite` defined and used correctly
- Subscript consistency: `_{\text{pred}}` appearing 3+ times should be a macro

### C4 — Cross-Reference Consistency
- `\Cref{}` vs `\ref{}` vs hardcoded `Fig.` — standardize
- Multi-reference grouping: `\Cref{fig:a,fig:b}` not `\Cref{fig:a} and \Cref{fig:b}`
- Subfigure format: `Fig. 1(a)` not `Fig. 1a`
- `\renewcommand\thesubfigure{(\alph{subfigure})}` present

### C5 — Label Naming Convention
- Consistent prefixes: `fig:`, `tab:`, `eq:`, `sec:`, `alg:`, `app:`
- No duplicate labels
- No unreferenced labels
- No dangling `\ref{}` calls

### C6 — Citation & Bibliography
- Cited keys missing from `.bib`
- Unused `.bib` entries
- Duplicate BibTeX keys across files
- arXiv formatting inconsistency
- Missing required fields
- Non-breaking space `~` before `\cite{}`

### C7 — Figure & Table Safety
- Missing figure files referenced in `\includegraphics{}`
- Dummy/placeholder figures
- Absolute paths in `\includegraphics`
- Label placement (inside `\caption{}` or before it, not after)
- Unreferenced figures/tables
- Missing size specifications

### C8 — Hidden Human Errors
- `TODO`, `XXX`, `FIXME`, `TBD`, `???`, `[CITE]`, `[REF]`, `[FILL]`
- Inconsistent method/dataset/metric naming capitalization
- Default template content not replaced
- Double spaces, missing `~` before `\cite`/`\ref`
- Excessive `\vspace{-Xmm}` hacks

### C9 — Academic Writing (LaTeX-Detectable)
- Unit formatting: `10\,cm` not `10cm`
- Number formatting: `10,000` not `10000`
- `\ie`/`\eg` macros used instead of bare `i.e.`/`e.g.`
- `state-of-the-art` hyphenation consistency
- Acronym first-use expansion
- Sentence-level patterns: starting with "And", "But", "Or"

## Content Proofreading Checklist

Run these checks in `content` or `full` mode:

### A — Language & Grammar
- Grammar errors (subject-verb agreement, articles, prepositions)
- Tense inconsistency (present for facts, past for experiments)
- Related Work tense: present preferred, flag mixing
- Coordinating conjunction sentence starters
- Missing Oxford comma, comma splices

### B — Language Quality
- Typos and spelling errors → **CRITICAL**
- Duplicate words ("the the") → **CRITICAL**
- Nominalization: prefer direct verbs over noun-heavy phrasing
- Redundant expressions: "In order to" → "To", "due to the fact that" → "because"
- Citation-as-noun: use `Author~\etalcite{#}` not bare `[3]` as subject
- Circular descriptions

### C — Scientific Clarity & Claims
- Overclaiming: every "significantly" needs a statistical test
- "outperform"/"superior"/"state-of-the-art" — verify across all metrics
- Causal logic gaps
- Variables used before definition
- Claims in figure captions
- "Only a few works..." contradicted by long citation list

### D — Structure & Flow
- Introduction has dedicated contribution paragraph
- Related Work is standalone section (not merged into intro)
- Related Work cites 15-25 papers for 6-8 page conference paper
- Related Work includes at least one comparison to this work
- Equations not re-explained in ablation (use cross-reference)
- Every experiment opens with WHY/WHAT/HOW statement
- No verbatim copy of contribution list from intro to conclusion

### E — Figure, Table & Caption Review
- Captions are self-contained (abbreviations defined, baselines cited)
- Caption grammatical completeness
- Font size consistency in figures vs caption
- Thousand separators in axis tick labels
- Bold/underline convention for best values defined in caption
- Quantitative consistency: text numbers match table/figure data → **CRITICAL if mismatch**
- Figure/table reference order is sequential

### F — LaTeX Formatting
- Thin space before units: `5\,m`
- Thousand separators for integers ≥ 1000
- Consistent figure reference style
- `\ie`/`\eg` macros, not bare text
- `et al.` with period
- Non-breaking space before `\cite`/`\ref`

### G — Abstract & Conclusion
- Abstract follows WHY → PROBLEM → HOW → RESULTS
- Acronyms expanded in abstract
- No citations in abstract → **CRITICAL**
- Single paragraph abstract
- Conclusion not verbatim restatement of abstract
- Future work is specific, not vague

### H — Notation Consistency
- Symbol overload detection (same letter, different meanings)
- Different symbols for same concept across sections
- Vector/matrix boldface consistency (`\mathbf{}`)
- Coordinate frame notation consistency
- Term capitalization consistency

### I — Hyphenation
- Compound adjective before noun: hyphenate ("real-time system")
- Adverb (-ly) + adjective: NEVER hyphenate ("tightly coupled" not "tightly-coupled")
- Common errors: "end-to-end", "state-of-the-art" as adjective

## Output Format

### Workspace Audit Output

```
## LaTeX Workspace Audit Results

**Files inspected**: [list all files read]
**Total issues**: N

### Issues by File

**`main.tex`**
[1]  L.53   Description | Fix direction

**`shortcuts.tex`**
[2]  L.14   Description | Fix direction

### Issues by Severity

CRITICAL
  [N]  File — summary

MAJOR
  [N]  File — summary

MINOR
  [N]  File — summary

STYLE
  [N]  File — summary
```

### Content Proofreading Output

```
## Paper Proofreading Results

Paper quality: GOOD / NEEDS REVISION / MAJOR REVISION

| Type     | Count |
|----------|-------|
| CRITICAL |       |
| MAJOR    |       |
| MINOR    |       |
| STYLE    |       |

Most common problems:
- ...

### Issues by File
[Same format as workspace audit]

### Caption Review
| # | Figure/Table | Issue | Suggestion |

### Formatting Patterns
| # | Pattern | Example | Fix |
```

### Phase 1 Complete Message

After outputting all findings, always end with:

```
---
**Phase 1 complete.** All issues listed above with numbers [1], [2], [3]...

Reply with one of:
- `fix safe` — typos and clear grammar errors only
- `fix all critical` — CRITICAL issues only
- `fix 1, 3, 5` — specific issue numbers
- `fix all` — all issues
- `discard 3, 7` — skip specific issues

**No files will be modified until you confirm.**
```

## Editing Constraints

When applying fixes in Phase 2:
- No em dashes in rewritten prose
- Prefer precise wording over vague intensifiers
- Do not change scientific claims unless user explicitly asks
- Preserve LaTeX structure, labels, and macros
