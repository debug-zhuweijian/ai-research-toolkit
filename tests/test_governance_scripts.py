from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAN_SCRIPT = ROOT / "scripts" / "scan-public-safety.py"
NOTES_SCRIPT = ROOT / "scripts" / "extract-release-notes.py"
VERIFY_SCRIPT = ROOT / "scripts" / "verify-profiles.py"


class GovernanceScriptTests(unittest.TestCase):
    def run_python(self, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, *args],
            cwd=cwd or ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_verify_profiles_passes_current_repo(self) -> None:
        result = self.run_python(str(VERIFY_SCRIPT))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_extract_release_notes_writes_single_changelog_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            changelog = tmp_path / "CHANGELOG.md"
            output = tmp_path / "notes.md"
            changelog.write_text(
                "# Changelog\n\n"
                "## [Unreleased]\n\n- Future.\n\n"
                "## [0.3.0-beta.2] - 2026-06-15\n\n"
                "### Fixed\n\n- Release governance.\n\n"
                "## [0.3.0-beta.1] - 2026-06-14\n\n"
                "- Previous beta.\n",
                encoding="utf-8",
            )

            result = self.run_python(
                str(NOTES_SCRIPT),
                "--tag",
                "v0.3.0-beta.2",
                "--changelog",
                str(changelog),
                "--output",
                str(output),
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            notes = output.read_text(encoding="utf-8")
            self.assertIn("0.3.0-beta.2", notes)
            self.assertIn("Release governance.", notes)
            self.assertNotIn("0.3.0-beta.1", notes)

    def test_scanner_allows_public_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init"], cwd=repo, check=True, stdout=subprocess.PIPE)
            readme = repo / "README.md"
            readme.write_text(
                "Use C:\\Users\\you\\.claude for local examples.\n"
                "Local endpoint examples may use http://localhost:8000/v1.\n"
                "OPENAI_API_KEY=your-key-here\n",
                encoding="utf-8",
            )
            subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)

            result = self.run_python(str(SCAN_SCRIPT), "--repo-root", str(repo), "--tree")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_scanner_blocks_secret_without_printing_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init"], cwd=repo, check=True, stdout=subprocess.PIPE)
            token = "A" * 24
            secret_file = repo / "config.md"
            secret_file.write_text(f"Authorization: Bearer {token}\n", encoding="utf-8")
            subprocess.run(["git", "add", "config.md"], cwd=repo, check=True)

            result = self.run_python(str(SCAN_SCRIPT), "--repo-root", str(repo), "--staged")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("bearer-token", result.stdout)
            self.assertNotIn(token, result.stdout)


if __name__ == "__main__":
    unittest.main()
