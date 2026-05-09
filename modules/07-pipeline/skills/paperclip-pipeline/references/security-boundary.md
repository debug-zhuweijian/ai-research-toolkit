# Paperclip Security Boundary

Public toolkit content may describe the Paperclip workflow, but must not expose private runtime details.

## Public Content

Allowed public content:

- Workflow descriptions.
- Handoff templates.
- Placeholder-only config examples.
- Verification scripts that inspect templates without contacting private services.
- Release-safe README, CHANGELOG, docs, modules, configs, and scripts.

## Private Content

Forbidden public content:

- API keys, tokens, cookies, passwords, private keys, and secrets.
- Real service URLs, internal URLs, IP addresses, ports, database strings, OAuth values, team IDs, workspace IDs, and job IDs.
- Local absolute paths, user home directories, real Obsidian paths, real Zotero paths, and private Paperclip paths.
- Runtime logs, cache files, coverage outputs, local task records, and deployment configs.

## Sanitization Rules

Use placeholders for any runtime value:

| Private value | Public placeholder |
| --- | --- |
| Paperclip API URL | `<PAPERCLIP_API_URL>` |
| Auth mode or token | `<PAPERCLIP_AUTH_METHOD>` |
| Workspace name | `<PUBLIC_WORKSPACE_NAME>` |
| Local project path | `<PROJECT_PATH>` |
| Private output directory | `<OUTPUT_DIR>` |

If a value can identify the user's machine, account, private service, or runtime state, do not publish it.
