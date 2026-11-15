#!/usr/bin/env python3
"""TSB: read-only diagnostics for Termux and Shizuku."""
from __future__ import annotations
import argparse, json, os, shutil, subprocess
from pathlib import Path

VERSION = "0.1.0"
PROBES = {
    "uid": "id -u",
    "android_release": "getprop ro.build.version.release",
    "android_sdk": "getprop ro.build.version.sdk",
    "device_manufacturer": "getprop ro.product.manufacturer",
}

def find_rish():
    candidates = []
    override = os.environ.get("TSB_RISH")
    if override: candidates.append(Path(override).expanduser())
    located = shutil.which("rish")
    if located: candidates.append(Path(located))
    candidates.extend([Path.home()/"rish", Path.home()/".local/bin/rish", Path.cwd()/"rish"])
    for candidate in candidates:
        try:
            p = candidate.resolve()
            if p.is_file() and os.access(p, os.X_OK): return p
        except OSError: pass
    return None

def probe(rish, command):
    env = os.environ.copy()
    env.setdefault("RISH_APPLICATION_ID", "com.termux")
    env.setdefault("RISH_PRESERVE_ENV", "0")
    try:
        p = subprocess.run([str(rish), "-c", command], capture_output=True,
                           text=True, timeout=8, check=False, env=env)
    except (OSError, subprocess.TimeoutExpired) as e:
        return False, str(e)
    value = (p.stdout or "").strip()
    if p.returncode: return False, (p.stderr or value or f"exit {p.returncode}").strip()
    return True, value

def status():
    rish = find_rish()
    out = {"tool":"TSB", "version":VERSION, "ready":False,
           "termux_detected":os.environ.get("PREFIX","").startswith("/data/data/com.termux/"),
           "rish_path":str(rish) if rish else None,
           "application_id":os.environ.get("RISH_APPLICATION_ID","com.termux"),
           "probes":{}, "notes":[]}
    if not rish:
        out["notes"].append("rish not found; export it from Shizuku terminal integration to ~/rish or PATH.")
        return out
    dex = next((p for p in (rish.parent/"rish_shizuku.dex", Path.home()/"rish_shizuku.dex") if p.is_file()), None)
    out["rish_dex_path"] = str(dex) if dex else None
    if not dex: out["notes"].append("rish_shizuku.dex not found beside rish or in home directory.")
    ok_all = True
    for key, command in PROBES.items():
        ok, value = probe(rish, command)
        out["probes"][key] = {"ok":ok, "value":value}
        ok_all = ok_all and ok
    out["ready"] = ok_all
    if not ok_all: out["notes"].append("Probes failed; check Shizuku is running and Termux is authorized.")
    else:
        uid = out["probes"]["uid"]["value"]
        out["identity"] = "root" if uid == "0" else ("Android shell" if uid == "2000" else f"UID {uid}")
    return out

def main():
    parser = argparse.ArgumentParser(description="Read-only Termux/Shizuku diagnostics.")
    parser.add_argument("command", nargs="?", choices=("doctor","status","version"), default="doctor")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.command == "version":
        print(VERSION); return 0
    result = status()
    if args.json: print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"TSB {VERSION} — Termux / Shizuku Bridge")
        print(f"Termux detected: {result['termux_detected']}")
        print(f"rish: {result['rish_path'] or 'not found'}")
        for key, item in result["probes"].items():
            print(f"{key}: {item['value'] if item['ok'] else 'FAILED — ' + item['value']}")
        for note in result["notes"]: print(f"NOTE: {note}")
        print("Doctor result: " + ("READY" if result["ready"] else "NEEDS ATTENTION"))
    return 0 if result["ready"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
