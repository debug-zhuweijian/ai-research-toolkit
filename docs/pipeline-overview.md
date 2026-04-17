# Pipeline Overview

## Full Workflow

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Phase 1     │     │  Phase 2     │     │  Phase 3      │     │  Phase 4     │     │  Phase 4+    │     │  Output      │
│  Paper       │────▶│  PDF → MD    │────▶│  AI Analysis  │────▶│  Knowledge   │────▶│  Knowledge   │────▶│  Academic    │
│  Search &    │     │  Conversion  │     │  & Writing    │     │  Base        │     │  Graph       │     │  Writing     │
│  Download    │     │              │     │               │     │              │     │              │     │  & PPT       │
└─────────────┘     └──────────────┘     └───────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
       │                    │                     │                     │                     │
   paper-search         MinerU              paper-review          knowledge-base        graphify
   Zotero+Jasminum      pdf-mcp             deep-research-v5      MemPalace             (HTML可视化)
   Playwright MCP       MarkItDown          academic-writing      ChromaDB
                                             web-search-prime      Obsidian
                                             web-reader
                                             zai-mcp-server
```

## Tool Mapping

| Phase | Tool | Type | Source |
|-------|------|------|--------|
| **1. Search** | paper-search-mcp | MCP + Skill | [openags/paper-search-mcp](https://github.com/openags/paper-search-mcp) |
| | Zotero + Jasminum | Desktop App | [zotero/zotero](https://github.com/zotero/zotero) |
| | Playwright MCP | MCP | [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) |
| **2. Convert** | MinerU MCP | MCP | [opendatalab/MinerU](https://github.com/opendatalab/MinerU) |
| | pdf-mcp | MCP | [angshuman/pdf-mcp](https://github.com/angshuman/pdf-mcp) |
| | MarkItDown | MCP | [microsoft/markitdown](https://github.com/microsoft/markitdown) |
| **3. Analyze** | paper-review | Skill | Custom (this repo) |
| | deep-research-v5 | Skill | Custom (this repo) |
| | academic-writing | Skill | Custom (this repo) |
| | Sequential Thinking | MCP | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) |
| | web-search-prime | MCP | Zhipu BigModel |
| | web-reader | MCP | Zhipu BigModel |
| | zai-mcp-server | MCP | Zhipu Z.AI |
| **4. Knowledge** | knowledge-base | Skill | Custom (this repo) |
| | Graphify | CLI + Skill | [safishamsi/graphify](https://github.com/safishamsi/graphify) |
| | MemPalace | MCP | [MemPalace/mempalace](https://github.com/MemPalace/mempalace) |
| | ChromaDB | Backend | [chroma-core/chroma](https://github.com/chroma-core/chroma) |
| | Obsidian | Desktop App | [obsidian.md](https://obsidian.md) |
| **Output** | academic-pptx | Skill | Custom (this repo) |
| | group-meeting-slides | Skill | Custom (this repo) |

## Data Flow

```
User Query
    ↓
paper-search → PDF files → MinerU → Markdown files
    ↓                                    ↓
    └───────────────────→ AI Analysis ←──┘
                              ↓
                    /paper-review → Structured Report
                    /deep-research-v5 → Cited Survey
                    /academic-writing → Draft Text
                              ↓
                    Knowledge Base (/knowledge-base sync)
                              ↓
                    Graphify → Interactive Knowledge Graph
                              ↓
                    /academic-pptx → Presentation Slides
```
