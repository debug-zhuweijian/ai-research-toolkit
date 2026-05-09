#!/usr/bin/env bash
# verify-paperclip-config.sh — Validate public Paperclip template files without contacting a Paperclip service.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG="$REPO_ROOT/modules/07-pipeline/configs/paperclip.example.json"
SKILL="$REPO_ROOT/modules/07-pipeline/skills/paperclip-pipeline/SKILL.md"
REFERENCES="$REPO_ROOT/modules/07-pipeline/skills/paperclip-pipeline/references"
REFERENCE_FILES=(
  "$REFERENCES/workflow.md"
  "$REFERENCES/handoff-contract.md"
  "$REFERENCES/security-boundary.md"
  "$REFERENCES/release-sync.md"
)

fail() {
  echo "[FAIL] $1" >&2
  exit 1
}

pass() {
  echo "[PASS] $1"
}

[[ -f "$CONFIG" ]] || fail "Missing $CONFIG"
[[ -f "$SKILL" ]] || fail "Missing $SKILL"
[[ -d "$REFERENCES" ]] || fail "Missing $REFERENCES"

for ref_path in "${REFERENCE_FILES[@]}"; do
  [[ -f "$ref_path" ]] || fail "Missing reference $(basename "$ref_path")"
done

python - "$CONFIG" "$SKILL" "${REFERENCE_FILES[@]}" <<'PY'
import json
import re
import sys
from pathlib import Path

config_path = Path(sys.argv[1])
scan_paths = [Path(path) for path in sys.argv[1:]]
data = json.loads(config_path.read_text(encoding="utf-8"))

required = {
    "paperclip_url",
    "auth",
    "workspace",
    "pipeline_mode",
    "allowed_outputs",
    "forbidden_outputs",
    "handoff_required_fields",
}
missing = sorted(required - data.keys())
if missing:
    raise SystemExit(f"Missing config keys: {missing}")

expected_placeholders = {
    "paperclip_url": "<PAPERCLIP_API_URL>",
    "auth": "<PAPERCLIP_AUTH_METHOD>",
    "workspace": "<PUBLIC_WORKSPACE_NAME>",
}
for key, expected in expected_placeholders.items():
    if data.get(key) != expected:
        raise SystemExit(f"{key} must be {expected!r}")

if data.get("pipeline_mode") != "template-only":
    raise SystemExit("pipeline_mode must be 'template-only'")

required_handoff = {
    "task_objective",
    "files_read",
    "files_modified",
    "commands_run",
    "evidence",
    "open_risks",
    "next_step",
}
actual_handoff = set(data.get("handoff_required_fields", []))
missing_handoff = sorted(required_handoff - actual_handoff)
if missing_handoff:
    raise SystemExit(f"Missing handoff fields: {missing_handoff}")

forbidden_patterns = [
    r"sk-[A-Za-z0-9_-]{20,}",
    r'(?i)"(?:[A-Za-z0-9_-]*api[_-]?key|[A-Za-z0-9_-]*token|[A-Za-z0-9_-]*cookie|[A-Za-z0-9_-]*password|[A-Za-z0-9_-]*secret|[A-Za-z0-9_-]*credentials?)"\s*:\s*"(?!<[^>]+>)[A-Za-z0-9_./+=-]{8,}"',
    r"(?i)(api[_-]?key|token|cookie|password|secret|credentials?)\s*[:=]\s*[\"']?[A-Za-z0-9_./+=-]{8,}[\"']?",
    r"(?i)bearer\s+[A-Za-z0-9_./+=-]{8,}",
    r"(?<![A-Za-z])[A-Za-z]:[\\/]",
    r"/Users/[^\"\s]+",
    r"/home/[^\"\s]+",
    r"https?://(localhost|127\.0\.0\.1|10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.)",
    r'(?i)"(?:workspace|team|job)[_-]?ids?"\s*:\s*"(?!<[^>]+>)[A-Za-z0-9_-]{4,}"',
    r"(?i)(workspace|team|job)[_-]?ids?\s*[:=]\s*[\"']?[A-Za-z0-9_-]{4,}[\"']?",
]
for path in scan_paths:
    text = path.read_text(encoding="utf-8")
    for pattern in forbidden_patterns:
        if re.search(pattern, text):
            raise SystemExit(f"Forbidden private-looking value matched in {path}: {pattern}")
PY

pass "Paperclip template files are public-safe"
pass "Paperclip references are present"
pass "Paperclip skill files verified"
