# Phase 1: Paper Search & Download

> 本阶段目标是：从 20+ 学术数据源搜索论文、下载 PDF、提取全文，为后续 PDF→Markdown 转换（Phase 2）提供原始素材。

---

## 本阶段工具

| 工具 | 用途 | 是否必需 | 链接 | 安装方式 |
|------|------|----------|------|----------|
| **paper-search-mcp** | 多源论文搜索与下载 | 是 | [openags/paper-search-mcp](https://github.com/openags/paper-search-mcp) | `uvx paper-search-mcp` |
| **Zotero** | 文献管理、元数据抓取 | 推荐 | [zotero/zotero](https://github.com/zotero/zotero) | [zotero.org](https://www.zotero.org/) 下载安装 |
| **Jasminum** | 知网等中文文献元数据 | 可选 | [l0o0/jasminum](https://github.com/l0o0/jasminum) | Zotero 插件（.xpi） |
| **translators_CN** | 中文文献库导入支持 | 可选 | [l0o0/translators_CN](https://github.com/l0o0/translators_CN) | 复制到 Zotero translators 目录 |
| **Playwright MCP** | 浏览器自动化（付费源登录下载） | 可选 | [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) | `npx -y @playwright/mcp@latest` |

---

## 安装步骤

### 1. 安装 paper-search-mcp

提供三种安装方式，按推荐顺序排列。

#### 方式 A：uvx 直接运行（推荐）

无需克隆仓库，`uv` 会自动管理虚拟环境：

```bash
# 确认 uv 已安装
uv --version

# 直接运行（首次会自动下载依赖）
uv run --with paper-search-mcp paper-search sources
```

#### 方式 B：pip 安装

```bash
pip install paper-search-mcp

# 验证
paper-search sources
```

#### 方式 C：克隆仓库（需要自定义或开发）

```bash
git clone https://github.com/openags/paper-search-mcp.git
cd paper-search-mcp
uv sync

# 验证
uv run paper-search sources
```

克隆后记录仓库路径，后续 Claude Code Skill 需要引用。

**验证命令：**

```bash
# 查看支持的学术源列表
uv run --directory /path/to/paper-search-mcp paper-search sources

# 搜索测试（arxiv 是最稳定的免费源）
uv run --directory /path/to/paper-search-mcp paper-search search "attention mechanism" -n 3 -s arxiv
```

### 2. 配置 Claude Code Skill

paper-search Skill 提供了 `/paper-search` 命令，需要在 Claude Code 中注册：

```bash
# 方式 A：使用 ai-research-toolkit 安装脚本
./scripts/install.sh --module 01-discovery

# 方式 B：直接在 ai-research-toolkit 中使用（已集成）
```

**关键步骤：编辑 SKILL.md，替换路径占位符。**

打开 `~/.claude/skills/paper-search/SKILL.md`，将所有 `<PAPER_SEARCH_MCP_PATH>` 替换为实际的 paper-search-mcp 仓库路径。

例如：

```bash
# 如果使用方式 C 克隆到了 ~/projects/paper-search-mcp
sed -i 's|<PAPER_SEARCH_MCP_PATH>|/c/Users/YOUR_USERNAME/projects/paper-search-mcp|g' \
  ~/.claude/skills/paper-search/SKILL.md

# 如果使用 uvx 运行（无本地克隆），替换为空字符串，并确保 uvx 可用
# 此时命令格式变为：uvx paper-search <command>
```

**验证：**

```bash
# 重启 Claude Code 会话，测试 Skill
# 在 Claude Code 中输入：
/paper-search search "graph neural networks" -n 3 -s arxiv
```

### 3. 安装 Zotero + Jasminum（推荐）

#### 3.1 安装 Zotero

1. 前往 [zotero.org/download](https://www.zotero.org/download/) 下载 Windows 安装包
2. 运行安装程序，默认安装即可
3. 安装浏览器 Connector（Zotero Connector 扩展），支持 Chrome/Edge/Firefox 一键保存文献

#### 3.2 安装 Jasminum（知网支持）

1. 从 [Jasminum Releases](https://github.com/l0o0/jasminum/releases) 下载最新 `.xpi` 文件
2. 打开 Zotero → 工具 → 插件 → 右上角齿轮 → Install Add-on From File
3. 选择下载的 `.xpi` 文件
4. 重启 Zotero

#### 3.3 安装 translators_CN（中文文献库）

```bash
# 克隆 translators_CN
git clone https://github.com/l0o0/translators_CN.git

# 复制到 Zotero translators 目录
# Zotero translators 目录通常在：
#   %APPDATA%\Zotero\Zotero\Profiles\*.default\translators\
# 或通过 Zotero → 编辑 → 首选项 → 高级 → 数据目录 查看

cp translators_CN/*.js "%APPDATA%/Zotero/Zotero/Profiles/"*/translators/
```

安装后在 Zotero 中刷新翻译器：编辑 → 首选项 → 高级 → 立即更新翻译器。

**验证：**

- Zotero 打开后，浏览器 Connector 图标变为可点击状态
- 在知网页面点击 Connector，确认元数据可正确抓取

---

## API Keys

### paper-search-mcp：免费优先

paper-search-mcp 采用 **FREE-FIRST** 设计：基础搜索和下载 **无需任何 API Key**。

21 个免费数据源开箱即用：arXiv、PubMed、bioRxiv、medRxiv、Semantic Scholar、CrossRef、OpenAlex、PMC、CORE、Europe PMC、DBLP、OpenAIRE、CiteSeerX、DOAJ、BASE、Zenodo、HAL、SSRN、Unpaywall、Google Scholar、IACR。

### 可选增强 Key（提升搜索质量与覆盖范围）

配置以下 API Key 后，对应数据源将获得更高的请求速率、更完整的结果或额外的元数据。**推荐至少配置 CORE 和 Semantic Scholar。**

#### 全部可配置 Key 一览

| 环境变量 | 数据源 | 推荐？ | 费用 | 获取地址 |
|----------|--------|--------|------|----------|
| `PAPER_SEARCH_MCP_CORE_API_KEY` | CORE | **推荐** | 免费 | [core.ac.uk/services/api](https://core.ac.uk/services/api) |
| `PAPER_SEARCH_MCP_SEMANTIC_SCHOLAR_API_KEY` | Semantic Scholar | **推荐** | 免费 | [semanticscholar.org/product/api](https://www.semanticscholar.org/product/api) |
| `PAPER_SEARCH_MCP_UNPAYWALL_EMAIL` | Unpaywall | 推荐 | 免费（仅需邮箱） | 直接设置你的邮箱即可 |
| `PAPER_SEARCH_MCP_DOAJ_API_KEY` | DOAJ | 可选 | 免费 | [doaj.org/api](https://doaj.org/api/docs) |
| `PAPER_SEARCH_MCP_IEEE_API_KEY` | IEEE Xplore | 可选 | 免费（需审核） | [developer.ieee.org](https://developer.ieee.org/) |
| `PAPER_SEARCH_MCP_ACM_API_KEY` | ACM Digital Library | 可选 | 需机构订阅 | [dl.acm.org](https://dl.acm.org/) |

#### 分步注册指南

##### 1. CORE API Key（推荐）

CORE 聚合了全球 3 亿+ 开放获取论文，配置 Key 后搜索结果显著增加。

1. 访问 [core.ac.uk/services/api](https://core.ac.uk/services/api)
2. 点击 "Register for API key"
3. 填写姓名、邮箱、用途（选 Research 即可）
4. 邮箱中收到 API Key（即时发放）

##### 2. Semantic Scholar API Key（推荐）

Semantic Scholar 拥有 2 亿+ 论文索引。免费用户有速率限制，配置 Key 后可提升到更高限额。

1. 访问 [semanticscholar.org/product/api](https://www.semanticscholar.org/product/api)
2. 点击 "Get API Key"
3. 填写表单（用途选 Academic Research）
4. 邮箱中收到 API Key

##### 3. Unpaywall Email（推荐）

Unpaywall 帮助定位 4700 万+ 论文的开放获取 PDF 版本，**无需注册，只需提供邮箱**（作为联系标识）。

```bash
# 直接使用你的学术邮箱
export PAPER_SEARCH_MCP_UNPAYWALL_EMAIL="your_name@university.edu"
```

##### 4. DOAJ API Key（可选）

DOAJ（开放获取期刊目录）收录 800 万+ 论文。大部分功能无需 Key，Key 用于批量访问。

1. 访问 [doaj.org/api](https://doaj.org/api/docs)
2. 按文档说明申请 API Key
3. DOAJ 的基础搜索无需 Key 即可使用

##### 5. IEEE API Key（可选，需审核）

IEEE Xplore 覆盖电气工程和计算机科学领域的优质期刊/会议论文。

1. 访问 [developer.ieee.org](https://developer.ieee.org/)
2. 注册开发者账号
3. 创建应用，选择 "IEEE Metadata API"
4. 提交后通常 1-3 个工作日审核通过
5. 收到 API Key 后配置即可

##### 6. ACM API Key（可选，需机构订阅）

ACM Digital Library 需要所在机构订阅才能获取 API Key。

1. 确认所在机构已订阅 ACM Digital Library
2. 在机构网络内访问 [dl.acm.org](https://dl.acm.org/)
3. 按照机构提供的 API 访问说明操作

#### 配置方式

**方式 A：写入 shell 配置文件（永久生效）**

```bash
# 编辑 ~/.bashrc（Git Bash）或 ~/.zshrc（macOS/Linux）
# 添加以下内容：

# --- Paper Search MCP API Keys ---
export PAPER_SEARCH_MCP_CORE_API_KEY="your_core_key"
export PAPER_SEARCH_MCP_SEMANTIC_SCHOLAR_API_KEY="your_s2_key"
export PAPER_SEARCH_MCP_UNPAYWALL_EMAIL="your_name@university.edu"
export PAPER_SEARCH_MCP_DOAJ_API_KEY="your_doaj_key"
export PAPER_SEARCH_MCP_IEEE_API_KEY="your_ieee_key"
export PAPER_SEARCH_MCP_ACM_API_KEY="your_acm_key"
```

保存后执行 `source ~/.bashrc` 生效。

**方式 B：在 MCP 配置中设置（Claude Code 自动传递）**

如果你使用 paper-search-mcp 作为 MCP 服务器运行，可以在 `~/.claude.json` 的 MCP 配置中添加环境变量：

```json
{
  "mcpServers": {
    "paper-search-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["paper-search-mcp"],
      "env": {
        "PAPER_SEARCH_MCP_CORE_API_KEY": "your_core_key",
        "PAPER_SEARCH_MCP_SEMANTIC_SCHOLAR_API_KEY": "your_s2_key",
        "PAPER_SEARCH_MCP_UNPAYWALL_EMAIL": "your_name@university.edu"
      }
    }
  }
}
```

**方式 C：在 Claude Code 会话中临时设置**

```bash
# 仅当前会话生效
export PAPER_SEARCH_MCP_CORE_API_KEY="your_core_key"
```

#### 验证 Key 是否生效

```bash
# 查看数据源状态（已配置 Key 的源会显示 "authenticated"）
/paper-search sources

# 测试 CORE 搜索
/paper-search search "computer vision" -n 3 -s core

# 测试 Semantic Scholar 搜索
/paper-search search "natural language processing" -n 3 -s semantic
```

> **推荐配置优先级：** CORE + Semantic Scholar + Unpaywall email（3 个免费，5 分钟配置完成）→ IEEE（需审核等待）→ DOAJ/ACM（视需求）

---

## 使用示例

### 示例 1：搜索论文

```bash
/paper-search search "graph neural networks" -n 10 -s arxiv,semantic
```

**参数说明：**

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 查询词 | 搜索关键词，支持英文 | 必填 |
| `-n` | 每个源返回的结果数 | 5 |
| `-s` | 数据源，逗号分隔或 `all` | all |
| `-y` | 年份过滤（仅 Semantic Scholar） | 无 |

**输出格式：** JSON 数组，包含 title、authors、year、source、DOI、abstract 等字段。

### 示例 2：下载 PDF

```bash
/paper-search download arxiv 2401.12345
```

下载指定论文的 PDF 文件。`arxiv` 是数据源名称，`2401.12345` 是论文在该源的 ID。

可选参数：

```bash
# 指定下载目录
/paper-search download arxiv 2401.12345 -o ./downloads

# 下载 Semantic Scholar 的论文（使用 SHA 或 corpusId）
/paper-search download semantic 42a8...
```

### 示例 3：提取全文

```bash
/paper-search read arxiv 2401.12345
```

直接提取论文全文文本，返回纯文本内容。适用于快速浏览摘要而不需要 PDF。

### 示例 4：查看支持的学术源

```bash
/paper-search sources
```

列出所有可用数据源及其状态（是否需要 API Key）。

---

## 支持的学术源

### 免费源（无需 API Key）

| 数据源 | ID | 说明 | 覆盖范围 |
|--------|-----|------|----------|
| **arXiv** | `arxiv` | 预印本服务器，物理/CS/Math/生物 | 200 万+ |
| **PubMed** | `pubmed` | 生物医学文献数据库 | 3500 万+ |
| **bioRxiv** | `biorxiv` | 生物学预印本 | 20 万+ |
| **medRxiv** | `medrxiv` | 医学预印本 | 20 万+ |
| **Google Scholar** | `google_scholar` | 综合学术搜索 | 全领域 |
| **Semantic Scholar** | `semantic` | AI 驱动学术搜索，2 亿+论文 | 全领域 |
| **CrossRef** | `crossref` | DOI 元数据注册中心 | 1.5 亿+ |
| **OpenAlex** | `openalex` | 开放学术目录 | 2.5 亿+ |
| **PMC** | `pmc` | PubMed Central 全文 | 900 万+ |
| **CORE** | `core` | 开放获取论文聚合 | 3 亿+ |
| **Europe PMC** | `europepmc` | 欧洲生命科学文献 | 4000 万+ |
| **DBLP** | `dblp` | 计算机科学文献 | 600 万+ |
| **OpenAIRE** | `openaire` | 欧洲开放科学基础设施 | 1 亿+ |
| **CiteSeerX** | `citeseerx` | CS/AI 文献索引 | 300 万+ |
| **DOAJ** | `doaj` | 开放获取期刊目录 | 800 万+ |
| **BASE** | `base` | 比勒费尔德学术搜索引擎 | 3 亿+ |
| **Zenodo** | `zenodo` | CERN 开放科学仓库 | 300 万+ |
| **HAL** | `hal` | 法国开放档案 | 400 万+ |
| **SSRN** | `ssrn` | 社会科学预印本 | 100 万+ |
| **Unpaywall** | `unpaywall` | 开放获取 PDF 定位 | 4700 万+ |
| **IACR** | `iacr` | 密码学 ePrint | 1.5 万+ |

### 需 Key 增强/付费源

| 数据源 | ID | 环境变量 | Key 类型 | 说明 |
|--------|-----|----------|----------|------|
| **CORE** | `core` | `PAPER_SEARCH_MCP_CORE_API_KEY` | 免费 | 推荐，显著提升结果数量 |
| **Semantic Scholar** | `semantic` | `PAPER_SEARCH_MCP_SEMANTIC_SCHOLAR_API_KEY` | 免费 | 推荐，提升速率限额 |
| **Unpaywall** | `unpaywall` | `PAPER_SEARCH_MCP_UNPAYWALL_EMAIL` | 邮箱 | 定位 OA 版 PDF |
| **DOAJ** | `doaj` | `PAPER_SEARCH_MCP_DOAJ_API_KEY` | 免费 | 批量访问增强 |
| **IEEE Xplore** | `ieee` | `PAPER_SEARCH_MCP_IEEE_API_KEY` | 免费（需审核） | 电气工程/CS 期刊会议 |
| **ACM Digital Library** | `acm` | `PAPER_SEARCH_MCP_ACM_API_KEY` | 需机构订阅 | CS 核心文献 |

### 数据源选择建议

| 场景 | 推荐源 | 理由 |
|------|--------|------|
| CS/AI 论文 | `arxiv,semantic,dblp` | 覆盖最全，响应最快 |
| 生物医学 | `pubmed,pmc,biorxiv` | PubMed 索引全面 |
| 综合搜索 | `semantic,crossref,openalex` | 跨学科覆盖 |
| 快速搜索 | `arxiv,semantic` | 延迟最低 |
| 中文文献 | Zotero + Jasminum | paper-search-mcp 不覆盖知网/万方 |

---

## 与下一阶段衔接

Phase 1 产出的 PDF 文件是 Phase 2 的输入。文件流转规则：

```
Phase 1 下载 PDF
    │
    ▼
按命名规范重命名: <AuthorYear_ShortTitle>.pdf
    │
    ▼
保存到: <OBSIDIAN_VAULT>/base/<AuthorYear_ShortTitle>/<name>_EN.pdf
    │
    ▼
Phase 2: PDF → Markdown 转换（MinerU）
```

**命名规范（严格遵守）：**

```
格式：FirstAuthorYear_ShortTitle
示例：Vaswani2017_Attention_Is_All_You_Need
禁止：纯数字、哈希、乱码、含空格的文件名
```

重命名依据（按优先级）：
1. 论文 → `FirstAuthorYear_ShortTitle`（从 PDF 内容提取）
2. 技术文档 → `项目/产品名_文档类型`
3. 无法判断 → 询问用户

---

## 常见问题

### Q1：搜索返回空结果或超时

**原因：** Google Scholar 在部分网络环境下被限制；某些源响应较慢。

**解决方案：**

```bash
# 排除 Google Scholar，使用其他综合源
/paper-search search "query" -s semantic,crossref,openalex

# 减少每个源的结果数
/paper-search search "query" -n 3 -s arxiv,semantic
```

### Q2：download 命令下载失败

**原因：** 部分论文的 PDF 需要机构访问权限，或源站点限流。

**解决方案：**

1. 检查论文是否有 Open Access 版本（`unpaywall` 源可帮助定位）
2. 使用 Playwright MCP 进行浏览器自动化下载（适用于需要登录的站点）
3. 手动在浏览器中下载后，使用 Phase 2 工具进行转换

### Q3：Windows 路径问题导致 Skill 执行失败

**原因：** Git Bash 和 Windows 路径格式不一致。

**解决方案：**

```bash
# 在 SKILL.md 中使用 Git Bash 路径格式
# Windows: C:\Users\YOUR_USERNAME\projects\paper-search-mcp
# Git Bash: /c/Users/YOUR_USERNAME/projects/paper-search-mcp

# 查找实际路径
cygpath -u "C:\Users\YOUR_USERNAME\projects\paper-search-mcp"
# 输出: /c/Users/YOUR_USERNAME/projects/paper-search-mcp
```

### Q4：中文论文搜索不到

**原因：** paper-search-mcp 主要覆盖英文文献数据库。

**解决方案：**

1. 使用 Zotero + Jasminum 从知网直接导入
2. 使用英文关键词搜索（许多中文论文有英文标题和摘要）
3. 在 Semantic Scholar 上搜索论文的英文标题

### Q5：read 命令返回的内容不完整

**原因：** `read` 命令提取的是文本层，扫描版 PDF（图片 PDF）无法直接提取。

**解决方案：**

1. 改用 `download` 命令下载 PDF，然后通过 Phase 2 的 MinerU 进行 OCR 转换
2. MinerU 支持启用 OCR 模式：`enable_ocr: true`

---

## Windows 注意事项

### Git Bash 路径格式

所有命令在 Git Bash 中执行，注意路径格式：

```bash
# 正确（Git Bash 格式）
/c/Users/YOUR_USERNAME/projects/paper-search-mcp

# 错误（Windows 格式在 Git Bash 中需要引号）
"C:\Users\YOUR_USERNAME\projects\paper-search-mcp"
```

### uv 命令路径

如果 `uv` 安装在非标准路径，确保它在 PATH 中：

```bash
# 检查 uv 位置
which uv

# 如果找不到，手动添加到 PATH
export PATH="$PATH:/c/Users/YOUR_USERNAME/.local/bin"
```

### 下载目录建议

```bash
# 建议使用 Unix 风格路径
/paper-search download arxiv 2401.12345 -o /g/obsidian/base/AuthorYear_Title

# 避免使用含空格或中文的路径
# 如果必须使用，加引号
/paper-search download arxiv 2401.12345 -o "/g/obsidian/base/Author Year Title"
```

### 编码问题

```bash
# 如果输出中文乱码，设置终端编码
export LANG=en_US.UTF-8
export LESSCHARSET=utf-8
```
