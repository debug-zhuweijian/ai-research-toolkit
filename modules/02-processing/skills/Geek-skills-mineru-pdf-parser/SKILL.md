---
name: Geek-skills-mineru-pdf-parser
version: 2.0.0
description: PDF解析工具，将PDF转换为LLM友好的Markdown格式
---
# MinerU PDF Parser

将 PDF 文档转换为 Markdown 格式。

## 推荐方式：MCP 工具

使用 `mcp__mineru-mcp__parse_documents` 工具（已配置，无需本地安装）：

```
参数:
  file_sources: "/path/to/file.pdf" 或 URL（支持 PDF/PPT/PPTX/DOC/DOCX/图片）
  language: "ch" | "en"（默认 "ch"）
  enable_ocr: true | false（默认 false）
  page_ranges: "2,4-6"（可选，指定页码范围）

输出: Markdown 文本
```

保存结果到 Obsidian vault: `G:\obsidian\Papers\<AuthorYear_ShortTitle>\<name>.md`

## 备选方式：CLI

MinerU 3.0 使用 client-server 架构：

```bash
# 解析 PDF（默认 hybrid-auto-engine 模式）
mineru -p input.pdf -o output_dir

# 指定 backend
mineru -p input.pdf -o output_dir -b pipeline       # 快速，4GB VRAM
mineru -p input.pdf -o output_dir -b vlm-auto-engine # 高精度，8GB VRAM
```

### Backend 选项

| Backend | VRAM | 精度 | 说明 |
|---------|------|------|------|
| `pipeline` | 4GB | 86+ | 快速，支持 CPU fallback |
| `vlm-auto-engine` | 8GB | 90+ | 高精度 |
| `hybrid-auto-engine` | 8GB | 90+ | 默认，平衡 |
| `vlm-http-client` | 2GB | 90+ | 远程 VLM 服务 |

### 模型下载

```bash
export MINERU_MODEL_SOURCE=huggingface  # 或 modelscope
mineru-models-download  # 交互式选择
```

## 参考

见 [references/mineru_v3_reference.md](references/mineru_v3_reference.md)
