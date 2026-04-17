# 完整安装教程

> 从零开始，搭建 AI 辅助科研全流程环境。预计 2-3 小时（含下载等待时间）。

本工具包是一个 **meta-repo**：它本身不包含工具源码，而是将多个开源工具串联成一个完整管线。每个工具都需要从其 GitHub 仓库独立安装。本教程将逐一覆盖。

---

## 安装路线图

```
第 1 步：基础环境（Python/Node/Git/uv）          ← 30 min
第 2 步：Claude Code + API Key（Anthropic 或兼容端点） ← 15 min
第 3 步：Clone 本 repo + 复制 Skills/Agents       ← 5 min
第 4 步：Phase 1 — paper-search-mcp 安装          ← 10 min
第 5 步：Phase 2 — MinerU + pdf-mcp 安装          ← 20 min
第 6 步：Phase 3 — 智谱 MCP + Sequential Thinking ← 15 min
第 7 步：Phase 4 — Graphify + MemPalace 安装       ← 20 min
第 8 步：MCP 配置合并 + 验证                      ← 15 min
```

---

## 第 1 步：基础环境

### 1.1 Python 3.10+（推荐 Anaconda）

```bash
# 下载 Anaconda：https://www.anaconda.com/download
# Windows 运行安装程序，macOS/Linux 用命令行安装

# 验证
python --version    # 应显示 3.10 或更高
conda --version
```

> 如果已有 Python 但没有 conda，也可以直接用系统 Python。但 Phase 4 的 MemPalace 需要 conda 创建独立环境。

### 1.2 Node.js 18+

```bash
# 下载 LTS：https://nodejs.org/
# 或用包管理器：
#   Windows: winget install OpenJS.NodeJS.LTS
#   macOS:   brew install node@20

# 验证
node --version      # 应显示 v18+ 或更高
npm --version
```

> Node.js 是多个 MCP 服务器（pdf-mcp、sequential-thinking、drawio、playwright）的运行时。

### 1.3 Git

```bash
# 下载：https://git-scm.com/
# Windows 用户推荐 Git Bash 终端

# 验证
git --version
```

### 1.4 uv（Python 包管理器）

uv 是 pip 的替代品，速度更快，用于安装 paper-search-mcp 等工具。

```bash
# Windows (PowerShell):
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# 验证
uv --version
```

### 1.5 验证基础环境

```bash
python --version   # 3.10+
node --version     # v18+
git --version      # 2.30+
uv --version       # 任意版本
```

全部通过后继续。

---

## 第 2 步：Claude Code + API Key（Anthropic 或兼容端点）

### 2.1 安装 Claude Code

```bash
npm install -g @anthropic-ai/claude-code

# 验证
claude --version
```

### 2.2 配置 API Key

Claude Code 需要一个 API Key 才能运行。有两种方式：

**方式 A：使用 Anthropic 官方 API Key**

1. 访问 [console.anthropic.com](https://console.anthropic.com)
2. 注册账号（Google 登录或邮箱注册）
3. 左侧菜单 → **API Keys** → **Create Key**
4. 复制 Key（格式 `sk-ant-api03-...`），**只显示一次**
5. 充值 $5（Settings → Billing → Add Credits，需要信用卡）

**方式 B：使用 Anthropic 兼容端点（如智谱 BigModel）**

如果你通过 Anthropic 兼容端点运行 Claude Code（例如智谱 BigModel 的 GLM 系列），无需 Anthropic API Key，只需配置对应平台的 API Key 和 `base_url`：

```bash
# 在 ~/.bashrc 或启动时设置环境变量
export ANTHROPIC_API_KEY="你的兼容端点API密钥"
export ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/paas/v4/"  # 以智谱为例
```

> 其他兼容端点（如 OpenRouter、AWS Bedrock 等）也支持类似配置，只需替换对应的 API Key 和 base_url。

### 2.3 启动 Claude Code

```bash
claude
# 首次启动提示输入 API Key → 粘贴你的 Key
# 能正常对话即说明配置成功
```

> 也可以用环境变量：`export ANTHROPIC_API_KEY="你的Key"`

---

## 第 3 步：Clone 本 Repo + 安装 Skills/Agents

### 3.1 Clone

```bash
git clone https://github.com/debug-zhuweijian/ai-research-toolkit.git
cd ai-research-toolkit
```

### 3.2 使用安装脚本

推荐使用仓库自带安装脚本，而不是手动复制 `modules/*/skills` 和 `modules/*/agents`。

```bash
# Bash / zsh / Git Bash
./scripts/install.sh --list
./scripts/install.sh --profile full

# 只安装知识管理相关模块
./scripts/install.sh --profile knowledge

# 只安装某个模块
./scripts/install.sh --module 05-knowledge
```

```powershell
# PowerShell
.\scripts\install.ps1 -List
.\scripts\install.ps1 -Profile full

# 只安装某个模块
.\scripts\install.ps1 -Module 05-knowledge
```

安装脚本默认写入：

- Skills → `~/.claude/skills/`
- Agents → `~/.claude/agents/`

可通过 `--skills-path` / `--agents-path`（PowerShell 为 `-SkillsPath` / `-AgentsPath`）覆盖目标路径；传 `--force` / `-Force` 可覆盖已有安装。

### 3.3 验证安装

```bash
./scripts/verify-setup.sh
```

### 3.4 替换路径占位符

部分 Skill 包含路径占位符，需要替换为你本地的实际路径。

**需要替换的占位符：**

| 占位符 | 含义 | 示例值 |
|--------|------|--------|
| `<PAPER_SEARCH_MCP_PATH>` | paper-search-mcp 安装路径 | `/c/Users/YOU/paper-search-mcp` |
| `<OBSIDIAN_VAULT>` | Obsidian vault 路径 | `/c/Users/YOU/obsidian-vault` |
| `<KNOWLEDGE_BASE_PATH>` | 知识库目录路径 | `/c/Users/YOU/knowledge` |
| `<KB_SCRIPTS_PATH>` | kb.js 脚本目录路径 | `/c/Users/YOU/scripts/kb` |
| `<DRAWIO_OUTPUT_DIR>` | draw.io 图表输出目录 | `/c/Users/YOU/drawio-output` |

**替换方法（以 paper-search 为例）：**

```bash
# Linux/macOS:
sed -i 's|<PAPER_SEARCH_MCP_PATH>|/home/YOU/paper-search-mcp|g' ~/.claude/skills/paper-search/SKILL.md

# Windows (Git Bash) — 注意用 Unix 风格路径:
sed -i 's|<PAPER_SEARCH_MCP_PATH>|/c/Users/YOU/paper-search-mcp|g' ~/.claude/skills/paper-search/SKILL.md
```

对其他占位符执行类似操作。如果暂时不确定路径，可以先跳过，后续安装对应工具后再回来替换。

> **Windows 路径转换**：Windows 路径 `C:\Users\YOU\` 在 Git Bash 中要写成 `/c/Users/YOU/`。可以用 `cygpath -u "C:\Users\YOU\xxx"` 转换。

---

## 第 4 步：Phase 1 — paper-search-mcp

> GitHub: [openags/paper-search-mcp](https://github.com/openags/paper-search-mcp)
> License: MIT | 21+ 免费学术源，支持 arXiv/PubMed/Semantic Scholar/CORE 等

### 4.1 安装

**方式 A：uvx 直接运行（推荐）**

无需 clone，uv 自动管理虚拟环境：

```bash
# 验证可用
uvx paper-search-mcp --help
```

**方式 B：pip 安装**

```bash
pip install paper-search-mcp
paper-search sources
```

**方式 C：克隆源码（需要自定义或开发）**

```bash
git clone https://github.com/openags/paper-search-mcp.git ~/paper-search-mcp
cd ~/paper-search-mcp
uv sync

# 验证
uv run paper-search sources
# 应列出 21+ 个数据源
```

如果选择方式 C，记录路径并替换 SKILL.md 中的 `<PAPER_SEARCH_MCP_PATH>`。

### 4.2 配置可选 API Key

基础搜索**无需任何 Key**。以下 Key 可提升搜索质量：

```bash
# 添加到 ~/.bashrc（永久生效）

# CORE（推荐 — 3 亿+ 论文，免费即时发放）
export PAPER_SEARCH_MCP_CORE_API_KEY="your_core_key"
# 注册：https://core.ac.uk/services/api

# Semantic Scholar（推荐 — 提升速率限额，免费）
export PAPER_SEARCH_MCP_SEMANTIC_SCHOLAR_API_KEY="your_s2_key"
# 注册：https://www.semanticscholar.org/product/api

# Unpaywall（推荐 — 定位开放获取 PDF，只需邮箱）
export PAPER_SEARCH_MCP_UNPAYWALL_EMAIL="your_name@university.edu"
# 无需注册，直接设置邮箱即可

# DOAJ（可选）
export PAPER_SEARCH_MCP_DOAJ_API_KEY="your_doaj_key"
# 注册：https://doaj.org/api/docs

# IEEE（可选，需审核 1-3 天）
export PAPER_SEARCH_MCP_IEEE_API_KEY="your_ieee_key"
# 注册：https://developer.ieee.org

# ACM（可选，需机构订阅）
export PAPER_SEARCH_MCP_ACM_API_KEY="your_acm_key"
# 注册：https://dl.acm.org
```

### 4.3 验证

```bash
# 搜索测试（arXiv 是最稳定的免费源）
paper-search search "graph neural networks" -n 3 -s arxiv
# 应返回 3 篇论文的 JSON 结果
```

---

## 第 5 步：Phase 2 — MinerU + pdf-mcp

### 5.1 MinerU MCP Server

> GitHub: [opendatalab/MinerU](https://github.com/opendatalab/MinerU)
> License: Apache-2.0 | PDF → 高质量 Markdown，保留表格/公式/多栏布局

**安装：**

```bash
pip install mineru-mcp-server

# 验证
mineru-mcp-server --help
```

**获取 API Key（云端转换需要，免费）：**

1. 访问 [openxlab.org.cn](https://openxlab.org.cn)
2. 注册账号（GitHub 登录或手机号）
3. 个人中心 → API Token → 生成新 Token
4. 复制保存

> 每日免费 1000 页，日常科研完全够用。无需本地 GPU。

### 5.2 pdf-mcp

> GitHub: [angshuman/pdf-mcp](https://github.com/angshuman/pdf-mcp)
> License: MIT | PDF 读写、拆分、合并、页面提取、转图片

**安装：**

```bash
# 克隆到 MCP 服务器目录
mkdir -p ~/.claude/mcp-servers
git clone https://github.com/angshuman/pdf-mcp.git ~/.claude/mcp-servers/pdf-mcp

# 安装依赖
cd ~/.claude/mcp-servers/pdf-mcp
npm install
```

**验证：**

```bash
# Linux/macOS:
node ~/.claude/mcp-servers/pdf-mcp/src/server.js --help

# Windows (Git Bash):
node ~/.claude/mcp-servers/pdf-mcp/src/server.js --help
# 无报错即成功
```

记录 server.js 的完整路径，后续 MCP 配置需要用到：
- Linux/macOS: `/home/YOU/.claude/mcp-servers/pdf-mcp/src/server.js`
- Windows: `C:/Users/YOU/.claude/mcp-servers/pdf-mcp/src/server.js`

### 5.3 MarkItDown（可选）

> GitHub: [microsoft/markitdown](https://github.com/microsoft/markitdown)
> License: MIT | Office 文件（DOCX/PPTX/XLSX）→ Markdown

```bash
# 安装（同时提供 MCP 服务器模式）
pip install markitdown-mcp

# 验证
markitdown-mcp --help
```

---

## 第 6 步：Phase 3 — 智谱 MCP + Sequential Thinking

### 6.1 智谱 BigModel API Key

> 官网：[open.bigmodel.cn](https://open.bigmodel.cn)
> 免费额度，一个 Key 供 4 个 MCP 服务器共用

**注册并获取 Key：**

1. 访问 [open.bigmodel.cn](https://open.bigmodel.cn)
2. 注册账号（手机号或微信扫码）
3. 控制台 → API Keys → 创建新密钥
4. 复制 Key（格式 `xxxxxxxx.xxxxxxxx`）

**此 Key 同时用于：**

| MCP 服务器 | 功能 | 配置方式 |
|------------|------|----------|
| `web-search-prime` | 网络搜索 | HTTP MCP（远程） |
| `web-reader` | 网页内容提取 | HTTP MCP（远程） |
| `zread` | GitHub 仓库读取 | HTTP MCP（远程） |
| `zai-mcp-server` | 图像/视频分析 | stdio MCP（本地 npx） |

前三个是 HTTP 类型，只需配置 URL + Authorization header，**无需安装任何 npm 包**。zai-mcp-server 需要 npx 自动下载。

### 6.2 Sequential Thinking MCP

> GitHub: [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)
> License: MIT | 结构化多步推理

无需 clone，npx 自动运行：

```bash
# 验证 npx 可用
npx --version
```

后续在 MCP 配置中通过 npx 启动即可。

### 6.3 zai-mcp-server

> npm: [@z_ai/mcp-server](https://www.npmjs.com/package/@z_ai/mcp-server)

无需手动安装，npx 自动下载。需要设置环境变量：

```bash
export Z_AI_API_KEY="你的智谱API密钥"
export Z_AI_MODE="ZHIPU"
```

---

## 第 7 步：Phase 4 — Graphify + MemPalace

### 7.1 Graphify

> GitHub: [safishamsi/graphify](https://github.com/safishamsi/graphify)
> License: MIT | 扫描文档 → 生成交互式知识图谱

```bash
# 注意包名是 graphifyy（双 y）
pip install graphifyy

# 初始化
graphify install

# 验证
graphify --version
```

### 7.2 MemPalace

> GitHub: [MemPalace/mempalace](https://github.com/MemPalace/mempalace)
> License: MIT | 语义记忆宫殿 + 知识图谱 + 向量搜索（19 个 MCP 工具）

MemPalace 需要**独立的 conda 环境**（避免依赖冲突）：

```bash
# 创建环境
conda create -n mempalace python=3.12 -y
conda activate mempalace

# 安装
pip install mempalace
# ChromaDB 会作为依赖自动安装

# 验证
python -c "import mempalace; print('OK')"
python -m mempalace.mcp_server --help
```

记录 mempalace 环境的 Python 路径：

```bash
# Linux/macOS:
which python
# 输出: /home/YOU/anaconda3/envs/mempalace/bin/python

# Windows (Git Bash):
which python
# 输出: /c/Users/YOU/anaconda3/envs/mempalace/python.exe

# 或用 conda 查询:
conda run -n mempalace which python
```

此路径后续配置 MCP 时需要用到。

### 7.3 Obsidian（推荐）

> 官网：[obsidian.md](https://obsidian.md)

1. 从 [obsidian.md](https://obsidian.md) 下载桌面客户端
2. 安装后创建新 Vault（或打开已有 Vault）
3. 推荐目录结构见 [configs/obsidian/vault-structure.md](../configs/obsidian/vault-structure.md)

### 7.4 Zotero + Jasminum（推荐，用于中文文献）

**Zotero：**
1. 从 [zotero.org](https://www.zotero.org/) 下载安装
2. 安装浏览器 Connector（Chrome/Edge/Firefox）

**Jasminum（知网支持）：**
1. 从 [Jasminum Releases](https://github.com/l0o0/jasminum/releases) 下载 `.xpi`
2. Zotero → 工具 → 插件 → Install Add-on From File → 选择 `.xpi`

**translators_CN（中文文献库）：**
1. `git clone https://github.com/l0o0/translators_CN.git`
2. 复制 `.js` 文件到 Zotero translators 目录
3. Zotero → 编辑 → 首选项 → 高级 → 立即更新翻译器

---

## 第 8 步：MCP 配置合并 + 验证

### 8.1 编辑 ~/.claude.json

**这是最关键的一步。** 所有 MCP 服务器的配置都写在这个文件中。

```bash
# 用你喜欢的编辑器打开
# Linux/macOS: ~/.claude.json
# Windows:     C:\Users\YOU\.claude.json
```

将 `configs/mcp-servers-full.json` 中的 `mcpServers` 部分**合并**到你的 `~/.claude.json` 中。注意是合并，不是覆盖 — 保留你已有的配置。

### 8.2 替换占位符

将以下占位符替换为实际值：

```jsonc
{
  "mcpServers": {
    // 智谱服务（3 个 HTTP 类型 + 1 个 stdio）
    "web-reader": {
      "type": "http",
      "url": "https://open.bigmodel.cn/api/mcp/web_reader/mcp",
      "headers": {
        "Authorization": "Bearer 你的智谱API密钥"    // ← 替换
      }
    },
    "web-search-prime": {
      "type": "http",
      "url": "https://open.bigmodel.cn/api/mcp/web_search_prime/mcp",
      "headers": {
        "Authorization": "Bearer 你的智谱API密钥"    // ← 替换
      }
    },
    "zread": {
      "type": "http",
      "url": "https://open.bigmodel.cn/api/mcp/zread/mcp",
      "headers": {
        "Authorization": "Bearer 你的智谱API密钥"    // ← 替换
      }
    },
    "zai-mcp-server": {
      "type": "stdio",
      "command": "cmd", "args": ["/c", "npx", "-y", "@z_ai/mcp-server"],
      // Linux/macOS 用: "command": "npx", "args": ["-y", "@z_ai/mcp-server"]
      "env": {
        "Z_AI_API_KEY": "你的智谱API密钥",           // ← 替换
        "Z_AI_MODE": "ZHIPU"
      }
    },

    // PDF 工具
    "mineru-mcp": {
      "type": "stdio",
      "command": "mineru-mcp-server",
      "env": {
        "MINERU_API_KEY": "你的OpenXLab_Token"        // ← 替换
      }
    },
    "pdf-mcp": {
      "type": "stdio",
      "command": "cmd", "args": ["/c", "node", "C:/Users/YOU/.claude/mcp-servers/pdf-mcp/src/server.js"],
      // Linux/macOS 用: "command": "node", "args": ["/home/YOU/.claude/mcp-servers/pdf-mcp/src/server.js"]
      "env": {}
    },

    // 知识库
    "mempalace": {
      "type": "stdio",
      // Linux/macOS:
      //   "command": "/home/YOU/anaconda3/envs/mempalace/bin/python",
      // Windows:
      "command": "C:/Users/YOU/anaconda3/envs/mempalace/python.exe",
      "args": ["-m", "mempalace.mcp_server"],
      "env": {}
    }
  }
}
```

> **Windows vs macOS/Linux**：`cmd` + `/c` 前缀仅 Windows 需要。Linux/macOS 直接写命令名即可。

### 8.3 最终验证

```bash
# 1. 重启 Claude Code（必须，MCP 配置修改后需重启）
claude

# 2. 在 Claude Code 中逐个测试：

# 测试 MinerU
> 请用 MinerU 解析一个 PDF 文件

# 测试 pdf-mcp
> 请用 pdf_info 查看 PDF 信息

# 测试网络搜索
> 请搜索 "Claude Code MCP 配置"

# 测试 MemPalace
> 请用 mempalace_status 查看 MemPalace 状态

# 3. 运行验证脚本
./scripts/verify-setup.sh
```

### 8.4 最小配置（如果只想快速体验）

如果暂时不想装全部 11 个 MCP 服务器，可以只配置 3 个核心：

```jsonc
{
  "mcpServers": {
    "mineru-mcp": {
      "type": "stdio",
      "command": "mineru-mcp-server",
      "env": { "MINERU_API_KEY": "你的OpenXLab_Token" }
    },
    "pdf-mcp": {
      "type": "stdio",
      "command": "cmd",
      "args": ["/c", "node", "C:/Users/YOU/.claude/mcp-servers/pdf-mcp/src/server.js"]
    },
    "web-search-prime": {
      "type": "http",
      "url": "https://open.bigmodel.cn/api/mcp/web_search_prime/mcp",
      "headers": { "Authorization": "Bearer 你的智谱API密钥" }
    }
  }
}
```

这 3 个覆盖了 Phase 1-2 的核心功能（论文搜索 + PDF 转换）。Phase 3-4 的工具可以后续按需添加。

---

## 故障排查

详见 [troubleshooting.md](troubleshooting.md)。

### 常见安装问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `mineru-mcp-server: command not found` | pip 未安装到当前环境 | `pip install mineru-mcp-server`，确认 `which mineru-mcp-server` 有输出 |
| `pdf-mcp server failed to start` | server.js 路径错误 | 检查 `~/.claude.json` 中路径是否正确，Windows 用正斜杠 |
| `mempalace` MCP 启动失败 | conda 环境路径错误 | 用 `conda run -n mempalace which python` 获取正确路径 |
| web-search-prime 无结果 | 智谱 Key 无效 | 检查 Key 格式（`xxx.xxx`），确认账户有免费额度 |
| npx 下载超时 | 网络问题 | 设置 `HTTPS_PROXY` 环境变量，或手动 `npm install -g` 对应包 |
| `npx` 不工作 | Node.js 不在系统 PATH | 确保 Node.js 与 npm/npx 在系统 PATH，重启终端 |

### 安全提醒

- **永远不要**将 API Key 提交到 Git
- 确保 `.gitignore` 包含 `.env`、`*.key`
- 代理环境（大学/公司网络）需配置 `NO_PROXY` 绕过 MinerU OpenXLab
