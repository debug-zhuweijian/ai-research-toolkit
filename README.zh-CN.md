<div align="center">

# AI Research Toolkit

**基于 Claude Code 的全流程 AI 辅助学术研究工具链**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.2.0--alpha-orange.svg)](CHANGELOG.md)

[English](README.md) | [中文](README.zh-CN.md)

</div>

面向学术研究者的全链路工具包，覆盖从文献发现到论文出版的完整研究流程。42 个 Skills、16 个 Agents、10 个 MCP 服务器，按 7 个研究阶段组织。

## 7 阶段管道

| 阶段 | 模块 | Skills | Agents | 说明 |
|------|------|--------|--------|------|
| 01 | [Discovery](modules/01-discovery/README.md) | 5 | 2 | 文献发现与管理 |
| 02 | [Processing](modules/02-processing/README.md) | 2 | — | 文档处理（PDF/DOCX/PPTX/XLSX） |
| 03 | [Analysis](modules/03-analysis/README.md) | 9 | 5 | 论文分析与深度研究 |
| 04 | [Writing](modules/04-writing/README.md) | 9 | 7 | 学术写作与出版 |
| 05 | [Knowledge](modules/05-knowledge/README.md) | 10 | 2 | 知识管理与图谱 |
| 06 | [Presentation](modules/06-presentation/README.md) | 7 | — | 演示与可视化 |
| 07 | [Pipeline](modules/07-pipeline/README.md) | — | — | 管道编排（规划中） |
| **合计** | | **42** | **16** | |

## 快速开始

### 环境要求

- [Claude Code](https://claude.ai/code) 已安装
- Python 3.10+（推荐 Anaconda）
- Node.js 18+
- Git 2.30+

### 安装

```bash
# 克隆
git clone https://github.com/debug-zhuweijian/ai-research-toolkit.git
cd ai-research-toolkit

# 按预设安装
./scripts/install.sh --profile researcher    # 推荐：完整研究流程
./scripts/install.sh --profile writer        # 论文写作 + 演示
./scripts/install.sh --profile full          # 全部安装
./scripts/install.sh --module 03-analysis    # 或安装单个阶段

# 配置 MCP 服务器
# 编辑 ~/.claude.json，合并 configs/mcp-servers-full.json
```

### 安装预设

| 预设 | 模块 | Skills 数 | 适用场景 |
|------|------|-----------|---------|
| `minimal` | 01, 02 | 7 | 文献搜索 + 文档处理 |
| `writer` | 04, 06 | 16 | 学术写作 + 演示 |
| `researcher` | 01-04 | 25 | 完整研究流程 |
| `knowledge` | 05, 06 | 17 | 知识管理 + Obsidian |
| `full` | 01-06 | 42 | 全链路 |

## MCP 服务器

| Server | 阶段 | 用途 |
|--------|------|------|
| paper-search-mcp | 01 | 20+ 数据库论文搜索 |
| zotero-mcp | 01 | Zotero 本地管理 |
| arxiv-latex-mcp | 01 | arXiv LaTeX 源码获取 |
| mineru-mcp | 02 | PDF→Markdown 转换 |
| pdf-mcp | 02 | PDF 操作 |
| mempalace | 05 | 知识图谱记忆 |

全局服务器（web-search-prime, web-reader, zread, zai-mcp-server, GitKraken）通过 `configs/mcp-servers-full.json` 配置。

## 文档

- [安装指南](docs/installation-guide.md)
- [环境要求](docs/prerequisites.md)
- [API Key 配置](docs/api-keys-guide.md)
- [管道概览](docs/pipeline-overview.md)
- [故障排除](docs/troubleshooting.md)

## v0.2 新特性

- **阶段式模块结构** — 按 7 个研究阶段组织
- **29 个新 Skills** — 头脑风暴、ML 论文写作、Obsidian 工作流等
- **15 个新 Agents** — 文献综述、LaTeX 专家、Rebuttal 写作
- **5 个安装预设** — 按需安装
- **14 个 DeepScientist agents** 移至 experimental/
- **5 个 kb-* 空壳** 已移除

详见 [CHANGELOG.md](CHANGELOG.md)。

## 许可证

MIT
