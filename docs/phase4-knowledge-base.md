# Phase 4: 知识库与知识图谱

本阶段搭建本地知识管理系统，将前三个阶段积累的论文笔记、调研报告、写作草稿等素材组织为可检索、可关联的知识网络。核心工具包括 Obsidian（笔记与文档管理）、Graphify（代码/文档知识图谱）、MemPalace（语义记忆宫殿）以及 ChromaDB（向量数据库）。

---

## 1. 本阶段工具

| 工具 | 类型 | 用途 | GitHub / 来源 |
|------|------|------|---------------|
| `/kb-scan` `/kb-apply` `/kb-lint` `/kb-stats` `/kb-sync` | Knowledge Base Skills | 知识库扫描、应用规则、检查、统计、同步 | 本 repo `skills/kb-*/` |
| `/knowledge-base` | Skill | 知识库综合管理入口 | 本 repo `skills/knowledge-base/` |
| `kb.js` 脚本 | 自定义脚本 | 知识库自动化处理脚本 | 见 `scripts/knowledge-base-README.md` |
| `/graphify` | Skill | 为代码库/文档生成知识图谱 | 本 repo `skills/graphify/` |
| Graphify CLI | Python 包 | 知识图谱引擎（`graphifyy`） | [safishamsi/graphify](https://github.com/safishamsi/graphify) |
| MemPalace MCP | MCP 服务器 | 语义记忆宫殿，支持知识图谱和语义搜索（19 个工具） | [MemPalace/mempalace](https://github.com/MemPalace/mempalace) |
| ChromaDB | 向量数据库 | MemPalace 的后端存储引擎 | [chroma-core/chroma](https://github.com/chroma-core/chroma) |
| Obsidian | 桌面应用 | Markdown 笔记管理、双向链接、图谱视图 | [obsidian.md](https://obsidian.md) |

---

## 2. 安装步骤

### 2.1 Graphify 安装

Graphify 是一个 Python 包，用于从代码和文档中自动构建知识图谱。

```bash
# 安装 graphify（注意包名是 graphifyy，带双 y）
pip install graphifyy

# 在目标目录初始化
cd /i/knowledge
graphify install
```

**验证安装**：

```bash
graphify --version
```

**配置**：Graphify 会在目标目录生成 `.graphify-data/` 和 `.graphifyignore`。编辑 `.graphifyignore` 排除不需要索引的文件：

```
# .graphifyignore 示例
.obsidian/
.graphify-data/
*.pdf
*.png
*.jpg
```

### 2.2 MemPalace 安装

MemPalace 需要独立的 conda 环境（与 claudecode 基础环境隔离），避免 ChromaDB 版本冲突。

```bash
# 创建独立环境
conda create -n mempalace python=3.12 -y
conda activate mempalace

# 安装 MemPalace（会自动安装 ChromaDB 等依赖）
pip install mempalace

# 验证
python -c "import mempalace; print(mempalace.__version__)"
```

**MCP 服务器配置**（添加到 `~/.claude.json`）：

```jsonc
{
  "mcpServers": {
    "mempalace": {
      "command": "conda",
      "args": [
        "run",
        "-n", "mempalace",
        "--no-banner",
        "python", "-m", "mempalace.mcp_server"
      ],
      "type": "stdio"
    }
  }
}
```

**验证 MCP 连接**：在 Claude Code 中执行：

```
请用 mempalace_status 查看 MemPalace 状态
```

### 2.3 Obsidian 安装与配置

#### 下载安装

1. 访问 [obsidian.md](https://obsidian.md)，下载 Windows 安装包
2. 安装到合适位置（如 `F:\Obsidian\`，不建议装在 C 盘）
3. 启动 Obsidian

#### 创建 Vault（保管库）

**主 Vault**（笔记与文档）：

1. 点击 "Open folder as vault"
2. 选择 `G:\obsidian\` 目录
3. 确认打开

**知识库 Vault**（Graphify 驱动）：

1. 点击 "Open folder as vault"
2. 选择 `I:\knowledge\` 目录
3. 确认打开

#### 推荐插件

在 Obsidian 设置 → Community Plugins 中安装：

| 插件 | 用途 |
|------|------|
| Claudian | Obsidian + Claude Code 集成 |
| Excalidraw | 手绘风格图表 |
| Dataview | 数据查询视图 |
| Templater | 模板管理 |
| Calendar | 日历视图 |

### 2.4 Knowledge Base 脚本

Knowledge Base 相关脚本位于 `I:\claude-docs\ai-research-toolkit\scripts\` 目录，详见 `knowledge-base-README.md`。

确保脚本有执行权限：

```bash
chmod +x /i/claude-docs/ai-research-toolkit/scripts/kb*.sh
```

---

## 3. 使用示例

### 3.1 Knowledge Base 工作流

Knowledge Base Skills 提供了完整的工作流：

#### 扫描（kb-scan）

```
/kb-scan
```

扫描知识库目录，发现新文件和变更。自动识别：
- 新增的 Markdown 文件
- PDF 转 Markdown 的产物
- 元数据缺失的文件

#### 应用规则（kb-apply）

```
/kb-apply
```

对扫描结果应用知识库规则：
- 自动添加 frontmatter（标题、日期、标签）
- 建立双向链接
- 分类归档

#### 检查（kb-lint）

```
/kb-lint
```

检查知识库质量：
- 死链接检测
- frontmatter 完整性
- 文件命名规范
- 重复内容检测

#### 统计（kb-stats）

```
/kb-stats
```

显示知识库统计信息：
- 总文件数和总大小
- 按类型/标签分布
- 最近更新文件
- 链接网络密度

#### 同步（kb-sync）

```
/kb-sync
```

在不同位置之间同步知识库内容：
- `I:\claude-docs\` → `I:\knowledge\raw\` 的资料同步
- Git 仓库提交和推送

### 3.2 知识图谱（Graphify）

为指定目录生成知识图谱：

```
/graphify I:\knowledge
```

**Graphify 会**：
1. 扫描目录下所有文本文件
2. 提取实体和关系
3. 构建 god nodes（核心概念）和社区结构
4. 生成 `GRAPH_REPORT.md`（概览报告）
5. 生成 `wiki/index.md`（可导航的知识索引）

**查看图谱结果**：

```bash
# 查看图谱报告
cat /i/knowledge/graphify-out/GRAPH_REPORT.md

# 通过 wiki 索引浏览
# 在 Obsidian 中打开 graphify-out/wiki/index.md
```

**在 Obsidian 中查看**：
- 使用 Obsidian 的 Graph View 功能可视化知识图谱
- 打开 `I:\knowledge\` vault，切换到 Graph View

### 3.3 MemPalace 语义记忆

MemPalace 通过 MCP 服务器自动运行，提供以下能力：

#### 存储知识

```
请将以下内容存入 MemPalace：
wing: neural-speech
room: decoding-methods
content: "Smith2024 提出了一种基于 Transformer 的 ECoG 语音解码方法，
在 15 个音素分类任务上达到 92% 的准确率..."
```

#### 语义搜索

```
请用 mempalace_search 搜索 "ECoG 语音解码最新方法"
```

#### 知识图谱查询

```
请用 mempalace_kg_query 查询 "Transformer" 实体的所有关系
```

#### 时间线

```
请用 mempalace_kg_timeline 查看 "神经语音解码" 的时间线
```

#### 漫游宫殿

```
请用 mempalace_traverse 从 "decoding-methods" 房间开始漫游，查看跨领域连接
```

---

## 4. 知识库目录结构

### 4.1 主 Vault（G:\obsidian\）

```
G:\obsidian\
├── .obsidian\              ← Obsidian 配置（插件、主题）
├── .claudian\              ← Claudian 会话数据
├── .claude\                ← Claude Code 项目配置
└── base\                   ← 纯笔记和文档内容
    ├── Smith2024_Neural_Decoding\
    │   ├── Smith2024_Neural_Decoding_EN.pdf
    │   ├── Smith2024_Neural_Decoding_EN.md
    │   ├── Smith2024_Neural_Decoding_review.md    ← paper-review 产出
    │   └── Smith2024_Neural_Decoding_notes.md     ← 个人笔记
    ├── DeepLearning_Speech\
    │   └── research_report.md                     ← deep-research 产出
    └── 日常笔记.md
```

### 4.2 知识库 Vault（I:\knowledge\）

```
I:\knowledge\
├── .obsidian\              ← Obsidian 配置
├── CLAUDE.md               ← 维护者操作手册
├── .graphifyignore         ← Graphify 忽略规则
├── raw\                    ← 源资料（从 I:\claude-docs\ 同步）
│   └── articles\
├── wiki\                   ← 编译后的知识（由 Graphify/Claude 维护）
│   ├── concepts\           ← 概念解释
│   ├── summaries\          ← 文献摘要
│   └── topics\             ← 专题整理
├── outputs\                ← Q&A 产出和健康报告
└── .graphify-data\         ← Graphify 引擎数据
```

### 4.3 资料暂存（I:\claude-docs\）

```
I:\claude-docs\
├── md\                     ← Markdown 文件
├── html\                   ← HTML 文件
├── ppt\                    ← PPT/PPTX 文件
├── draw.io\                ← Draw.io 图表
├── txt\                    ← 纯文本
├── scripts\                ← 脚本文件
└── ai-research-toolkit\    ← 本工具包
```

---

## 5. 与其他阶段衔接

### 5.1 从 Phase 3 接收素材

| 素材来源 | 接收方式 | 存储位置 |
|----------|----------|----------|
| 论文 PDF | MinerU 转换 → 手动或自动归档 | `G:\obsidian\base\<论文名>\` |
| 审阅报告 | `/paper-review` 产出 | `G:\obsidian\base\<论文名>\*_review.md` |
| 调研报告 | `/deep-research-v5` 产出 | `G:\obsidian\base\<主题名>\` |
| 写作草稿 | `/academic-writing` 产出 | `G:\obsidian\base\<项目名>\draft\` |
| 组会 PPT | `/group-meeting-slides` 产出 | `I:\claude-docs\ppt\` |

### 5.2 为 Phase 5 提供知识支撑

Phase 5（实验管理与结果分析）将从知识库中获取：
- 文献中的基线方法和实验设计
- 数据集描述和评估指标
- 相关工作的对比表格

### 5.3 日常工作流

```
阅读新论文 → MinerU 转 MD → /paper-review → 归档到 base/
                                          ↓
                          /kb-scan → /kb-apply → /kb-lint
                                          ↓
                         Graphify 更新图谱 → Obsidian 查看
                                          ↓
                         MemPalace 存储关键发现 → 语义搜索可用
```

---

## 6. 常见问题

### Q1: Graphify 构建图谱时报内存不足怎么办？

Graphify 在处理大型代码库时会消耗较多内存。解决方案：
- 在 `.graphifyignore` 中排除大型二进制文件和无关目录
- 分批处理：先对子目录运行 Graphify，再对根目录运行
- 确保系统可用内存不低于 4GB

### Q2: MemPalace 的数据存在哪里？

MemPalace 的数据存储在 ChromaDB 中，默认位于 `~/.mempalace/` 目录。可以通过环境变量 `MEMPALACE_DATA_DIR` 自定义存储路径。ChromaDB 的数据是持久化的，重启不会丢失。

### Q3: kb-lint 报告大量死链接怎么处理？

死链接通常是因为文件移动或重命名导致的。处理方式：
1. 运行 `/kb-lint` 查看死链接详情
2. 手动修正链接路径，或使用 `/kb-apply` 自动修复
3. 如果是已删除的文件，移除指向它的链接即可

### Q4: Obsidian 的两个 Vault 可以同时打开吗？

可以。Obsidian 支持多窗口打开不同的 Vault。推荐：
- 主窗口：`G:\obsidian\`（日常工作）
- 辅助窗口：`I:\knowledge\`（查阅知识图谱）

### Q5: Graphify 和 MemPalace 的知识图谱有什么区别？

| 特性 | Graphify | MemPalace |
|------|----------|-----------|
| 数据来源 | 文件系统（代码、文档） | 交互式存储（MCP 调用） |
| 图谱类型 | 文件/实体关系图 | 语义记忆宫殿 |
| 查询方式 | `GRAPH_REPORT.md` / wiki | MCP 工具（search, traverse, kg_query） |
| 适用场景 | 理解代码库/文档结构 | 存储和检索研究知识 |
| 存储位置 | `.graphify-data/` | ChromaDB (`~/.mempalace/`) |

两者互补：Graphify 用于静态文档的结构化理解，MemPalace 用于动态知识的积累和检索。

---

## 7. Windows 注意事项

1. **路径分隔符**：Obsidian 使用反斜杠 `\`，Claude Code / Git Bash 使用正斜杠 `/`。在 MCP 工具中使用 Windows 原生路径，在 Bash 命令中使用 Unix 路径格式

2. **ChromaDB 与 SQLite**：ChromaDB 依赖 SQLite，Windows 上可能出现锁定问题。如果 MemPalace 启动失败，检查是否有其他进程占用了 `~/.mempalace/` 目录

3. **conda 环境激活**：MemPalace MCP 通过 `conda run -n mempalace` 启动，不需要手动激活环境。如果报错，确认 `mempalace` 环境已正确创建：
   ```bash
   conda env list | grep mempalace
   ```

4. **Graphify 路径**：在 Windows 上使用 Graphify CLI 时，路径需要使用正斜杠或双反斜杠：
   ```bash
   # 正确
   graphify build I:/knowledge
   # 也正确
   graphify build "I:\\knowledge"
   ```

5. **Obsidian Vault 位置**：避免将 Vault 放在 OneDrive 或其他同步目录中，同步冲突会损坏 `.obsidian/` 配置。推荐的 Vault 位置是本地磁盘（`G:\` 或 `I:\`）

6. **文件编码**：所有 Markdown 文件统一使用 UTF-8 编码（无 BOM）。Windows 记事本默认保存为 UTF-8 BOM，建议使用 VS Code 或 Obsidian 编辑

7. **长路径**：知识库中的文件路径可能较长，确保 Windows 长路径支持已启用（组策略 → 启用 Win32 长路径）
