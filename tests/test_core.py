import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tsb.constants import PROBES, VERSION
from tsb.privacy import sanitize_report
from tsb.report import render_json, render_text
from tsb.runner import find_rish_dex, run_fixed_probe


class CoreTests(unittest.TestCase):
    def sample(self):
        return {
            "version": VERSION,
            "ready": True,
            "termux_detected": True,
            "rish_found": True,
            "rish_path": "/data/data/com.termux/files/home/rish",
            "dex_found": True,
            "dex_path": "/data/data/com.termux/files/home/rish_shizuku.dex",
            "application_id": "private.app",
            "identity": "Android shell",
            "probes": {"uid": {"ok": True, "value": "2000"}},
            "notes": [],
        }

    def test_probe_allowlist_is_small_and_fixed(self):
        self.assertEqual(
            set(PROBES), {"uid", "android_release", "android_sdk", "manufacturer"}
        )
        self.assertTrue(all(isinstance(value, str) for value in PROBES.values()))

    def test_report_redacts_paths_and_custom_app_id(self):
        result = sanitize_report(self.sample())
        self.assertEqual(result["rish_path"], "rish")
        self.assertEqual(result["dex_path"], "rish_shizuku.dex")
        self.assertEqual(result["application_id"], "[redacted]")

    def test_report_redacts_paths_in_nested_text(self):
        data = self.sample()
        data["notes"] = [
            "Termux data: /data/data/com.termux/files/home/private",
            "Shared file: /storage/emulated/0/Download/diagnostic.txt",
            "Linux home: /home/alice/.config/tsb",
            "Legacy storage: /sdcard/Download/diagnostic.txt",
        ]
        data["probes"]["manufacturer"] = {
            "ok": False,
            "value": "Read failed near /Users/alice/Library/Logs/tsb.log",
        }

        result = sanitize_report(data)

        for private_path in (
            "/data/data/com.termux",
            "/storage/emulated/0",
            "/home/alice",
            "/sdcard",
            "/Users/alice",
        ):
            self.assertNotIn(private_path, str(result))
        self.assertEqual(result["notes"][1], "Shared file: [path]")
        self.assertEqual(result["probes"]["manufacturer"]["value"],
                         "Read failed near [path]")

    def test_include_paths_is_explicit_and_preserves_paths(self):
        data = self.sample()
        data["notes"] = ["Local file: /storage/emulated/0/Download/report.txt"]
        result = sanitize_report(data, include_paths=True)
        self.assertTrue(result["rish_path"].startswith("/data/"))
        self.assertTrue(result["dex_path"].startswith("/data/"))
        self.assertIn("/storage/emulated/0/Download/report.txt", result["notes"][0])
        self.assertEqual(result["application_id"], "[redacted]")

    def test_renderers(self):
        data = self.sample()
        self.assertIn('"ready": true', render_json(data))
        self.assertIn("Overall: READY", render_text(data))
        self.assertIn("Python version:", render_text({**data, "python_version": "3.x"}))

    def test_dex_override_is_respected(self):
        with tempfile.TemporaryDirectory() as directory:
            dex = Path(directory) / "custom.dex"
            dex.write_text("test", encoding="utf-8")
            with patch.dict(os.environ, {"TSB_RISH_DEX": str(dex)}):
                self.assertEqual(find_rish_dex(None), dex.resolve())

    def test_missing_dex_returns_none(self):
        with patch.dict(os.environ, {"TSB_RISH_DEX": "/definitely/not/a/real/file.dex"}):
            self.assertIsNone(find_rish_dex(None))

    def test_unlisted_command_is_blocked_before_execution(self):
        with patch("tsb.runner.subprocess.run") as run:
            result = run_fixed_probe(Path("/tmp/rish"), "id")
        self.assertFalse(result["ok"])
        self.assertIn("Blocked", result["value"])
        run.assert_not_called()

    def test_version(self):
        self.assertRegex(VERSION, r"^[0-9]+[.][0-9]+[.][0-9]+$")
        self.assertEqual(VERSION, "0.2.1")


if __name__ == "__main__":
    unittest.main()
