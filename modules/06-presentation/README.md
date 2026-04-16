---
phase: 06-presentation
title: 演示与可视化
---

# Phase 06: 演示与可视化

学术 PPT、图表绘制、信息图与会议演讲支持。

## 包含组件

### Skills（7）

| Skill | 说明 |
|-------|------|
| `academic-pptx` | 学术论文 PPT 生成 |
| `group-meeting-slides` | 组会报告幻灯片制作 |
| `academic-plotting` | 学术论文图表绘制（matplotlib/seaborn） |
| `drawio` | Draw.io 架构图/流程图生成 |
| `notion-infographic` | Notion 风格信息图制作 |
| `publication-chart-skill` | 出版级图表制作 |
| `presenting-conference-talks` | 会议演讲稿与展示准备 |

## 依赖关系

```
academic-pptx
    --> document-skills/pptx（Phase 02）
        --> pptxgenjs（npm）
        --> markitdown[pptx]
        --> LibreOffice（可选，格式转换）
        --> Poppler（可选，PDF 渲染）
```

## 快速开始

```bash
# 学术 PPT 生成
/academic-pptx

# 组会幻灯片
/group-meeting-slides

# 学术图表
/academic-plotting

# 架构图/流程图
/drawio

# 会议演讲准备
/presenting-conference-talks
```

## 图表能力对比

| 需求 | 推荐 Skill |
|------|-----------|
| 数据可视化（折线/柱状/热力图） | `academic-plotting` |
| 出版级统计图表 | `publication-chart-skill` |
| 架构图/流程图/系统图 | `drawio` |
| 信息图/概览图 | `notion-infographic` |
| PPT 内嵌图表 | `academic-pptx` |
