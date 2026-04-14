# install-skills.ps1 — PowerShell version of install-skills.sh
# Usage: .\scripts\install-skills.ps1 [-SkillsPath ~/.claude/skills] [-AgentsPath ~/.claude/agents]

param(
    [string]$SkillsPath = "$env:USERPROFILE\.claude\skills",
    [string]$AgentsPath = "$env:USERPROFILE\.claude\agents"
)

$RepoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

Write-Host "=== AI Research Toolkit — Install Skills & Agents ===" -ForegroundColor Cyan
Write-Host "Skills target: $SkillsPath"
Write-Host "Agents target: $AgentsPath"
Write-Host ""

# Create directories
New-Item -ItemType Directory -Force -Path $SkillsPath | Out-Null
New-Item -ItemType Directory -Force -Path $AgentsPath | Out-Null

# Copy skills
Write-Host "--- Installing Skills ---" -ForegroundColor Yellow
$skillCount = 0
Get-ChildItem -Directory -Path "$RepoRoot\skills" | ForEach-Object {
    $dest = Join-Path $SkillsPath $_.Name
    if (Test-Path $dest) {
        Write-Host "  [SKIP] $($_.Name) (already exists)" -ForegroundColor Gray
    } else {
        Copy-Item -Recurse $_.FullName $dest
        Write-Host "  [INSTALLED] $($_.Name)" -ForegroundColor Green
        $skillCount++
    }
}
Write-Host "Installed $skillCount new skills."

# Copy agents
Write-Host ""
Write-Host "--- Installing Agents ---" -ForegroundColor Yellow
$agentCount = 0
Get-ChildItem -File -Path "$RepoRoot\agents" -Filter "*.md" | ForEach-Object {
    $dest = Join-Path $AgentsPath $_.Name
    if (Test-Path $dest) {
        Write-Host "  [SKIP] $($_.Name) (already exists)" -ForegroundColor Gray
    } else {
        Copy-Item $_.FullName $dest
        Write-Host "  [INSTALLED] $($_.Name)" -ForegroundColor Green
        $agentCount++
    }
}
Write-Host "Installed $agentCount new agents."

Write-Host ""
Write-Host "=== Path Placeholders ===" -ForegroundColor Cyan
Write-Host @"
Some skills contain placeholders you need to customize:

  <PAPER_SEARCH_MCP_PATH>  -> Path to paper-search-mcp
  <KB_SCRIPTS_PATH>        -> Path to knowledge base scripts
  <KNOWLEDGE_BASE_PATH>    -> Path to your knowledge base
  <OBSIDIAN_VAULT>         -> Path to your Obsidian vault

Edit the SKILL.md files in $SkillsPath to replace these placeholders.
"@
