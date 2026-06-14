#!/usr/bin/env python3
"""Extract a single release section from the committed changelog."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def normalize_tag(tag: str) -> str:
    return tag[1:] if tag.startswith("v") else tag


def section_pattern(version: str) -> re.Pattern[str]:
    escaped = re.escape(version)
    return re.compile(rf"^## \[(?:v)?{escaped}\](?:\s+-\s+.*)?$", re.MULTILINE)


def extract_section(changelog: str, tag: str) -> str:
    version = normalize_tag(tag)
    match = section_pattern(version).search(changelog)
    if not match:
        raise ValueError(f"CHANGELOG.md has no section for {tag}")

    start = match.start()
    next_match = re.search(r"^## \[", changelog[match.end() :], re.MULTILINE)
    end = match.end() + next_match.start() if next_match else len(changelog)
    section = changelog[start:end].strip()
    if not section:
        raise ValueError(f"CHANGELOG.md section for {tag} is empty")
    return section + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract release notes from CHANGELOG.md.")
    parser.add_argument("--tag", required=True, help="release tag, for example v0.3.0-beta.2")
    parser.add_argument(
        "--changelog",
        default=str(ROOT / "CHANGELOG.md"),
        help="path to the committed changelog",
    )
    parser.add_argument("--output", required=True, help="path to write release notes")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    changelog_path = Path(args.changelog)
    output_path = Path(args.output)
    try:
        notes = extract_section(changelog_path.read_text(encoding="utf-8"), args.tag)
    except (OSError, ValueError) as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(notes, encoding="utf-8")
    print(f"Release notes written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
