# MinerU 3.0 Reference

## MCP Tool (Recommended)

### parse_documents

将文档转换为 Markdown/JSON。

**参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file_sources` | string | 是 | 本地路径或 URL（逗号分隔多个） |
| `language` | string | 否 | `"ch"` (默认) / `"en"` |
| `enable_ocr` | boolean | 否 | `false` (默认) |
| `page_ranges` | string | 否 | `"2,4-6"` 或 `"2--2"` |

**支持格式:** PDF, PPT, PPTX, DOC, DOCX, JPG, JPEG, PNG

**输出:** Markdown 文本

### get_ocr_languages

获取 OCR 支持的语言列表（109 种语言）。

## CLI Reference (MinerU 3.0.x)

### 基本用法

```bash
mineru -p <input> -o <output_dir> [options]
```

### 关键选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `-p, --path` | - | 输入文件或目录 |
| `-o, --output-dir` | - | 输出目录 |
| `-b, --backend` | `hybrid-auto-engine` | 解析后端 |
| `--lang` | 自动检测 | 文档语言 |
| `--device-mode` | `cuda` | `cuda` / `cpu` |

### Backend 值

- `pipeline` — 快速，CPU/GPU，4GB VRAM min
- `vlm-auto-engine` — 高精度，90+ OmniDocBench
- `vlm-http-client` — 远程 VLM（2GB VRAM）
- `hybrid-auto-engine` — 默认，混合方案
- `hybrid-http-client` — 远程混合

**注意:** 旧值 `vlm`、`hybrid` 已废弃，必须使用 `*-auto-engine` 或 `*-http-client`。

### 模型管理

```bash
# 设置模型源
export MINERU_MODEL_SOURCE=huggingface  # 或 modelscope

# 下载模型（交互式）
mineru-models-download

# 模型配置写入 ~/mineru.json
```

### API Server 模式

```bash
# 启动 FastAPI 服务
mineru-api --host 0.0.0.0 --port 8000

# REST 端点
POST /file_parse          # 同步解析
POST /tasks               # 异步任务
GET  /tasks/{task_id}     # 查询任务状态
```

## 版本信息

- **当前版本:** 3.0.4 (2026-04)
- **Python 支持:** 3.10-3.13 (Linux/macOS), 3.10-3.12 (Windows)
- **VRAM 最低:** pipeline 4GB, VLM/hybrid 8GB
- **RAM 最低:** 16GB, 推荐 32GB+
- **GPU:** Volta 及以后（RTX 3080 OK）
