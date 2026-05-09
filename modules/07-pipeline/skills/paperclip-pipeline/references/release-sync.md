# Paperclip Release Sync Protocol

The debug repository is the working source. The release repository is a sanitized public mirror. Do not mirror the whole debug repository.

## Allowed Sync Paths

- `modules/07-pipeline/`
- `scripts/`
- `configs/`
- `docs/`
- `profiles/`
- `README.md`
- `README.zh-CN.md`
- `README.ja.md`
- `README.ko.md`
- `CHANGELOG.md`
- `LICENSE`
- `.github/workflows/release.yml`

## Forbidden Sync Paths

- Top-level `skills/`
- Top-level `agents/`
- `.coverage/`
- `htmlcov/`
- `.env`
- Logs, caches, runtime state, and private Paperclip job data.

## Sync Flow

1. Finish debug optimization in the debug repository.
2. Run debug verification.
3. Run secret and path scans.
4. Copy only whitelisted files.
5. Run release repository verification.
6. Inspect `git diff --stat` and `git diff --name-status`.
7. Run release repository secret and path scans.
8. Review README, CHANGELOG, and release notes for public accuracy.
9. Commit and tag only after all checks pass.

## Conflict Rule

If the release repository has a newer script than the debug repository, keep the release script as baseline and patch only the Paperclip-specific behavior into it.
