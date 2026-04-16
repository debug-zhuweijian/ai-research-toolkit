---
name: paper-proofread
description: LaTeX 论文审校：两阶段工作流，先检测所有问题再选择性修复。基于 ICRA/CVPR 级审稿标准。
---

# Paper Proofreading (LaTeX)

Two-phase LaTeX paper proofreading system based on real conference review standards (ICRA, RSS, CVPR, NeurIPS, RA-L, T-RO).

Source: [awesome-claudecode-paper-proofreading](https://github.com/LimHyungTae/awesome-claudecode-paper-proofreading) by Hyungtae Lim (ICRA 2025 Outstanding Reviewer).

## CRITICAL: Read Reference Files Before Execution

This skill has TWO reference files containing the detailed review rules with ✅/❌ judgment examples.
**You MUST read both files before running any checks.** The bullet points below are summaries only — the reference files contain the actual judgment criteria.

```
Read these files FIRST:
- references/01_latex_workspace_review.md  (for workspace/full mode)
- references/02_paper_proofreading.md      (for content/full mode)
```

If the reference files are missing, tell the user that the full review instructions are unavailable rather than proceeding with only the summaries in this file.

## When To Use

Invoke when the user asks to:
- proofread a LaTeX paper
- check LaTeX workspace for submission errors
- review paper before conference submission
- audit LaTeX preamble, references, labels, figures
- find grammar/notation/claim issues in a paper

## Mode Selection

Ask the user for mode if not specified:

| Mode | Scope | When |
|------|-------|------|
| `workspace` | LaTeX infrastructure audit (C1-C9) | Preamble, packages, macros, refs, labels, figures |
| `content` | Paper content proofreading (A-I) | Grammar, claims, structure, notation, captions |
| `full` | Workspace first, then content | **Recommended before submission** |

## Required Input

1. **Root `.tex` file** (e.g., `main.tex`) — mandatory
2. **Compiled PDF** (optional, for content mode — enables figure placement + leftover annotation checks)
3. If mode is unclear, **ask**.

## File Reading Protocol

Before running any checks, **silently** read the full workspace:

1. Read the root `.tex` file
2. Resolve every `\input{...}` and `\include{...}` recursively
3. Read shared preamble/macro files: `shortcuts.tex`, `macros.tex`, `commands.tex`, `preamble.tex`
4. Read shared symbol files: `preamble_symbols.tex`, `preamble_packages.tex` (in `../references/` if workspace uses shared folder)
5. Read every referenced `.bib` file
6. Check `figures/` directory for missing assets (workspace mode)
7. Distinguish `figures/` (final manuscript figures) from `pics/` (raw sources — do NOT flag for missing .tex references)
8. If PDF is provided, use it for figure placement and leftover annotations (content mode)

**Never review only the top-level file** unless the user explicitly narrows scope.

## Two-Phase Protocol

### Phase 1: Detection Only

**CRITICAL: Do NOT modify any files in Phase 1. Do NOT rewrite paragraphs. Do NOT apply style changes proactively.**

- Report all findings with unique IDs: `[1]`, `[2]`, `[3]`...
- For each finding include: severity, location (file + line), diagnosis, why it matters, actionable fix direction
- Severity levels: `CRITICAL` | `MAJOR` | `MINOR` | `STYLE`
- If nothing is wrong, say so clearly and mention remaining limits (missing PDF, missing bib files, etc.)

After Phase 1 output, **stop and wait** for user decision.

### Phase 2: Approved Fixes Only

Only edit files after explicit user approval:

| Command | Action |
|---------|--------|
| `fix safe` | Only definite typos, duplicate words, clear grammar errors |
| `fix all critical` | Only CRITICAL issues |
| `fix 1, 3, 5` | Specific issue numbers |
| `fix all` | All issues |
| `discard 3, 7` | Skip specific issues |

When fixing:
- Apply **only** approved fixes
- Keep edits minimal and localized
- Preserve meaning, notation, and LaTeX structure
- Do NOT silently fix unapproved neighboring issues
- After edits, summarize what changed and note anything intentionally left untouched

## Editing Constraints

When applying fixes in Phase 2:
- **No em dashes** (`—`) in rewritten prose — use comma, colon, semicolon, or restructure
- Prefer precise, concrete wording over vague intensifiers
- Do not change scientific claims unless user explicitly asks
- Preserve LaTeX structure, labels, and macros where possible
- Avoid introducing new terminology unless required for consistency

## Workspace Audit Checklist (C1-C9)

> These are summaries. **Read `references/01_latex_workspace_review.md` for full rules with examples.**

### C1 — Preamble Configuration
Duplicate/conflicting/unused/missing packages. cleveref `[nameinlink,capitalize]` options. hyperref colorlinks. caption font consistency. Math packages (`amsmath`, `mathtools`, `bm`). Algorithm environment conflicts.

### C2 — Package Load Order & Conflicts
`hyperref`→`cleveref`. `amsmath`→`mathtools`. `xcolor`→`tikz`. `caption`→`subcaption`. Flag `subfig`+`subcaption` conflict, `epsfig` redundancy, `\usepackage{times}/pslatex`.

### C3 — Macro Safety & Naming Consistency
`\methodname` defined once, used consistently, no hardcoded strings. `\xspace` on text-mode macros. `\etalcite` defined and used with `~` + plural verb. Subscript macros for repeated patterns. Shared symbol conflicts between local and shared preamble files. `\renewcommand` flagged as intentional or accidental.

### C4 — Cross-Reference Consistency
`\Cref{}` standardization. Multi-reference grouping. Subfigure format `5(a)` with `\renewcommand\thesubfigure`. Forward references minimized. `~` spacing before `\Cref{}`.

### C5 — Label Naming Convention
Prefixes: `fig:`, `tab:`, `eq:`, `sec:`, `alg:`, `app:`. No duplicate labels. No unreferenced labels. No dangling `\ref{}` calls.

### C6 — Citation & Bibliography
Cited keys in bib. Unused bib entries. Duplicate BibTeX keys across files. arXiv formatting. Missing required fields. Venue abbreviation consistency. `~` before `\cite{}`.

### C7 — Figure & Table Safety
Missing figure files. Dummy/placeholder figures. Absolute paths. Label placement (inside `\caption{}` or before, NOT after). Unreferenced figures/tables. Missing size specs. `\hline` vs booktabs. Decimal alignment (`siunitx` S columns).

### C8 — Hidden Human Errors
`TODO`, `XXX`, `FIXME`, `TBD`, `???`, `[CITE]`, `[REF]`, `[FILL]`, `\tobeupdated`. Inconsistent method/dataset/metric naming. Default template content. `\journalVersion{}` non-empty. `deprecated/` folder still `\input`-ted. Double spaces. Missing `~`. Hard-coded `\\` in prose. `\vspace{-Xmm}` accumulated total.

### C9 — Academic Writing (LaTeX-Detectable)
Unit formatting (`\,`). Thousand separators. `\ie`/`\eg` macros (define if missing). `state-of-the-art` noun vs adjective. Acronym first-use in abstract AND body separately. Sentences starting with "And", "But", "Or". "etc." in formal prose. Figure reference order vs document position.

## Content Proofreading Checklist (A-I)

> These are summaries. **Read `references/02_paper_proofreading.md` for full rules with examples.**

### A — Language & Grammar
Subject-verb agreement. Articles. Prepositions. Tense consistency (present for facts/contributions, past for experiments). Related Work tense (present preferred; flag only mixing). Oxford comma. Comma splices.

### B — Language Quality & Awkward Expression
Typos/spelling → **CRITICAL**. Duplicate words → **CRITICAL**. Nominalization (prefer direct verbs). Redundant expressions ("In order to"→"To"). Citation-as-noun (use `Author~\etalcite{#}`). Circular descriptions. Verb choice ("suggest"→"propose"/"investigate"/"present").

### C — Scientific Clarity & Claims
Every "significantly" needs statistical test or quantitative alternative. "outperform"/"superior"/"state-of-the-art" verified across all metrics. Causal logic gaps. Variables used before definition. Claims in figure captions. "Only a few works..." contradicted by citation list. Scope-limiting language without justification.

### D — Structure & Flow
**Introduction**: dedicated contribution paragraph. **Related Work**: standalone section (CRITICAL if merged into intro), 15-25 papers for 6-8 page paper, at least one comparison to this work (MAJOR if none). **Method**: equation references with narrative context. **Experiments**: each opens with WHY/WHAT/HOW statement, claim coverage verified, most impressive first. **General**: no repetition across sections, no verbatim intro→conclusion copy, ablation cross-references method section.

### E — Figure, Table & Caption Review
**Captions**: grammatically complete, self-contained (abbreviations defined, baselines cited with `\cite{}`, datasets named), no body text duplication, period at end. **Figures**: font size consistent with caption (`\footnotesize`), tick labels legible, thousand separators in axis ticks, no excessive whitespace. **Tables**: bold/underline convention defined in caption, consistent metric names, units in headers. **Reference order**: sequential ascending. **Quantitative consistency**: text numbers match table/figure data exactly → **CRITICAL if mismatch**.

### F — LaTeX Formatting
Thin space before units (`\,`). Thousand separators for integers ≥1000 (NOT decimals). Consistent figure reference style. `\ie`/`\eg` macros. `et al.` with period. `~` before `\cite`/`\ref`. `state-of-the-art` consistency.

### G — Abstract & Conclusion Quality
**Abstract**: WHY(1-2 sentences)→PROBLEM(1 sentence)→HOW&WHAT(~3 sentences)→RESULTS(1 sentence). Acronyms expanded within abstract. Zero `\cite{}` → **CRITICAL**. Single paragraph → **CRITICAL if broken**. **Conclusion**: not verbatim abstract restatement. Limitations acknowledged. Future work specific with grounding sentence.

### H — Notation Consistency
Symbol overload detection (build symbol table across all equations). Different symbols for same concept. Vector/matrix boldface (`\mathbf{}`). Greek vectors (`\boldsymbol{}`). Coordinate frame notation consistent subscript order. Superscript semantic consistency. Term capitalization consistency.

### I — Hyphenation Consistency
**Rule 1**: Compound adjective before noun → hyphenate (real-time system). **Rule 2**: -ly adverb + adjective → NEVER hyphenate (tightly coupled, NOT tightly-coupled). Common robotics/CV patterns: "end-to-end", "state-of-the-art", "deep learning" (noun phrase, not hyphenated as adjective).

## Output Format

### For Workspace Audit

```
## LaTeX Workspace Audit Results

**Files inspected**: [list all files read]
**Total issues**: N

### Issues by File

**`main.tex`**
[1]  L.53   Description | Impact / Suggested fix

**`shortcuts.tex`**
[2]  L.14   Description | Impact / Suggested fix

### Issues by Severity

CRITICAL
  [N]  File — brief summary

MAJOR
  [N]  File — brief summary

MINOR
  [N]  File — brief summary

STYLE
  [N]  File — brief summary

### Infrastructure Suggestions
[Workspace-level recommendations not tied to a specific file]
```

### For Content Proofreading

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

### LaTeX Formatting Patterns
| # | Pattern | Example Found | Suggested Fix |

### Optional Polishing Suggestions
[High-level structural improvements only]
```

### Phase 1 Complete Message

After outputting ALL findings, always end with:

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
