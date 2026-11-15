import unittest
from tsb.constants import PROBES, VERSION
from tsb.privacy import sanitize_report
from tsb.report import render_json, render_text

class CoreTests(unittest.TestCase):
    def sample(self):
        return {"version": VERSION, "ready": True, "termux_detected": True,
                "rish_found": True, "rish_path": "/data/data/com.termux/files/home/rish",
                "dex_found": True, "application_id": "private.app",
                "identity": "Android shell",
                "probes": {"uid": {"ok": True, "value": "2000"}},"notes":[]}
    def test_probe_allowlist_is_small_and_fixed(self):
        self.assertEqual(set(PROBES), {"uid","android_release","android_sdk","manufacturer"})
        self.assertTrue(all(isinstance(v, str) for v in PROBES.values()))
    def test_report_redacts_paths_and_custom_app_id(self):
        result = sanitize_report(self.sample())
        self.assertEqual(result["rish_path"], "rish")
        self.assertEqual(result["application_id"], "[redacted]")
    def test_include_paths_is_explicit(self):
        result = sanitize_report(self.sample(), include_paths=True)
        self.assertTrue(result["rish_path"].startswith("/data/"))
    def test_renderers(self):
        data = self.sample()
        self.assertIn('"ready": true', render_json(data))
        self.assertIn("Overall: READY", render_text(data))
    def test_version(self):
        self.assertRegex(VERSION, r"^\d+\.\d+\.\d+$")

if __name__ == "__main__":
    unittest.main()
