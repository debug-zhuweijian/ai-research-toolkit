# Paperclip Handoff Contract

Every agent or sub-task must return a complete handoff packet. Incomplete handoffs are not accepted.

## Required Fields

```yaml
task_objective: "What this agent was asked to accomplish"
files_read:
  - "relative/path/read.md"
files_modified:
  - "relative/path/modified.md"
commands_run:
  - command: "command that was run"
    outcome: "pass, fail, or blocked"
evidence:
  - "specific output, file path, diff, or verification result"
assumptions:
  - "explicit assumption made during work"
open_risks:
  - "remaining risk or empty list"
next_step: "recommended next action"
```

## Acceptance Rules

- `task_objective` must match the assigned task.
- `files_read` and `files_modified` must use repository-relative paths.
- `commands_run` must include enough detail to reproduce the verification.
- `evidence` must point to observable artifacts or command output.
- `open_risks` must not hide blockers.
- `next_step` must be concrete.

## Coordinator Review

The coordinator must verify changed files and critical command outputs directly. A handoff summary is evidence to inspect, not proof by itself.
