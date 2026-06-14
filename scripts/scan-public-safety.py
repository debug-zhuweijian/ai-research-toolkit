#!/usr/bin/env python3
"""Scan public repository content for sensitive values without printing them."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


TEXT_EXTENSIONS = {
    ".bash",
    ".bat",
    ".cfg",
    ".css",
    ".csv",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".jsonc",
    ".md",
    ".ps1",
    ".py",
    ".sh",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}

PUBLIC_URL_HOSTS = {
    "api.anthropic.com",
    "console.anthropic.com",
    "core.ac.uk",
    "developer.ieee.org",
    "dl.acm.org",
    "doaj.org",
    "export.arxiv.org",
    "github.com",
    "githubusercontent.com",
    "huggingface.co",
    "open.bigmodel.cn",
    "openxlab.org.cn",
    "semanticscholar.org",
    "zread.ai",
}

SENSITIVE_PATH_PARTS = {
    ".env",
    ".omc",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "auths",
    "graphify-out",
    "htmlcov",
    "logs",
    "node_modules",
}

SENSITIVE_SUFFIXES = (
    ".db",
    ".db-shm",
    ".db-wal",
    ".env",
    ".key",
    ".log",
    ".pyc",
    ".secret",
    ".session.json",
    ".token",
)

SECRET_KEY_RE = re.compile(
    r"(?i)\b(api[_-]?key|token|secret|password|access[_-]?token|"
    r"refresh[_-]?token|client[_-]?secret)\b\s*[:=]\s*([\"']?)([^\"'\s,}]+)"
)
BEARER_RE = re.compile(r"(?i)\bBearer\s+([A-Za-z0-9._~+/=-]{20,})")
PRIVATE_KEY_RE = re.compile(r"BEGIN [A-Z0-9 ]*PRIVATE KEY")
COOKIE_RE = re.compile(r"(?i)\b(cookie|session)\b\s*[:=]\s*[^\s]{20,}")
IP_URL_RE = re.compile(r"https?://(?:\d{1,3}\.){3}\d{1,3}(?::\d+)?(?:/|\b)")
URL_RE = re.compile(r"https?://([^/\s\"'<>]+)")
BASE_URL_RE = re.compile(r"(?i)\b(vps|base[_-]?url|openai_base_url|compatible endpoint)\b")
WINDOWS_USER_PATH_RE = re.compile(
    r"(?i)C:\\Users\\(?!(YOU|YOUR_USERNAME|USERNAME|yourname)\\)[^\\\s]+"
)
LONG_RANDOM_RE = re.compile(r"^[A-Za-z0-9._~+/=-]{24,}$")


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    category: str
    severity: str


def run_git(args: list[str], *, text: bool = True) -> str | bytes:
    result = subprocess.run(
        ["git", *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
    )
    return result.stdout


def is_binary(data: bytes) -> bool:
    return b"\0" in data[:4096]


def decode(data: bytes) -> str:
    return data.decode("utf-8", errors="replace")


def is_text_path(path: str) -> bool:
    suffix = Path(path).suffix.lower()
    return suffix in TEXT_EXTENSIONS or suffix == ""


def normalize(path: str) -> str:
    return path.replace("\\", "/")


def path_is_sensitive(path: str) -> bool:
    normalized = normalize(path).lower()
    parts = set(part for part in normalized.split("/") if part)
    name = Path(normalized).name
    if any(part in SENSITIVE_PATH_PARTS for part in parts):
        return True
    if name in SENSITIVE_PATH_PARTS:
        return True
    return name.endswith(SENSITIVE_SUFFIXES)


def is_placeholder_value(value: str) -> bool:
    raw = value.strip().strip("\"'")
    upper = raw.upper()
    lower = raw.lower()
    if re.fullmatch(r"<[A-Z0-9_./:-]+>", raw):
        return True
    if re.fullmatch(r"YOUR_[A-Z0-9_]+", upper):
        return True
    if lower in {"your-key-here", "your-token-here", "your-api-key", "example", "placeholder"}:
        return True
    if "your-" in lower or "-your-" in lower or "example" in lower:
        return True
    if raw.startswith("$") or raw.startswith("${"):
        return True
    if raw.startswith("%") and raw.endswith("%"):
        return True
    if any(word in raw for word in ("你的", "示例", "占位符")):
        return True
    return False


def host_is_public(host: str) -> bool:
    host = host.lower().split(":", 1)[0]
    return any(host == allowed or host.endswith(f".{allowed}") for allowed in PUBLIC_URL_HOSTS)


def scan_text(path: str, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        if PRIVATE_KEY_RE.search(line):
            findings.append(Finding(path, lineno, "private-key", "high"))
        if BEARER_RE.search(line):
            token = BEARER_RE.search(line).group(1)  # type: ignore[union-attr]
            if not is_placeholder_value(token):
                findings.append(Finding(path, lineno, "bearer-token", "high"))
        if COOKIE_RE.search(line):
            findings.append(Finding(path, lineno, "cookie-or-session", "high"))
        if IP_URL_RE.search(line):
            findings.append(Finding(path, lineno, "raw-ip-url", "high"))
        if WINDOWS_USER_PATH_RE.search(line):
            findings.append(Finding(path, lineno, "windows-user-path", "medium"))
        for match in SECRET_KEY_RE.finditer(line):
            value = match.group(3)
            if LONG_RANDOM_RE.match(value) and not is_placeholder_value(value):
                findings.append(Finding(path, lineno, "secret-assignment", "high"))
        if BASE_URL_RE.search(line):
            for host in URL_RE.findall(line):
                if not host_is_public(host) and not is_placeholder_value(host):
                    findings.append(Finding(path, lineno, "private-base-url", "high"))
    return findings


def tracked_files() -> list[str]:
    output = run_git(["ls-files"])
    assert isinstance(output, str)
    return [line for line in output.splitlines() if line]


def staged_entries() -> list[tuple[str, str, str | None]]:
    output = run_git(["diff", "--cached", "--name-status", "--diff-filter=ACMR"])
    assert isinstance(output, str)
    entries: list[tuple[str, str, str | None]] = []
    for line in output.splitlines():
        if not line:
            continue
        fields = line.split("\t")
        status = fields[0]
        if status.startswith("R") and len(fields) >= 3:
            entries.append((status, fields[2], fields[1]))
        elif len(fields) >= 2:
            entries.append((status, fields[1], None))
    return entries


def read_staged(path: str) -> bytes:
    output = run_git(["show", f":{path}"], text=False)
    assert isinstance(output, bytes)
    return output


def read_worktree(path: str) -> bytes:
    return Path(path).read_bytes()


def scan_blob(path: str, data: bytes) -> list[Finding]:
    if not is_text_path(path) or is_binary(data):
        return []
    return scan_text(path, decode(data))


def scan_tree() -> list[Finding]:
    findings: list[Finding] = []
    for path in tracked_files():
        if path_is_sensitive(path):
            findings.append(Finding(path, 0, "sensitive-path-tracked", "high"))
            continue
        try:
            findings.extend(scan_blob(path, read_worktree(path)))
        except OSError:
            findings.append(Finding(path, 0, "read-error", "medium"))
    return findings


def scan_staged() -> list[Finding]:
    findings: list[Finding] = []
    for status, path, old_path in staged_entries():
        for candidate in [old_path, path]:
            if candidate and path_is_sensitive(candidate):
                findings.append(Finding(candidate, 0, f"sensitive-path-staged-{status}", "high"))
        if path_is_sensitive(path):
            continue
        try:
            findings.extend(scan_blob(path, read_staged(path)))
        except subprocess.CalledProcessError:
            findings.append(Finding(path, 0, "staged-read-error", "medium"))
    return findings


def scan_paths(paths: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    for path in paths:
        normalized = normalize(path)
        if path_is_sensitive(normalized):
            findings.append(Finding(normalized, 0, "sensitive-path", "high"))
            continue
        try:
            findings.extend(scan_blob(normalized, read_worktree(path)))
        except OSError:
            findings.append(Finding(normalized, 0, "read-error", "medium"))
    return findings


def print_findings(findings: list[Finding]) -> None:
    for finding in findings:
        location = finding.path if finding.line == 0 else f"{finding.path}:{finding.line}"
        print(f"{finding.severity}\t{finding.category}\t{location}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan public files for sensitive values.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--tree", action="store_true", help="scan tracked public tree")
    group.add_argument("--staged", action="store_true", help="scan staged index blobs")
    group.add_argument("--paths", nargs="+", help="scan explicit worktree paths")
    return parser.parse_args()


def main() -> int:
    os.chdir(Path(__file__).resolve().parents[1])
    args = parse_args()
    if args.tree:
        findings = scan_tree()
    elif args.staged:
        findings = scan_staged()
    else:
        findings = scan_paths(args.paths)

    if findings:
        print_findings(findings)
        return 1

    print("Public safety scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
