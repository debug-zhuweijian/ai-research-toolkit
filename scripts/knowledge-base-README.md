# Knowledge Base Scripts

The knowledge base management scripts (`kb.js`) are NOT included in this repository due to uncertain licensing.

## What kb.js Does

`kb.js` is a Node.js script that manages the knowledge base pipeline:

| Command | Purpose |
|---------|---------|
| `scan` | Scan source directory for new materials |
| `apply` | Ingest new materials into knowledge base |
| `lint` | Run 8 health checks |
| `index` | Regenerate wiki/index.md |
| `stats` | Print current statistics |

## How to Get kb.js

### Option 1: Build Your Own

The kb.js script is a relatively simple Node.js CLI that:
1. Scans a source directory for new files
2. Copies/syncs them to a target knowledge base directory
3. Runs health checks on the knowledge base structure
4. Maintains statistics

You can create a similar script using:
- `fs.watch` for file monitoring
- `chokidar` for cross-platform file watching
- Simple `fs.cpSync` for file copying

### Option 2: Use Graphify Instead

[Graphify](https://github.com/safishamsi/graphify) can serve a similar purpose:
```bash
pip install graphifyy
graphify install
graphify <your-directory>
```

Graphify will scan your files, build a knowledge graph, and generate interactive visualizations.

### Option 3: Manual Management

Without kb.js, you can manually manage your knowledge base:
1. Copy new Markdown files to your knowledge base's `raw/articles/` directory
2. Run `graphify <knowledge-base-path>` to update the knowledge graph
3. Use Obsidian to browse and search your notes

## Knowledge Base Directory Structure

```
<YOUR_KNOWLEDGE_BASE>/
├── wiki/
│   ├── concepts/      # Concept pages
│   └── summaries/     # Summary pages
├── raw/
│   └── articles/      # Source articles (Markdown)
└── .graphify-data/
    └── graph.json     # Knowledge graph data
```
