"""Cross-check project-local skill setup without touching installed user skills."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/sync_project_skills.py"


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="skill-discovery-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ("alpha", "beta"):
            folder = self.root / "skills" / "research" / name
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text(f"---\nname: {name}\ndescription: test\n---\n", encoding="utf-8")
            (folder / "notes.md").write_text(f"source {name}\n", encoding="utf-8")

    def run_tool(self, *args):
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), *args],
                                capture_output=True, text=True, encoding="utf-8", env=dict(os.environ, PYTHONUTF8="1"))
        data = json.loads(result.stdout or result.stderr)
        return result.returncode, data

    def test_preview_is_read_only_and_auto_apply_is_idempotent(self):
        code, plan = self.run_tool()
        self.assertEqual(code, 0)
        self.assertFalse(plan["complete"])
        self.assertFalse((self.root / ".agents").exists())
        self.assertNotEqual(self.run_tool("--check")[0], 0)
        code, result = self.run_tool("--apply", "--mode", "auto")
        self.assertEqual(code, 0)
        self.assertTrue(result["complete"])
        self.assertTrue(all(row["state"] in ("linked", "copy_matches") for row in result["entries"]))
        code, again = self.run_tool("--apply", "--mode", "auto")
        self.assertEqual(code, 0)
        self.assertTrue(again["complete"])
        self.assertEqual(self.run_tool("--check")[0], 0)

    def test_copy_drift_is_detected_and_never_replaced(self):
        code, _ = self.run_tool("--apply", "--mode", "copy")
        self.assertEqual(code, 0)
        copied = self.root / ".agents/skills/alpha/notes.md"
        copied.write_text("user-owned edit\n", encoding="utf-8")
        code, report = self.run_tool("--apply", "--mode", "copy")
        self.assertNotEqual(code, 0)
        self.assertIn("conflicting_or_stale", [row["state"] for row in report["entries"]])
        self.assertEqual(copied.read_text(encoding="utf-8"), "user-owned edit\n")

    def test_unmanaged_extras_are_preserved(self):
        extra = self.root / ".agents/skills/other"
        extra.mkdir(parents=True)
        (extra / "private.txt").write_text("keep", encoding="utf-8")
        code, report = self.run_tool("--apply", "--mode", "copy")
        self.assertEqual(code, 0)
        self.assertIn("unmanaged_extra", [row["state"] for row in report["entries"]])
        self.assertEqual((extra / "private.txt").read_text(encoding="utf-8"), "keep")

    def test_conflict_prevents_all_new_entries(self):
        collision = self.root / ".agents/skills/alpha"
        collision.mkdir(parents=True)
        (collision / "mine.txt").write_text("keep", encoding="utf-8")
        code, _ = self.run_tool("--apply", "--mode", "copy")
        self.assertNotEqual(code, 0)
        self.assertFalse((self.root / ".agents/skills/beta").exists())
        self.assertEqual((collision / "mine.txt").read_text(encoding="utf-8"), "keep")


if __name__ == "__main__": unittest.main()
