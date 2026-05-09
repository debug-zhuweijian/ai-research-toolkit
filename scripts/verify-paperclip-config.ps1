# verify-paperclip-config.ps1 — Validate public Paperclip template files without contacting a Paperclip service.
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$Config = Join-Path $RepoRoot "modules/07-pipeline/configs/paperclip.example.json"
$Skill = Join-Path $RepoRoot "modules/07-pipeline/skills/paperclip-pipeline/SKILL.md"
$References = Join-Path $RepoRoot "modules/07-pipeline/skills/paperclip-pipeline/references"
$ReferenceFiles = @(
  (Join-Path $References "workflow.md"),
  (Join-Path $References "handoff-contract.md"),
  (Join-Path $References "security-boundary.md"),
  (Join-Path $References "release-sync.md")
)

function Fail($Message) {
  Write-Error "[FAIL] $Message"
  exit 1
}

function Pass($Message) {
  Write-Output "[PASS] $Message"
}

if (!(Test-Path $Config)) { Fail "Missing $Config" }
if (!(Test-Path $Skill)) { Fail "Missing $Skill" }
if (!(Test-Path $References)) { Fail "Missing $References" }

foreach ($RefPath in $ReferenceFiles) {
  if (!(Test-Path $RefPath)) { Fail "Missing reference $(Split-Path -Leaf $RefPath)" }
}

$Raw = Get-Content $Config -Raw -Encoding UTF8
$Data = $Raw | ConvertFrom-Json

$Required = @(
  "paperclip_url",
  "auth",
  "workspace",
  "pipeline_mode",
  "allowed_outputs",
  "forbidden_outputs",
  "handoff_required_fields"
)

$Names = $Data.PSObject.Properties.Name
foreach ($Key in $Required) {
  if ($Names -notcontains $Key) { Fail "Missing config key: $Key" }
}

if ($Data.paperclip_url -ne "<PAPERCLIP_API_URL>") { Fail "paperclip_url must be <PAPERCLIP_API_URL>" }
if ($Data.auth -ne "<PAPERCLIP_AUTH_METHOD>") { Fail "auth must be <PAPERCLIP_AUTH_METHOD>" }
if ($Data.workspace -ne "<PUBLIC_WORKSPACE_NAME>") { Fail "workspace must be <PUBLIC_WORKSPACE_NAME>" }
if ($Data.pipeline_mode -ne "template-only") { Fail "pipeline_mode must be template-only" }

$RequiredHandoff = @(
  "task_objective",
  "files_read",
  "files_modified",
  "commands_run",
  "evidence",
  "open_risks",
  "next_step"
)
foreach ($Field in $RequiredHandoff) {
  if ($Data.handoff_required_fields -notcontains $Field) { Fail "Missing handoff field: $Field" }
}

$ForbiddenPatterns = @(
  'sk-[A-Za-z0-9_-]{20,}',
  '(?i)"(?:[A-Za-z0-9_-]*api[_-]?key|[A-Za-z0-9_-]*token|[A-Za-z0-9_-]*cookie|[A-Za-z0-9_-]*password|[A-Za-z0-9_-]*secret|[A-Za-z0-9_-]*credentials?)"\s*:\s*"(?!<[^>]+>)[A-Za-z0-9_./+=-]{8,}"',
  '(?i)(api[_-]?key|token|cookie|password|secret|credentials?)\s*[:=]\s*["'']?[A-Za-z0-9_./+=-]{8,}["'']?',
  '(?i)bearer\s+[A-Za-z0-9_./+=-]{8,}',
  '(?<![A-Za-z])[A-Za-z]:[\\/]',
  '/Users/[^`"\s]+',
  '/home/[^`"\s]+',
  'https?://(localhost|127\.0\.0\.1|10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.)',
  '(?i)"(?:workspace|team|job)[_-]?ids?"\s*:\s*"(?!<[^>]+>)[A-Za-z0-9_-]{4,}"',
  '(?i)(workspace|team|job)[_-]?ids?\s*[:=]\s*["'']?[A-Za-z0-9_-]{4,}["'']?'
)

$ScanFiles = @($Config, $Skill) + $ReferenceFiles
foreach ($ScanFile in $ScanFiles) {
  $ScanText = Get-Content $ScanFile -Raw -Encoding UTF8
  foreach ($Pattern in $ForbiddenPatterns) {
    if ($ScanText -match $Pattern) { Fail "Forbidden private-looking value matched in ${ScanFile}: $Pattern" }
  }
}

Pass "Paperclip template files are public-safe"
Pass "Paperclip references are present"
Pass "Paperclip skill files verified"
