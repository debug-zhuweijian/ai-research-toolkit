# AI Research Toolkit 公开工具目录

本目录对应 `v0.3.0-beta.2` 的公开仓库内容，只列出本仓库已经包含的公开 modules、skills、agents、脚本、模板，以及公开文档中说明的上游集成类别。

本仓库不是任何本机 Claude 私有环境的镜像。本机私有 skills、私有 agents、plugin cache、凭据、API key、私有 URL、运行 ID、日志、数据库和机器专属路径都不属于公开发布内容。

## Research Discovery

公开模块：[`modules/01-discovery`](../modules/01-discovery/)

包含的 skills：

- `0-autoresearch-skill`
- `academic-pipeline`
- `daily-paper-generator`
- `paper-search`
- `zotero-obsidian-bridge`

公开文档中说明的上游集成：

- `paper-search-mcp`
- `zotero-mcp`
- `arxiv-latex-mcp`
- Zotero、Jasminum、`translators_CN`

## Document / PDF / Office Processing

公开模块：[`modules/02-processing`](../modules/02-processing/)

包含的 skills：

- `document-skills`
- `Geek-skills-mineru-pdf-parser`

公开文档中说明的上游集成：

- MinerU / OpenXLab
- `pdf-mcp`
- MarkItDown
- LibreOffice 与 Poppler

## Literature Review And Evidence Analysis

公开模块：[`modules/03-analysis`](../modules/03-analysis/)

包含的 skills：

- `academic-paper-reviewer`
- `brainstorming-research-ideas`
- `confidence-check`
- `content-research-writer`
- `creative-thinking-for-research`
- `deep-research-v5`
- `paper-proofread`
- `paper-review`
- `research-ideation`

公开文档中说明的上游集成：

- Sequential Thinking MCP
- Web search / web reader MCP 模式

## Writing And Revision

公开模块：[`modules/04-writing`](../modules/04-writing/)

包含的 skills：

- `academic-paper`
- `academic-writing`
- `ml-paper-writing`
- `post-acceptance`
- `results-analysis`
- `results-report`
- `review-response`
- `systems-paper-writing`
- `writing-anti-ai`

## Knowledge Graph / Obsidian / Graphify / MemPalace

公开模块：[`modules/05-knowledge`](../modules/05-knowledge/)

包含的 skills：

- `graphify`
- `knowledge-base`
- `knowledge-distillation`
- `obsidian-bases`
- `obsidian-cli`
- `obsidian-experiment-log`
- `obsidian-literature-workflow`
- `obsidian-markdown`
- `obsidian-project-bootstrap`
- `obsidian-project-memory`

公开脚本与集成：

- [`modules/05-knowledge/skills/graphify/rebuild_graph.py`](../modules/05-knowledge/skills/graphify/rebuild_graph.py)
- Graphify
- MemPalace
- ChromaDB
- Obsidian 工作流约定

## Presentation And Figures

公开模块：[`modules/06-presentation`](../modules/06-presentation/)

包含的 skills：

- `academic-plotting`
- `academic-pptx`
- `drawio`
- `group-meeting-slides`
- `notion-infographic`
- `presenting-conference-talks`
- `publication-chart-skill`

公开文档中说明的上游集成：

- draw.io MCP
- 用于视觉验收的 Playwright MCP 模式

## Pipeline Orchestration

公开模块：[`modules/07-pipeline`](../modules/07-pipeline/)

active beta skill：

- `paperclip-pipeline`

公开模板与验证脚本：

- [`modules/07-pipeline/configs/paperclip.example.json`](../modules/07-pipeline/configs/paperclip.example.json)
- [`scripts/verify-paperclip-config.sh`](../scripts/verify-paperclip-config.sh)
- [`scripts/verify-paperclip-config.ps1`](../scripts/verify-paperclip-config.ps1)

公开 Paperclip 面只包含工作流协议、交接包约定和脱敏配置模板，不包含私有 Paperclip 服务连接器或部署细节。

## Verification And Handoff Governance

公开脚本：

- [`scripts/install.sh`](../scripts/install.sh)
- [`scripts/install.ps1`](../scripts/install.ps1)
- [`scripts/verify-setup.sh`](../scripts/verify-setup.sh)
- [`scripts/verify-profiles.py`](../scripts/verify-profiles.py)
- [`scripts/scan-public-safety.py`](../scripts/scan-public-safety.py)
- [`scripts/verify-paperclip-config.sh`](../scripts/verify-paperclip-config.sh)
- [`scripts/verify-paperclip-config.ps1`](../scripts/verify-paperclip-config.ps1)

支持的安装预设：

- `minimal`：阶段 01 和阶段 02
- `researcher`：阶段 01 到阶段 04
- `writer`：阶段 04 和阶段 06
- `knowledge`：阶段 05 和阶段 06
- `full`：阶段 01 到阶段 07

profile 验证脚本会从模块内容重新计算 skill 数，并检查 JSON profile、Bash 安装器和 PowerShell 安装器是否一致。

## Experimental Agents

公开实验区：[`experimental/`](../experimental/)

`experimental/` 目录记录需要独立平台运行的 DeepScientist 风格 agents。它们不会由标准 profile 安装器安装，也不作为默认公开 runtime 面的一部分。

## Private / Local Integrations Boundary

公开仓库可以描述 Claude Code、MCP servers、Obsidian、Graphify、MemPalace、Zotero、MinerU、BigModel 等集成类别，但不得包含：

- 真实 API key、access token、refresh token、cookie 或 private key。
- 私有 VPS URL、私有 OpenAI-compatible endpoint、私有 base URL 或私有模型默认值。
- 本机认证 JSON、`.env` 文件、日志、数据库、coverage 输出、缓存或运行导出文件。
- 只存在于本机 `.claude`、`.codex`、`.agents` 或 plugin cache 中的 skill / agent 正文。
- 机器专属绝对路径，除非是明确的占位符示例。

公开文档和模板统一使用 `<ANTHROPIC_API_KEY>`、`<BIGMODEL_API_KEY>`、`<MINERU_API_KEY>`、`<BASE_URL>`、`<ANTHROPIC_COMPATIBLE_BASE_URL>` 等占位符。
