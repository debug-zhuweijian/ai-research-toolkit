---
name: paper-review
description: 研究论文分析、评审与方法论检查
---
# Paper Review

## Overview

Use this skill to turn a paper into research-ready notes instead of a vague summary. Focus on the research question, method, experimental design, evidence quality, limitations, and what the user can reuse in their own work.

Use the local document skills when the source is a file:
- For PDFs, use the existing `document-skills/pdf` workflow to extract text and tables as needed.
- For PPTX or DOCX supplements, use the sibling `pptx` or `docx` skills when the paper package includes slides, appendices, or reviews in those formats.

## When To Use

Use this skill when the user asks for any of the following:
- Read and explain a paper PDF
- Summarize a paper for study, literature tracking, or group meeting
- Extract the method, model, theorem, dataset, or experiment design from a paper
- Judge whether a paper is strong, weak, reproducible, or useful for a thesis/project
- Compare a target paper against the user's current direction, baseline, or idea

Do not use this skill for broad multi-paper synthesis. Use `literature-review` for that.

## Workflow

### 1. Identify the paper context

Establish the minimum context before analyzing:
- Title
- Venue, year, and version if available
- Research area
- User goal

If the user provides a PDF only, infer the topic from the title, abstract, introduction, and figures before going deeper.

### 2. Read in a research order

Read the paper in this order unless the user asks otherwise:
1. Title and abstract
2. Introduction and stated problem
3. Figures, tables, and captions
4. Method section
5. Experimental setup and datasets
6. Results and ablations
7. Conclusion and limitations
8. Related work only if needed for context

Avoid pretending every section deserves equal weight. Spend more attention on the method and evidence.

### 3. Extract the paper's core claims

State the following explicitly:
- What problem is being solved
- Why prior approaches are insufficient
- What the paper claims is new
- What exact mechanism or idea produces the claimed benefit
- What evidence supports the claim

Distinguish between:
- The authors' claim
- Evidence directly shown in the paper
- Your own inference

### 4. Evaluate method quality

For the method, explain:
- Inputs and outputs
- Main architecture, algorithm, or derivation
- Training or optimization strategy
- Assumptions and prerequisites
- What is simple engineering versus what is actually novel

If equations appear central, explain them in plain language first. Only reproduce notation when it helps comprehension.

### 5. Evaluate experiment quality

Check these points explicitly:
- Datasets and benchmarks are appropriate
- Baselines are strong and current enough
- Metrics match the task
- Ablations isolate the claimed contribution
- Improvements are practically meaningful, not only statistically present
- Reproducibility signals exist

Call out missing evidence rather than smoothing over it.

### 6. Translate to the user's research context

Always connect the paper to likely downstream use:
- What idea is reusable
- What part is hard to reproduce
- What assumptions may fail in another domain
- What would be worth implementing first
- Whether the paper is a core reference, supporting reference, or probably skippable

## Output Format

Default to this structure unless the user asks for something else:

```markdown
# Paper Review

## Citation
- Title:
- Authors:
- Venue / Year:
- Link or file:

## One-Sentence Take
- 

## Problem
- 

## Main Contribution
- 

## Method
- 

## Experimental Evidence
- 

## Strengths
- 

## Weaknesses / Threats to Validity
- 

## Reproducibility Notes
- 

## What To Reuse
- 

## Recommendation
- Read closely / cite / implement / skip
```

## Short-Form Variant

If the user asks for a quick read, compress to:
- one-sentence contribution
- three key ideas
- two main limitations
- one action recommendation

## Guardrails

- Do not confuse the abstract's promises with demonstrated evidence.
- Do not call a paper "state of the art" unless the paper clearly supports that claim.
- Do not over-explain related work if the user's goal is implementation or decision-making.
- Do not hide uncertainty. If the PDF extraction is messy or equations are unreadable, say so.
- Do not produce marketing language. Produce research notes.
