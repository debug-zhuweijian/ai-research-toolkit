---
phase: 04-writing
title: 学术写作与出版
---

# Phase 04: 学术写作与出版

论文撰写、审稿响应、出版全流程支持。

## 包含组件

### Skills（9）

| Skill | 说明 |
|-------|------|
| `academic-writing` | 学术写作规范与风格指导 |
| `academic-paper` | 完整学术论文结构生成 |
| `ml-paper-writing` | 机器学习论文专项写作 |
| `systems-paper-writing` | 系统类论文专项写作 |
| `writing-anti-ai` | 降低 AI 检测率的写作技巧 |
| `post-acceptance` | 论文接收后处理（校样、版权等） |
| `review-response` | 审稿意见回复撰写 |
| `results-analysis` | 实验结果分析与可视化 |
| `results-report` | 实验结果报告生成 |

### Agents（7）

| Agent | 说明 |
|-------|------|
| `section-drafter` | 论文章节草稿撰写 |
| `prose-polisher` | 文本润色与语言优化 |
| `rebuttal-writer` | Rebuttal 撰写代理 |
| `writing-reviewer` | 写作质量审查代理 |
| `logic-reviewer` | 逻辑连贯性审查代理 |
| `latex-figure-specialist` | LaTeX 图表排版专家 |
| `latex-layout-auditor` | LaTeX 排版审计代理 |

## 核心流水线

```
academic-writing
    --> academic-paper
        --> academic-paper-reviewer (Phase 03)
            --> review-response
                --> post-acceptance
                    --> presenting-conference-talks (Phase 06)
```

## 快速开始

```bash
# 学术论文写作
/academic-writing

# ML 论文专项
/ml-paper-writing

# 审稿回复
/review-response
```
