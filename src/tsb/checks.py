"""Independent, read-only environment and Shizuku checks."""
from __future__ import annotations

import os
import platform
import sys
from pathlib import Path
from typing import Any

from .constants import DEFAULT_APPLICATION_ID, PROBES, VERSION
from .runner import find_rish, find_rish_dex, run_fixed_probe


def _is_termux() -> bool:
    prefix = os.environ.get("PREFIX", "")
    return prefix.startswith("/data/data/com.termux/") or (
        prefix.endswith("/com.termux/files/usr")
        and "TERMUX_VERSION" in os.environ
    )


def collect_diagnostics() -> dict[str, Any]:
    rish = find_rish()
    dex = find_rish_dex(rish) if rish else None
    report: dict[str, Any] = {
        "tool": "TSB",
        "version": VERSION,
        "ready": False,
        "termux_detected": _is_termux(),
        "termux_version": os.environ.get("TERMUX_VERSION") or "not reported",
        "python_version": platform.python_version(),
        "python_executable": Path(sys.executable).name,
        "application_id": os.environ.get("RISH_APPLICATION_ID", DEFAULT_APPLICATION_ID),
        "rish_found": rish is not None,
        "rish_path": str(rish) if rish else None,
        "dex_found": dex is not None,
        "dex_path": str(dex) if dex else None,
        "probes": {},
        "notes": [],
    }

    if not report["termux_detected"]:
        report["notes"].append(
            "Termux could not be confirmed. Run TSB inside the official Termux app."
        )
    if rish is None:
        report["notes"].append(
            "rish was not found. Export the current rish helper using Shizuku's "
            "terminal-app integration, then place it in ~/rish or PATH."
        )
        return report

    if dex is None:
        report["notes"].append(
            "rish_shizuku.dex was not found. Re-export the helper and companion "
            "file from Shizuku's terminal-app integration. On Android 14+, do not "
            "run a writable DEX copy from shared storage."
        )

    for name, command in PROBES.items():
        report["probes"][name] = run_fixed_probe(rish, command)

    probes_ok = all(item["ok"] for item in report["probes"].values())
    report["ready"] = bool(report["termux_detected"] and dex and probes_ok)

    uid = report["probes"].get("uid", {}).get("value")
    if report["probes"].get("uid", {}).get("ok"):
        report["identity"] = {"0": "root", "2000": "Android shell"}.get(
            uid, f"UID {uid}"
        )

    if not probes_ok:
        report["notes"].append(
            "One or more fixed probes failed. Check that Shizuku is running and "
            "Termux is authorized in Shizuku."
        )
    elif not report["ready"]:
        report["notes"].append(
            "The remote probes responded, but the local Termux/rish companion "
            "checks are incomplete."
        )
    return report
