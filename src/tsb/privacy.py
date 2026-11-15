"""Privacy filters for support reports."""
from __future__ import annotations
from copy import deepcopy
from pathlib import Path
import re

def sanitize_report(data: dict, *, include_paths: bool = False) -> dict:
    clean = deepcopy(data)
    if not include_paths:
        for key in ("rish_path", "dex_path"):
            if clean.get(key):
                clean[key] = Path(clean[key]).name
    app_id = clean.get("application_id")
    if app_id and app_id != "com.termux":
        clean["application_id"] = "[redacted]"
    # Avoid leaking home-directory paths through diagnostic output.
    for probe in clean.get("probes", {}).values():
        value = probe.get("value")
        if isinstance(value, str):
            probe["value"] = re.sub(r"/data/(?:user|data)/[^\s:]+", "[path]", value)
    return clean
