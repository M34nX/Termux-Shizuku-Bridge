import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tsb.constants import PROBES, VERSION
from tsb.privacy import sanitize_report
from tsb.report import render_json, render_text
from tsb.runner import find_rish_dex


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

    def test_include_paths_is_explicit(self):
        result = sanitize_report(self.sample(), include_paths=True)
        self.assertTrue(result["rish_path"].startswith("/data/"))
        self.assertTrue(result["dex_path"].startswith("/data/"))

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

    def test_version(self):
        self.assertRegex(VERSION, r"^\d+\.\d+\.\d+$")


if __name__ == "__main__":
    unittest.main()
