---
phase: 05-knowledge
title: 知识管理与图谱
---

# Phase 05: 知识管理与图谱

Obsidian 笔记管理、知识图谱构建与文献知识蒸馏。

## 包含组件

### Skills（10）

| Skill | 说明 |
|-------|------|
| `graphify` | 代码/文档知识图谱自动构建 |
| `knowledge-base` | 知识库管理与维护 |
| `knowledge-distillation` | 知识蒸馏与精炼 |
| `obsidian-markdown` | Obsidian Markdown 格式规范 |
| `obsidian-bases` | Obsidian Bases 数据库查询 |
| `obsidian-cli` | Obsidian 命令行操作 |
| `obsidian-literature-workflow` | 文献笔记工作流 |
| `obsidian-project-memory` | 项目记忆管理 |
| `obsidian-project-bootstrap` | 项目初始化引导 |
| `obsidian-experiment-log` | 实验日志记录 |

### Agents（2）

| Agent | 说明 |
|-------|------|
| `literature-reviewer-obsidian` | Obsidian 文献综述代理 |
| `research-knowledge-curator-obsidian` | Obsidian 研究知识策展代理 |

### MCP Server

| Server | 用途 |
|--------|------|
| `mempalace` | 语义记忆宫殿（知识存储与检索） |

## 依赖关系

```
obsidian-literature-workflow
    --> obsidian-markdown（必需）
    --> zotero-obsidian-bridge（条件依赖，Phase 01）

graphify --> pip install graphifyy（注意双 y）
```

## 未包含组件

以下为空壳 skill，未纳入本模块：
- `obsidian-link-graph`
- `obsidian-project-lifecycle`
- `obsidian-research-log`
- `obsidian-synthesis-map`

## 快速开始

```bash
# 初始化 Obsidian 项目
/obsidian-project-bootstrap

# 文献笔记工作流
/obsidian-literature-workflow

# 构建知识图谱（需先安装 graphifyy）
/graphify
```
