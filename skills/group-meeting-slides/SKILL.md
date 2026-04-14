---
name: group-meeting-slides
description: 从论文和研究资料准备组会演示幻灯片
---
# Group Meeting Slides

## Overview

Use this skill to transform research content into a concise, defensible slide deck for advisor meetings, group updates, paper reading reports, or milestone reviews.

Use the sibling `pptx` skill when the user wants an actual `.pptx` file created or edited. Use this skill first to determine what the deck should say.

## When To Use

Use this skill when the user asks to:
- Make slides for a paper presentation
- Summarize weekly or monthly research progress
- Present experiment results to an advisor or lab
- Build opening, midterm, proposal, or defense update decks
- Convert notes into a slide-by-slide structure

## Workflow

### 1. Identify the meeting context

Determine:
- audience
- time limit
- meeting type
- deck goal

Common meeting types:
- paper reading
- weekly progress
- experiment update
- proposal / thesis planning
- rebuttal / response update

### 2. Decide the deck shape

Use a deck length that matches the meeting:
- 5 to 7 slides for a quick progress update
- 8 to 12 slides for paper reading or experiment report
- 12 to 18 slides for proposal or milestone review

Prefer fewer slides with clear claims over many dense slides.

### 3. Build the story

Use one of these structures:

#### Paper-reading deck
- Why this problem matters
- What prior work struggles with
- Paper idea
- Method intuition
- Key experiments
- Strengths and limitations
- What is relevant to our work

#### Progress-update deck
- Goal since last meeting
- What was done
- Results
- Failures or blockers
- Interpretation
- Next experiments
- Decisions needed

#### Proposal-style deck
- Problem statement
- Motivation and gap
- Proposed direction
- Preliminary evidence
- Risks
- Plan and milestones

### 4. Make each slide earn its place

For every slide, define:
- title
- one main claim
- 2 to 4 support bullets
- recommended visual
- speaker note

If a slide has no single claim, split or delete it.

### 5. Emphasize figures and results

For results slides, specify:
- what chart or table to show
- which comparison matters
- what takeaway the audience should remember

Never leave a result slide as raw numbers without interpretation.

## Output Format

Default to this structure:

```markdown
# Slide Outline

## Slide 1: Title
- Purpose:
- Main claim:
- Bullets:
- Visual:
- Speaker note:

## Slide 2: ...
```

## PPTX-Ready Variant

If the user wants direct deck production:
- keep each slide to a title plus 2 to 5 concise bullets
- indicate charts, tables, or diagrams explicitly
- mark appendix candidates separately
- then hand off to the local `pptx` skill for actual file creation

## Guardrails

- Do not paste paper prose directly into slides.
- Do not overload slides with derivation details unless the audience requires it.
- Do not show every experiment; show the experiments that support the story.
- Always include at least one slide on limitations, blockers, or open questions for research meetings.
- Optimize for what the advisor or lab needs to react to, not for completeness.
