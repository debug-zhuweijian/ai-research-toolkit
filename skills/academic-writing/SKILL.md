---
name: academic-writing
description: 学术写作：起草、修改和润色学术论文、期刊文章
---
# Academic Writing

## Overview

Use this skill to turn rough research writing into publication-oriented prose. Focus on argument quality, structure, precision, and evidence alignment rather than generic "polishing."

Use the local `docx` skill when the user needs a `.docx` file edited with formatting or tracked changes. Use this skill to decide what the text should become.

## When To Use

Use this skill when the user asks to:
- polish a paper section
- rewrite an abstract or introduction
- improve a thesis chapter
- draft related work or discussion sections
- prepare a rebuttal or response to reviewers
- convert notes into academic prose
- make English more natural without losing technical meaning

## Workflow

### 1. Identify the writing artifact

Determine:
- artifact type
- target venue or degree context
- target audience
- desired intervention

Typical artifact types:
- abstract
- introduction
- related work
- methods
- experiments
- discussion
- conclusion
- rebuttal
- review response
- proposal

### 2. Preserve meaning before style

Before rewriting, identify:
- main claim
- evidence supporting the claim
- scope of the claim
- technical terms that must remain exact

Never improve fluency by weakening precision.

### 3. Fix the highest-level problems first

Prioritize in this order:
1. argument structure
2. paragraph logic
3. sentence clarity
4. concision
5. tone and style

Do not waste effort on sentence polish when the paragraph is logically broken.

### 4. Match the academic task

#### Abstract
- problem
- method
- evidence
- contribution
- significance

#### Introduction
- context
- problem gap
- why prior work is insufficient
- proposed idea
- contribution list

#### Related work
- group prior work by line of approach
- explain limits of each line
- connect directly to the current paper

#### Rebuttal / reviewer response
- answer each concern explicitly
- concede valid issues
- avoid defensive language
- state concrete revisions or clarifications

### 5. Offer revision levels

When useful, provide one of these:
- light edit
- substantive rewrite
- structural rewrite

Make the chosen level explicit so the user understands how much changed.

## Output Format

Use one of these depending on the request.

### Polishing mode

```markdown
## Revised Version
[clean rewritten text]

## Key Improvements
- 
```

### Reviewer-response mode

```markdown
## Reviewer Comment
[comment]

## Response
[clear, respectful response]

## Planned Revision
- 
```

### Structure-feedback mode

```markdown
## Main Issues
- 

## Suggested Structure
- 

## Revised Draft
[text]
```

## Style Rules

- Prefer precise claims over inflated claims.
- Prefer short declarative sentences when the point is technical.
- Use hedge words only when uncertainty is real.
- Keep contribution statements explicit and countable.
- Avoid vague praise words such as "novel", "effective", or "robust" unless justified nearby.
- Preserve notation, dataset names, metric names, and baseline names exactly.

## Guardrails

- Do not invent citations, results, or experimental details.
- Do not overclaim significance when the evidence is narrow.
- Do not erase the author's technical intent for smoother English.
- Do not produce rebuttal language that sounds emotional or combative.
- If the draft is missing evidence, say that the issue is substantive rather than stylistic.
