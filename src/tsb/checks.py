"""Independent, read-only environment and Shizuku checks."""
from __future__ import annotations
import os
from pathlib import Path
from typing import Any
from .constants import DEFAULT_APPLICATION_ID, PROBES, VERSION
from .runner import find_rish, run_fixed_probe

def collect_diagnostics() -> dict[str, Any]:
    rish = find_rish()
    report: dict[str, Any] = {
        "tool": "TSB", "version": VERSION, "ready": False,
        "termux_detected": os.environ.get("PREFIX", "").startswith("/data/data/com.termux/"),
        "application_id": os.environ.get("RISH_APPLICATION_ID", DEFAULT_APPLICATION_ID),
        "rish_found": rish is not None, "rish_path": str(rish) if rish else None,
        "dex_found": False, "probes": {}, "notes": [],
    }
    if rish is None:
        report["notes"].append("rish was not found. Export it using Shizuku terminal integration and place it in ~/rish or PATH.")
        return report
    dex_candidates = (rish.parent / "rish_shizuku.dex", Path.home() / "rish_shizuku.dex")
    dex = next((p for p in dex_candidates if p.is_file()), None)
    report["dex_found"] = dex is not None
    if dex is None:
        report["notes"].append("rish_shizuku.dex was not found beside rish or in the home directory.")
    for name, command in PROBES.items():
        report["probes"][name] = run_fixed_probe(rish, command)
    all_ok = all(item["ok"] for item in report["probes"].values())
    report["ready"] = all_ok
    if all_ok:
        uid = report["probes"]["uid"]["value"]
        report["identity"] = {"0": "root", "2000": "Android shell"}.get(uid, f"UID {uid}")
        if uid == "0":
            report["notes"].append("The remote identity is root. TSB itself still runs only fixed read-only probes.")
    else:
        report["notes"].append("One or more probes failed. Check that Shizuku is running and Termux is authorized.")
    return report
