# Phase 4: 知识库与知识图谱

本阶段负责把前面阶段产生的论文笔记、调研报告、写作草稿和图表材料，整理成可检索、可关联、可持续更新的知识体系。当前仓库的入口已经统一到 `knowledge-base` / `kb` skill，不再分发旧的 `kb-scan`、`kb-apply`、`kb-lint`、`kb-stats`、`kb-sync` 空壳命令。

---

## 1. 当前可用组件

| 组件 | 类型 | 用途 | 来源 |
|------|------|------|------|
| `/knowledge-base` 或 `/kb` | Skill | 统一知识库维护入口，支持 `scan` / `apply` / `lint` / `index` / `stats` / `sync` / `status` | 本 repo `modules/05-knowledge/skills/knowledge-base/` |
| `/graphify` | Skill | 为文档或代码目录生成知识图谱 | 本 repo `modules/05-knowledge/skills/graphify/` |
| `rebuild_graph.py` | Python 脚本 | GraphRAG 风格语义抽取与图重建 | 本 repo `modules/05-knowledge/skills/graphify/` |
| `Graphify CLI` | Python 包 | 图谱构建与导出 | [safishamsi/graphify](https://github.com/safishamsi/graphify) |
| `MemPalace MCP` | MCP 服务器 | 语义记忆与知识图谱查询 | [MemPalace/mempalace](https://github.com/MemPalace/mempalace) |
| `ChromaDB` | 向量数据库 | MemPalace 后端存储 | [chroma-core/chroma](https://github.com/chroma-core/chroma) |
| `Obsidian` | 桌面应用 | Markdown 笔记管理、双向链接、图谱浏览 | [obsidian.md](https://obsidian.md) |

如需当前 Skill / Agent 全量列表，参见 [modules/05-knowledge/README.md](../modules/05-knowledge/README.md)。

---

## 2. 安装与前置准备

### 2.1 安装本仓库知识管理模块

```bash
./scripts/install.sh --profile knowledge
```

或仅安装知识管理模块：

```bash
./scripts/install.sh --module 05-knowledge
```

### 2.2 安装 Graphify

```bash
pip install graphifyy
graphify --version
```

### 2.3 安装 MemPalace

建议使用独立环境，避免与其他 Python 依赖冲突：

```bash
conda create -n mempalace python=3.12 -y
conda activate mempalace
pip install mempalace
python -m mempalace.mcp_server --help
```

### 2.4 配置路径占位符

知识管理相关 Skill 依赖以下占位符，请在安装后的 `~/.claude/skills/.../SKILL.md` 中替换：

| 占位符 | 含义 |
|--------|------|
| `<OBSIDIAN_VAULT>` | 主 Obsidian vault 路径 |
| `<KNOWLEDGE_BASE_PATH>` | 知识库根目录 |
| `<KB_SCRIPTS_PATH>` | `kb.js` 所在目录 |

如果你使用 draw.io 辅助知识整理，还需要替换：

| 占位符 | 含义 |
|--------|------|
| `<DRAWIO_OUTPUT_DIR>` | draw.io 产物输出目录 |

---

## 3. 推荐工作流

### 3.1 统一知识库入口

`knowledge-base` skill 现在是唯一的知识库自动化入口：

```text
/knowledge-base scan
/knowledge-base apply
/knowledge-base lint
/knowledge-base index
/knowledge-base stats
/knowledge-base sync

# /kb 是同一 skill 的短名
/kb status
```

建议约定如下：

- `scan`：查看是否有新资料或待入库文件
- `apply`：在确认扫描结果后实际入库
- `lint`：检查 frontmatter、链接和命名质量
- `index`：刷新知识库索引
- `stats`：查看总量和分布
- `sync`：跑一整套标准流程（scan → apply → lint → index）
- `status`：快速看当前状态

### 3.2 Graphify / rebuild_graph.py

Graphify 适合做结构化图谱浏览；`rebuild_graph.py` 适合做语义增强抽取。

典型流程：

1. 把待分析资料放到知识库的 `raw/` 或其他统一素材目录。
2. 先用 `graphify` 生成基础图谱。
3. 需要更强语义抽取时，在目标目录中运行 `rebuild_graph.py`。
4. 在 `graphify-out/`、`GRAPH_REPORT.md`、`graph.json` 中查看结果。

`rebuild_graph.py` 需要以下环境变量：

```bash
export GRAPHIFY_API_URL="http://your-endpoint/v1/chat/completions"
export GRAPHIFY_API_KEY="your-api-key"
export GRAPHIFY_API_MODEL="your-model-name"
```

### 3.3 MemPalace

MemPalace 适合长期记忆和语义检索，不替代文档型知识库。推荐分工：

- Obsidian / Markdown：保留可编辑、可发布的笔记正文
- Graphify：构建可视化关系图
- MemPalace：做跨项目语义搜索、关系查询、时间线梳理

---

## 4. 目录建议

建议至少区分三个位置：

| 目录 | 用途 |
|------|------|
| `<OBSIDIAN_VAULT>` | 主笔记与项目管理 |
| `<KNOWLEDGE_BASE_PATH>` | 结构化知识库、Graphify 输出、索引 |
| `<CLAUDE_DOCS>` | 原始下载材料、临时导出、待整理内容 |

推荐关系：

- Phase 1/2/3 产物先进入 `<CLAUDE_DOCS>`
- 经 `knowledge-base apply` 或人工整理后进入 `<KNOWLEDGE_BASE_PATH>`
- 经摘要、改写、链接后沉淀到 `<OBSIDIAN_VAULT>`

---

## 5. 与其他阶段衔接

| 来源阶段 | 常见产物 | Phase 4 的处理方式 |
|----------|----------|--------------------|
| Phase 1 | 搜索记录、下载 PDF | 进入待整理目录，标记来源与主题 |
| Phase 2 | Markdown 转换结果、结构化提取文本 | 作为 `scan` / `apply` 的输入 |
| Phase 3 | 审阅报告、调研报告、写作草稿 | 入库后建立主题、项目、论文之间的双向链接 |
| Phase 6 | 图表、PPT、流程图 | 作为项目资产归档，并在笔记中链接 |

---

## 6. 常见问题

### Q1: 旧的 `/kb-scan` 等命令还能用吗？

不能依赖。仓库当前只保证 `knowledge-base` / `kb` 入口，旧命令不再作为分发能力维护。

### Q2: `rebuild_graph.py` 导入时报错怎么办？

当前实现已经改为仅在实际运行时校验环境变量。若执行时报错，优先检查：

- `GRAPHIFY_API_URL`
- `GRAPHIFY_API_KEY`
- `GRAPHIFY_API_MODEL`

### Q3: Graphify 和 MemPalace 应该选哪个？

- 需要可视化图谱、社区结构、文件间关系：选 Graphify
- 需要语义检索、长期记忆、实体关系查询：选 MemPalace
- 大多数项目会同时使用，两者职责不同

### Q4: kb.js 不在本仓库里怎么办？

按 `modules/05-knowledge/skills/knowledge-base/SKILL.md` 中的 `<KB_SCRIPTS_PATH>` 配置外部脚本目录；本仓库只提供 skill 接口和对接约定，不内嵌 kb.js 实现。

---

## 7. Windows 注意事项

- Git Bash 路径使用 `/c/Users/...` 风格，不使用反斜杠
- MCP 配置中的 Node 路径同样建议使用正斜杠
- 如果 `npx` 无法调用，确认 Node.js 已加入系统 PATH，而不是只在某个 shell 配置里可见
