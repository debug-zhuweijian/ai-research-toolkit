# install.ps1 — Install skills and agents from selected modules/profile.

[CmdletBinding()]
param(
    [ValidateSet("minimal", "knowledge", "full")]
    [string]$Profile,

    [string[]]$Module,

    [string]$SkillsPath = "$env:USERPROFILE\.claude\skills",

    [string]$AgentsPath = "$env:USERPROFILE\.claude\agents",

    [switch]$Force,

    [switch]$List
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$ModulesRoot = Join-Path $RepoRoot "modules"

function Get-ProfileModules {
    param([string]$Name)

    switch ($Name) {
        "minimal"   { return @("01-discovery", "02-processing") }
        "knowledge" { return @("05-knowledge", "06-presentation") }
        "full"      { return @("01-discovery", "02-processing", "03-analysis", "04-writing", "05-knowledge", "06-presentation") }
        default     { throw "Unknown profile: $Name" }
    }
}

function Get-ModuleSummary {
    Get-ChildItem $ModulesRoot -Directory | Sort-Object Name | ForEach-Object {
        $skillCount = (Get-ChildItem (Join-Path $_.FullName "skills") -Directory -ErrorAction SilentlyContinue | Measure-Object).Count
        $agentCount = (Get-ChildItem (Join-Path $_.FullName "agents") -File -Filter "*.md" -ErrorAction SilentlyContinue | Measure-Object).Count
        [PSCustomObject]@{
            Name = $_.Name
            Skills = $skillCount
            Agents = $agentCount
        }
    }
}

if ($List) {
    Write-Host "Profiles:" -ForegroundColor Cyan
    Write-Host "  minimal   -> 01-discovery, 02-processing"
    Write-Host "  knowledge -> 05-knowledge, 06-presentation"
    Write-Host "  full      -> 01-discovery, 02-processing, 03-analysis, 04-writing, 05-knowledge, 06-presentation"
    Write-Host ""
    Write-Host "Modules:" -ForegroundColor Cyan
    Get-ModuleSummary | ForEach-Object {
        Write-Host ("  {0} (skills: {1}, agents: {2})" -f $_.Name, $_.Skills, $_.Agents)
    }
    return
}

if ($Profile -and $Module) {
    throw "--Profile and -Module cannot be used together."
}

if (-not $Profile -and (-not $Module -or $Module.Count -eq 0)) {
    $Profile = "full"
}

$RequestedModules = @()
if ($Profile) {
    $RequestedModules = @(Get-ProfileModules -Name $Profile)
} else {
    $RequestedModules = @($Module)
}

$SeenModules = @{}
$OrderedModules = New-Object System.Collections.Generic.List[string]
foreach ($ModuleName in $RequestedModules) {
    $ModulePath = Join-Path $ModulesRoot $ModuleName
    if (-not (Test-Path $ModulePath -PathType Container)) {
        throw "Unknown module: $ModuleName. Run .\scripts\install.ps1 -List to see valid modules."
    }
    if (-not $SeenModules.ContainsKey($ModuleName)) {
        $SeenModules[$ModuleName] = $true
        $null = $OrderedModules.Add($ModuleName)
    }
}

New-Item -ItemType Directory -Force -Path $SkillsPath | Out-Null
New-Item -ItemType Directory -Force -Path $AgentsPath | Out-Null

Write-Host "=== AI Research Toolkit — Install Skills & Agents ===" -ForegroundColor Cyan
Write-Host "Repo root: $RepoRoot"
if ($Profile) {
    Write-Host "Profile: $Profile"
} else {
    Write-Host "Modules: $($OrderedModules -join ', ')"
}
Write-Host "Skills target: $SkillsPath"
Write-Host "Agents target: $AgentsPath"
Write-Host "Force overwrite: $($Force.IsPresent)"
Write-Host ""

$SkillsInstalled = 0
$SkillsSkipped = 0
$AgentsInstalled = 0
$AgentsSkipped = 0

foreach ($ModuleName in $OrderedModules) {
    $ModulePath = Join-Path $ModulesRoot $ModuleName
    $SkillDirs = @(Get-ChildItem (Join-Path $ModulePath "skills") -Directory -ErrorAction SilentlyContinue)
    $AgentFiles = @(Get-ChildItem (Join-Path $ModulePath "agents") -File -Filter "*.md" -ErrorAction SilentlyContinue)

    if ($SkillDirs.Count -eq 0 -and $AgentFiles.Count -eq 0) {
        throw "Module $ModuleName has no installable skills or agents."
    }

    Write-Host "--- $ModuleName ---" -ForegroundColor Yellow

    foreach ($SkillDir in $SkillDirs) {
        $Destination = Join-Path $SkillsPath $SkillDir.Name
        if (Test-Path $Destination) {
            if ($Force) {
                Remove-Item -LiteralPath $Destination -Recurse -Force
                Copy-Item -LiteralPath $SkillDir.FullName -Destination $Destination -Recurse
                Write-Host "  [UPDATED] skill: $($SkillDir.Name)" -ForegroundColor Green
                $SkillsInstalled++
            } else {
                Write-Host "  [SKIP] skill: $($SkillDir.Name)" -ForegroundColor DarkGray
                $SkillsSkipped++
            }
        } else {
            Copy-Item -LiteralPath $SkillDir.FullName -Destination $Destination -Recurse
            Write-Host "  [INSTALLED] skill: $($SkillDir.Name)" -ForegroundColor Green
            $SkillsInstalled++
        }
    }

    foreach ($AgentFile in $AgentFiles) {
        $Destination = Join-Path $AgentsPath $AgentFile.Name
        if (Test-Path $Destination) {
            if ($Force) {
                Copy-Item -LiteralPath $AgentFile.FullName -Destination $Destination -Force
                Write-Host "  [UPDATED] agent: $($AgentFile.Name)" -ForegroundColor Green
                $AgentsInstalled++
            } else {
                Write-Host "  [SKIP] agent: $($AgentFile.Name)" -ForegroundColor DarkGray
                $AgentsSkipped++
            }
        } else {
            Copy-Item -LiteralPath $AgentFile.FullName -Destination $Destination
            Write-Host "  [INSTALLED] agent: $($AgentFile.Name)" -ForegroundColor Green
            $AgentsInstalled++
        }
    }

    Write-Host ""
}

Write-Host "=== Summary ===" -ForegroundColor Cyan
Write-Host "Skills installed/updated: $SkillsInstalled"
Write-Host "Skills skipped: $SkillsSkipped"
Write-Host "Agents installed/updated: $AgentsInstalled"
Write-Host "Agents skipped: $AgentsSkipped"
Write-Host ""
Write-Host "Skills with path placeholders may still require customization:" -ForegroundColor Cyan
Write-Host "  <PAPER_SEARCH_MCP_PATH>"
Write-Host "  <OBSIDIAN_VAULT>"
Write-Host "  <KNOWLEDGE_BASE_PATH>"
Write-Host "  <KB_SCRIPTS_PATH>"
Write-Host "  <DRAWIO_OUTPUT_DIR>"
Write-Host ""
Write-Host "Run ./scripts/verify-setup.sh to verify core dependencies and install targets."
