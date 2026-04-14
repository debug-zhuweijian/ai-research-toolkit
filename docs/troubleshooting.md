# Troubleshooting

## Common Issues

### MCP Server Issues

#### "mineru-mcp-server: command not found"

```bash
# Ensure mineru-mcp-server is installed
pip install mineru-mcp-server

# If using conda, make sure you're in the right environment
conda activate base
which mineru-mcp-server
```

#### "pdf-mcp server failed to start"

```bash
# Verify the path in your MCP config is correct
ls ~/.claude/mcp-servers/pdf-mcp/src/server.js

# If not found, re-clone:
git clone https://github.com/angshuman/pdf-mcp.git ~/.claude/mcp-servers/pdf-mcp
cd ~/.claude/mcp-servers/pdf-mcp && npm install
```

#### "MemPalace MCP not connecting"

```bash
# Check conda environment exists
conda env list | grep mempalace

# If not, create it:
conda create -n mempalace python=3.12
conda activate mempalace
pip install mempalace

# Verify:
python -m mempalace.mcp_server --help
```

### Claude Code Issues

#### Skills not appearing

```bash
# Verify skills directory
ls ~/.claude/skills/

# Should see: paper-search, paper-review, academic-writing, etc.

# If missing, re-copy from this repo:
cp -rn skills/* ~/.claude/skills/
```

#### Agents not appearing

```bash
# Verify agents directory
ls ~/.claude/agents/deep*

# If missing:
cp -rn agents/* ~/.claude/agents/
```

### paper-search-mcp Issues

#### "No module named paper_search_mcp"

```bash
# Install with uvx (recommended):
uvx paper-search-mcp

# Or install globally:
pip install paper-search-mcp
```

#### "Search returned 0 results"

- Check your internet connection
- Some sources may be temporarily down. Try `-s arxiv` only
- If behind a proxy, set `HTTP_PROXY` and `HTTPS_PROXY` environment variables

### MinerU Issues

#### "MINERU_API_KEY not set"

1. Register at [openxlab.org.cn](https://openxlab.org.cn)
2. Go to Settings → API Token
3. Copy the token and add to MCP config:
   ```json
   "env": { "MINERU_API_KEY": "your-token-here" }
   ```

#### PDF conversion quality poor

- MinerU cloud API handles most PDFs well
- For scanned PDFs, enable OCR: set `enable_ocr: true` in the MinerU request
- For complex layouts (multi-column, tables), results may need manual cleanup

### Knowledge Base Issues

#### "kb.js: command not found"

The kb.js knowledge base scripts are NOT included in this repo. See `scripts/knowledge-base-README.md` for setup instructions.

#### Graphify "command not found"

```bash
pip install graphifyy   # Note: double-y!
graphify install
```

### Windows-Specific Issues

#### Git Bash path issues

Git Bash uses Unix-style paths. In MCP config, use forward slashes:
- Correct: `C:/Users/yourname/.claude/mcp-servers/pdf-mcp/src/server.js`
- Wrong: `C:\Users\yourname\.claude\mcp-servers\pdf-mcp\src\server.js`

#### "cmd /c npx" not working

Make sure Node.js and npm are in your system PATH (not just Git Bash PATH).
Restart Claude Code after adding Node.js to PATH.

#### `cp -rn` not supported

On older Git Bash versions, use `cp -r --no-clobber` instead:
```bash
cp -r --no-clobber skills/* ~/.claude/skills/
```

## Still Stuck?

1. Check the [GitHub Issues](https://github.com/debug-zhuweijian/ai-research-toolkit/issues)
2. Ask in your research group chat
3. Review the detailed phase documentation in `docs/`
