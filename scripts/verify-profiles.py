#!/usr/bin/env python3
"""Verify install profile manifests, installers, and module counts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILES_DIR = ROOT / "profiles"
MODULES_DIR = ROOT / "modules"
INSTALL_SH = ROOT / "scripts" / "install.sh"
INSTALL_PS1 = ROOT / "scripts" / "install.ps1"


def load_profiles() -> dict[str, dict[str, object]]:
    profiles: dict[str, dict[str, object]] = {}
    for path in sorted(PROFILES_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        name = data.get("name")
        if not isinstance(name, str):
            raise ValueError(f"{path}: missing string name")
        profiles[name] = data
    return profiles


def count_skills(module_names: list[str]) -> int:
    total = 0
    for module_name in module_names:
        skills_dir = MODULES_DIR / module_name / "skills"
        if skills_dir.exists():
            total += sum(1 for child in skills_dir.iterdir() if child.is_dir())
    return total


def count_agents(module_names: list[str]) -> int:
    total = 0
    for module_name in module_names:
        agents_dir = MODULES_DIR / module_name / "agents"
        if agents_dir.exists():
            total += sum(1 for child in agents_dir.glob("*.md") if child.is_file())
    return total


def parse_bash_profiles() -> dict[str, list[str]]:
    text = INSTALL_SH.read_text(encoding="utf-8")
    pattern = re.compile(r"^\s*([a-z][a-z0-9_-]*)\)\s+echo \"([^\"]*)\"", re.MULTILINE)
    return {name: modules.split() for name, modules in pattern.findall(text)}


def parse_powershell_profiles() -> dict[str, list[str]]:
    text = INSTALL_PS1.read_text(encoding="utf-8-sig")
    pattern = re.compile(
        r'"([a-z][a-z0-9_-]*)"\s*\{\s*return @\(([^)]*)\)\s*\}',
        re.MULTILINE,
    )
    profiles: dict[str, list[str]] = {}
    for name, raw_modules in pattern.findall(text):
        profiles[name] = re.findall(r'"([^"]+)"', raw_modules)
    return profiles


def validate_profiles() -> list[str]:
    errors: list[str] = []
    profiles = load_profiles()
    bash_profiles = parse_bash_profiles()
    powershell_profiles = parse_powershell_profiles()

    expected_names = set(profiles)
    required_names = {"minimal", "researcher", "writer", "knowledge", "full"}
    if expected_names != required_names:
        errors.append(f"profile JSON names mismatch: {sorted(expected_names)} != {sorted(required_names)}")
    if set(bash_profiles) != expected_names:
        errors.append(f"install.sh profiles mismatch: {sorted(bash_profiles)} != {sorted(expected_names)}")
    if set(powershell_profiles) != expected_names:
        errors.append(f"install.ps1 profiles mismatch: {sorted(powershell_profiles)} != {sorted(expected_names)}")

    for name, profile in sorted(profiles.items()):
        modules = profile.get("modules")
        if not isinstance(modules, list) or not all(isinstance(item, str) for item in modules):
            errors.append(f"{name}: modules must be a string list")
            continue

        for module_name in modules:
            if not (MODULES_DIR / module_name).is_dir():
                errors.append(f"{name}: unknown module {module_name}")

        if name in bash_profiles and bash_profiles[name] != modules:
            errors.append(f"{name}: install.sh modules {bash_profiles[name]} != {modules}")
        if name in powershell_profiles and powershell_profiles[name] != modules:
            errors.append(f"{name}: install.ps1 modules {powershell_profiles[name]} != {modules}")

        actual_skill_count = count_skills(modules)
        if profile.get("skills_count") != actual_skill_count:
            errors.append(
                f"{name}: skills_count {profile.get('skills_count')} != actual {actual_skill_count}"
            )
        actual_agent_count = count_agents(modules)
        if profile.get("agents_count") != actual_agent_count:
            errors.append(
                f"{name}: agents_count {profile.get('agents_count')} != actual {actual_agent_count}"
            )

    full_modules = profiles.get("full", {}).get("modules", [])
    expected_full_modules = [
        "01-discovery",
        "02-processing",
        "03-analysis",
        "04-writing",
        "05-knowledge",
        "06-presentation",
        "07-pipeline",
    ]
    if full_modules != expected_full_modules:
        errors.append(f"full profile modules {full_modules} != {expected_full_modules}")

    return errors


def main() -> int:
    errors = validate_profiles()
    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        return 1

    print("Profile verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
