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

# Should see installed skills such as paper-search, knowledge-base, drawio, etc.

# Reinstall with the repo installer:
./scripts/install.sh --profile full
```

Use `./scripts/install.sh --list` or `.\scripts\install.ps1 -List` to confirm the five supported profiles: `minimal`, `researcher`, `writer`, `knowledge`, and `full`. The `full` profile installs Phase 01 through Phase 07, including the active beta `07-pipeline` module.

#### Agents not appearing

```bash
# Verify agents directory
ls ~/.claude/agents/

# Reinstall with the repo installer:
./scripts/install.sh --profile full
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

#### "npx" not working

Make sure Node.js and npm are in your system PATH (not just Git Bash PATH).
Restart Claude Code after adding Node.js to PATH.

#### `cp -rn` not supported

Use the installer instead of manual copy:
```bash
./scripts/install.sh --profile full
```

### Release and Public Safety Issues

#### Beta release appears as Latest

Alpha, beta, and rc tags should publish as GitHub prereleases and should not become Latest. If a beta release metadata state looks wrong:

1. Check `.github/workflows/release.yml` contains `prerelease` and `make_latest`.
2. Check the release by tag with GitHub CLI or API.
3. Patch only release metadata fields from the real release id; do not delete/recreate the release and do not rewrite the tag.

#### Public safety scan blocks a commit or release

The scanner intentionally reports only path, line, category, and severity. It does not print the matched secret value.

```bash
python scripts/scan-public-safety.py --staged
python scripts/scan-public-safety.py --tree
```

Use placeholders such as `<ANTHROPIC_API_KEY>`, `<BIGMODEL_API_KEY>`, `<MINERU_API_KEY>`, and `<ANTHROPIC_COMPATIBLE_BASE_URL>` in public docs and templates.

## Still Stuck?

1. Check the [GitHub Issues](https://github.com/debug-zhuweijian/ai-research-toolkit/issues)
2. Ask in your research group chat
3. Review the detailed phase documentation in `docs/`
