---
phase: 02-processing
title: 文档处理
---

# Phase 02: 文档处理

PDF、Word、PPT、Excel 等文档的解析、转换与结构化提取。

## 包含组件

### Skills（2）

| Skill | 说明 |
|-------|------|
| `document-skills` | 综合文档处理套件（pdf + docx + pptx + xlsx，40+ 文件） |
| `Geek-skills-mineru-pdf-parser` | MinerU 驱动的 PDF 高精度解析 |

## MCP Servers

| Server | 用途 |
|--------|------|
| `mineru-mcp` | MinerU 文档转 Markdown（支持 PDF/PPT/DOCX/图片） |
| `pdf-mcp` | PDF 读取、拆分、合并、提取、渲染 |
| `markitdown` | URL/文件转 Markdown 通用接口 |

## 快速开始

```bash
# PDF 转 Markdown（通过 MinerU）
/Geek-skills-mineru-pdf-parser

# PDF 信息查询与文本提取（通过 pdf-mcp）
# 直接使用 MCP 工具即可，无需 skill 调用
```

## 能力矩阵

| 功能 | mineru-mcp | pdf-mcp | markitdown |
|------|:----------:|:-------:|:----------:|
| PDF 转 Markdown | v | - | v |
| PDF 拆分/合并 | - | v | - |
| PDF 元数据 | - | v | - |
| PDF 页面渲染 | - | v | - |
| 通用 URL 转换 | - | - | v |
| OCR 支持 | v | - | - |
