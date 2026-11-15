"""Human-readable and JSON report rendering."""
from __future__ import annotations
import json
from typing import Any

def render_json(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)

def render_text(data: dict[str, Any]) -> str:
    lines = [f"TSB {data['version']} — Termux / Shizuku diagnostics",
             f"Overall: {'READY' if data['ready'] else 'NEEDS ATTENTION'}",
             f"Termux detected: {'yes' if data['termux_detected'] else 'not confirmed'}",
             f"rish found: {'yes' if data['rish_found'] else 'no'}",
             f"Shizuku DEX found: {'yes' if data['dex_found'] else 'no'}"]
    if data.get("identity"):
        lines.append(f"Remote identity: {data['identity']}")
    for name, item in data.get("probes", {}).items():
        lines.append(f"{name}: {item['value'] if item['ok'] else 'FAILED — ' + item['value']}")
    if data.get("notes"):
        lines.append("Notes:")
        lines.extend(f"- {note}" for note in data["notes"])
    return "\n".join(lines)
