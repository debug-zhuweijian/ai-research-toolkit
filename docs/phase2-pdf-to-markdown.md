# Phase 2: PDF to Markdown

> 本阶段目标是：将 Phase 1 下载的 PDF（以及其他文档）高质量转换为 LLM 友好的 Markdown 格式，为 Phase 3 AI 分析提供结构化文本输入。

---

## 本阶段工具

| 工具 | 用途 | 是否必需 | 链接 | 安装方式 |
|------|------|----------|------|----------|
| **MinerU** | PDF→MD 核心转换引擎 | 是 | [opendatalab/MinerU](https://github.com/opendatalab/MinerU) | `pip install mineru-mcp-server` 或 CLI |
| **pdf-mcp** | PDF 读写/拆分/合并/页面提取 | 是 | [angshuman/pdf-mcp](https://github.com/angshuman/pdf-mcp) | `git clone` + `npm install` |
| **MarkItDown** | Office/图片→MD 格式转换 | 可选 | [microsoft/markitdown](https://github.com/microsoft/markitdown) | `pip install markitdown` |

---

## 安装步骤

### 1. MinerU MCP Server

MinerU 提供两种使用方式：云端 API（推荐）和本地 GPU 部署。

#### 方式 A：云端 API（推荐，零配置 GPU）

通过 MinerU MCP Server 连接 OpenXLab 云端 API，无需本地 GPU。

```bash
# 安装 MCP Server（Claude Code 已内置，无需手动安装）
# 确认 MCP 工具可用：
# mcp__mineru-mcp__parse_documents
# mcp__mineru-mcp__get_ocr_languages
```

Claude Code 中已配置 `mineru-mcp` MCP 服务器，直接使用即可。

如果需要手动配置，在 `.claude.json` 的 `mcpServers` 中添加：

```json
{
  "mineru-mcp": {
    "command": "uvx",
    "args": ["mineru-mcp-server"]
  }
}
```

#### 方式 B：本地 GPU 部署（高吞吐、离线可用）

适用于有 NVIDIA GPU（8GB+ VRAM）的环境。

```bash
# 创建独立 conda 环境（推荐）
conda create -n mineru python=3.12 -y
conda activate mineru

# 安装 MinerU
pip install mineru

# 下载模型（交互式选择）
export MINERU_MODEL_SOURCE=huggingface  # 或 modelscope（国内更快）
mineru-models-download

# 验证 CLI
mineru --version
```

**硬件需求：**

| 后端 (Backend) | 最低 VRAM | 精度 (OmniDocBench) | 说明 |
|-----------------|-----------|---------------------|------|
| `pipeline` | 4GB | 86+ | 快速，支持 CPU fallback |
| `vlm-auto-engine` | 8GB | 90+ | 高精度 |
| `hybrid-auto-engine` | 8GB | 90+ | 默认，平衡速度和精度 |
| `vlm-http-client` | 2GB | 90+ | 远程 VLM 服务 |

**验证：**

```bash
# 云端 API 方式：在 Claude Code 中测试
# 调用 mcp__mineru-mcp__parse_documents 工具
# file_sources: "test.pdf"

# 本地 CLI 方式
mineru -p test.pdf -o ./test_output
ls ./test_output/
```

### 2. pdf-mcp（PDF 操作工具）

提供 PDF 读取、拆分、合并、页面提取等操作，是 MinerU 的补充工具。

```bash
# 克隆仓库
git clone https://github.com/angshuman/pdf-mcp.git
cd pdf-mcp

# 安装依赖
npm install

# 验证
node index.js --help
```

**配置 Claude Code MCP：** 在 `.claude.json` 的 `mcpServers` 中添加：

```json
{
  "pdf-mcp": {
    "command": "node",
    "args": ["/path/to/pdf-mcp/index.js"]
  }
}
```

**验证：** Claude Code 中应可调用以下 MCP 工具：

- `mcp__pdf-mcp__pdf_info` — PDF 元数据
- `mcp__pdf-mcp__pdf_read` — 提取文本
- `mcp__pdf-mcp__pdf_split` — 拆分页面
- `mcp__pdf-mcp__pdf_merge` — 合并 PDF
- `mcp__pdf-mcp__pdf_extract_pages` — 提取指定页
- `mcp__pdf-mcp__pdf_page_to_image` — 页面渲染为图片
- `mcp__pdf-mcp__pdf_to_images` — 全部页面渲染
- `mcp__pdf-mcp__pdf_write` — 创建 PDF

### 3. MarkItDown（可选，非 PDF 文档转换）

支持 Word、Excel、PowerPoint、图片等格式转换为 Markdown。

```bash
# 安装
pip install markitdown

# 验证
markitdown --help

# 使用
markitdown input.docx > output.md
markitdown input.pptx > output.md
markitdown input.xlsx > output.md
```

**支持格式：** DOCX, PPTX, XLSX, HTML, 图片 (JPG/PNG), CSV, JSON, ZIP 等。

### 全部验证

```bash
# MinerU MCP
# 在 Claude Code 中: mcp__mineru-mcp__get_ocr_languages

# pdf-mcp
# 在 Claude Code 中: mcp__pdf-mcp__pdf_info file_path="test.pdf"

# MarkItDown（可选）
markitdown --version
```

---

## API Keys

### MinerU OpenXLab Key（云端 API）

**费用：** 免费（有调用额度限制）

**获取步骤：**

1. 前往 [openxlab.org.cn](https://openxlab.org.cn/) 注册账号
2. 登录后进入个人设置 → API Token
3. 生成 Token 并保存

**配置方式：**

```bash
# 在 MinerU MCP 的环境变量中配置
# 或在 .bashrc 中添加
export MINERU_API_KEY="your_openxlab_token"
```

> **注意：** 如果使用本地 GPU 部署（方式 B），则不需要 API Key。

### pdf-mcp 和 MarkItDown

均无需 API Key，完全本地运行。

---

## 使用示例

### 示例 1：单篇 PDF 转换（MCP 方式，推荐）

使用 Claude Code 中的 MinerU MCP 工具：

```
调用 mcp__mineru-mcp__parse_documents
参数：
  file_sources: "<OBSIDIAN_VAULT>/base/Vaswani2017_Attention/Vaswani2017_Attention_EN.pdf"
  language: "en"
  enable_ocr: false
```

或通过 Skill 命令：

```bash
/Geek-skills-mineru-pdf-parser <OBSIDIAN_VAULT>/base/Vaswani2017_Attention/Vaswani2017_Attention_EN.pdf
```

**参数说明：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file_sources` | string | 是 | 本地路径或 URL，逗号分隔多个 |
| `language` | string | 否 | `"ch"` (默认) / `"en"` |
| `enable_ocr` | boolean | 否 | `false` (默认)，扫描版 PDF 设为 `true` |
| `page_ranges` | string | 否 | `"2,4-6"` 或 `"2--2"`（从第 2 页到倒数第 2 页） |

**输出：** Markdown 文本，保留标题层级、表格、公式结构。

### 示例 2：批量转换

通过 Claude Code 批量处理一个目录下的所有 PDF：

```
1. 列出目录下所有 PDF 文件
2. 对每个文件调用 mcp__mineru-mcp__parse_documents
3. 将结果保存为对应的 .md 文件
```

本地 CLI 批量转换（适用于大量文件）：

```bash
# 激活 MinerU 环境
conda activate mineru

# 批量转换目录下所有 PDF
mineru -p /g/obsidian/base/ -o /g/obsidian/base/output/ -b pipeline

# 指定后端和语言
mineru -p ./papers/ -o ./output/ -b hybrid-auto-engine --lang en
```

### 示例 3：pdf-mcp 操作

#### 查看 PDF 信息

```
mcp__pdf-mcp__pdf_info
  file_path: "<OBSIDIAN_VAULT>/base/Author2024_Title/paper.pdf"
```

返回：页数、标题、作者、文件大小等元数据。

#### 拆分 PDF

```
mcp__pdf-mcp__pdf_split
  input_path: "<OBSIDIAN_VAULT>/base/Author2024_Title/paper.pdf"
  output_dir: "<OBSIDIAN_VAULT>/base/Author2024_Title/pages/"
```

将每页拆分为独立 PDF 文件。

#### 合并多个 PDF

```
mcp__pdf-mcp__pdf_merge
  input_paths: ["part1.pdf", "part2.pdf", "part3.pdf"]
  output_path: "merged.pdf"
```

#### 提取指定页面

```
mcp__pdf-mcp__pdf_extract_pages
  input_path: "paper.pdf"
  output_path: "pages_1_3.pdf"
  pages: [1, 2, 3]
```

页面编号从 1 开始。

#### 渲染页面为图片

```
mcp__pdf-mcp__pdf_page_to_image
  input_path: "paper.pdf"
  page: 1
  output_path: "page1.png"
  scale: 2.0
```

`scale: 1.0` = 72 DPI, `2.0` = 144 DPI (默认), `3.0` = 216 DPI。

#### 提取 PDF 文本

```
mcp__pdf-mcp__pdf_read
  file_path: "paper.pdf"
  page: 5
```

`page` 参数可选，省略则提取全部页面文本。

### 示例 4：MarkItDown 处理非 PDF 文件

```bash
# Word 文档
markitdown "report.docx" > report.md

# PowerPoint
markitdown "slides.pptx" > slides.md

# Excel
markitdown "data.xlsx" > data.md

# 图片（使用 OCR）
markitdown "scan.jpg" > scan.md
```

在 Claude Code 中也可通过 MCP 调用：

```
mcp__markitdown__convert_to_markdown
  uri: "file:///<OBSIDIAN_VAULT>/base/report.docx"
```

---

## 文件保存规则

### 目录结构

Phase 2 产出的 Markdown 文件严格按照 Obsidian vault 规范保存：

```
<OBSIDIAN_VAULT>/base/
└── <AuthorYear_ShortTitle>\
    ├── <name>_EN.pdf      ← Phase 1 下载的英文 PDF（原件）
    ├── <name>_ZH.pdf      ← 中文 PDF（如有）
    ├── <name>_EN.md       ← Phase 2 转换的英文 Markdown
    └── <name>_ZH.md       ← 中文 Markdown（如有）
```

### 命名规则

- **一个 PDF 对应一个 MD**，不要生成 `.txt` 文件
- 文件名格式：`AuthorYear_ShortTitle`（无空格，下划线连接）
- 例如：`Vaswani2017_Attention_Is_All_You_Need`

### 转换后的处理流程

```
Phase 1 PDF 下载
    │
    ▼
重命名: <AuthorYear_ShortTitle>_EN.pdf
    │
    ▼
保存到: <OBSIDIAN_VAULT>/base/<AuthorYear_ShortTitle>\
    │
    ▼
Phase 2 MinerU 转换 → <AuthorYear_ShortTitle>_EN.md
    │
    ▼
同一目录下保存 MD 文件
    │
    ▼
Phase 3: AI 分析处理 .md 文件
```

### 特殊情况

| 情况 | 处理方式 |
|------|----------|
| 扫描版 PDF | `enable_ocr: true`，支持 109 种语言 |
| 超大 PDF（100+ 页） | 使用 `page_ranges` 分段转换 |
| 含大量公式 | MinerU 自动保留 LaTeX 公式结构 |
| 含表格 | MinerU 保留 Markdown 表格格式 |
| 含图片 | MinerU 生成图片引用（不提取图片文件） |

> **已知限制：** MinerU 生成的 Markdown 中图片以引用形式存在（`![](path)`），不会自动提取嵌入图片。如需提取图片，需使用 `pdf-mcp` 的 `pdf_page_to_image` 渲染对应页面，或使用 `pypdfium2` 按坐标裁剪。

---

## 与下一阶段衔接

Phase 2 产出的 Markdown 文件是 Phase 3 的输入：

```
Phase 2 产出 .md 文件
    │
    ▼
保存到: <OBSIDIAN_VAULT>/base/<AuthorYear_ShortTitle>\<name>.md
    │
    ▼
Phase 3: AI 分析
    - /paper-review: 论文精读与评审
    - /deep-research-v5: 深度研究分析
    - /academic-writing: 学术写作辅助
    - graphify: 知识图谱构建
```

**Phase 3 可用的输入格式：**

- `.md` — Markdown 全文（Phase 2 产出）
- `.pdf` — 原始 PDF（通过 pdf-mcp 读取）
- 图片 — 页面截图（通过 pdf_page_to_image 产出）

---

## 常见问题

### Q1：MinerU 转换结果中公式乱码或丢失

**原因：** 复杂的 LaTeX 公式（如矩阵、多行公式）在转换中可能丢失结构。

**解决方案：**

1. 确保 PDF 是文本层 PDF（非扫描版），关闭 OCR 可提高公式保留率
2. 对关键公式页面，使用 `pdf_page_to_image` 渲染为图片，配合 Claude 的视觉能力阅读
3. 本地部署时尝试 `vlm-auto-engine` 后端，公式识别精度更高

### Q2：转换超时或报错

**原因：** 云端 API 有文件大小和页数限制；本地 GPU 内存不足。

**解决方案：**

```bash
# 云端方式：分段转换
# page_ranges: "1-20" 第一批
# page_ranges: "21-40" 第二批

# 本地方式：降低后端精度
mineru -p large.pdf -o output/ -b pipeline  # 4GB VRAM 即可

# 本地方式：CPU fallback
mineru -p large.pdf -o output/ --device-mode cpu
```

### Q3：pdf-mcp 的 node 命令找不到

**原因：** Node.js 未在 PATH 中，或 pdf-mcp 路径配置错误。

**解决方案：**

```bash
# 检查 Node.js
node --version

# 如果未安装，从 nodejs.org 下载 LTS 版本

# 在 .claude.json 中使用绝对路径
{
  "pdf-mcp": {
    "command": "node",
    "args": ["C:/Users/YOUR_USERNAME/projects/pdf-mcp/index.js"]
  }
}
```

### Q4：扫描版 PDF 转换质量差

**原因：** 扫描版 PDF 没有文本层，需要 OCR 识别。

**解决方案：**

1. 启用 OCR：`enable_ocr: true`
2. 指定正确语言：`language: "ch"` 或 `"en"`
3. 查看支持的语言列表：调用 `mcp__mineru-mcp__get_ocr_languages`（109 种语言）
4. 对于低质量扫描件，先用 `pdf_page_to_image` 以高 DPI (3.0x) 渲染，再使用 OCR

### Q5：转换后的 Markdown 格式不理想（表格错位、段落混乱）

**原因：** PDF 排版复杂（双栏、嵌套表格、文本框）时转换精度下降。

**解决方案：**

1. 使用本地 GPU 部署的 `vlm-auto-engine` 后端，精度从 86 提升至 90+
2. 对问题页面单独使用 `pdf_page_to_image` 渲染，配合 AI 视觉模型重新解析
3. 使用 `page_ranges` 参数对复杂页面单独处理
4. 对于关键文献，建议人工校对 Markdown 输出

---

## Windows 注意事项

### 路径格式

MinerU MCP 和 pdf-mcp 在 Windows 下均支持两种路径格式：

```bash
# Windows 路径（反斜杠或正斜杠均可）
"<OBSIDIAN_VAULT>/base/Author2024_Title/paper.pdf"
"<OBSIDIAN_VAULT>/base/Author2024_Title/paper.pdf"

# Git Bash 路径
"/g/obsidian/base/Author2024_Title/paper.pdf"
```

### 文件路径中的中文

```bash
# 如果路径含中文，确保终端编码为 UTF-8
chcp 65001  # CMD
# Git Bash 通常无需额外设置

# 在 Claude Code MCP 调用中，中文路径正常支持
file_sources: "<OBSIDIAN_VAULT>/base/张三2024_深度学习/paper.pdf"
```

### 本地 GPU 部署注意事项

```bash
# 确认 CUDA 可用
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"

# MinerU 在 Windows 上的 Python 版本限制
# 支持 Python 3.10-3.12（不支持 3.13+）
conda create -n mineru python=3.12 -y

# 如果模型下载缓慢，使用 ModelScope 镜像
export MINERU_MODEL_SOURCE=modelscope
mineru-models-download
```

### 大文件处理

```bash
# Windows 文件系统对大文件（>4GB）需要 NTFS 格式
# 检查磁盘格式
fsutil fsinfo volumeinfo C:

# 如果遇到内存不足，减少并发
# MinerU CLI 单文件处理，不会并发占用过多内存
```
