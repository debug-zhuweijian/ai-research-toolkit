---
phase: 01-discovery
title: 文献发现与管理
---

# Phase 01: 文献发现与管理

文献检索、爬取、筛选与 Zotero/Obsidian 桥接。

## 包含组件

### Skills（5）

| Skill | 说明 |
|-------|------|
| `paper-search` | 多源论文检索（arXiv、Semantic Scholar、Google Scholar） |
| `academic-pipeline` | 端到端学术研究管道入口 |
| `0-autoresearch-skill` | 自动化研究流程编排 |
| `daily-paper-generator` | 每日 arXiv 论文摘要生成 |
| `zotero-obsidian-bridge` | Zotero 文献库与 Obsidian 笔记双向同步 |

### Agents（2）

| Agent | 说明 |
|-------|------|
| `paper-crawler` | 论文批量爬取与元数据提取 |
| `paper-miner` | 论文内容深度挖掘与结构化 |

## MCP Servers

| Server | 用途 |
|--------|------|
| `paper-search-mcp` | 论文检索 API 聚合 |
| `zotero-mcp` | Zotero 本地/云端库操作 |
| `arxiv-latex-mcp` | arXiv 论文 LaTeX 源码获取 |

## 快速开始

```bash
# 论文检索
/paper-search "speech decoding EEG"

# 启动完整研究管道
/academic-pipeline
```

## 依赖关系

- `zotero-obsidian-bridge` 需要 Zotero MCP server 正常运行
- `paper-search` 依赖 `paper-search-mcp` 项目（需单独部署）
- `daily-paper-generator` 需要 arXiv API 访问
