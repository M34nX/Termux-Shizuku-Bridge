"""Restricted rish and companion-file discovery and execution."""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from .constants import COMMAND_TIMEOUT_SECONDS, DEFAULT_APPLICATION_ID


def find_rish() -> Path | None:
    candidates: list[Path] = []
    override = os.environ.get("TSB_RISH")
    if override:
        candidates.append(Path(override).expanduser())
    located = shutil.which("rish")
    if located:
        candidates.append(Path(located))
    candidates.extend(
        (
            Path.home() / "rish",
            Path.home() / ".local/bin/rish",
            Path.cwd() / "rish",
        )
    )
    seen: set[str] = set()
    for candidate in candidates:
        try:
            path = candidate.resolve()
            key = str(path)
            if key in seen:
                continue
            seen.add(key)
            if path.is_file() and os.access(path, os.X_OK):
                return path
        except OSError:
            continue
    return None


def find_rish_dex(rish: Path | None) -> Path | None:
    """Find the companion DEX without treating Shizuku's service binary as a DEX."""
    candidates: list[Path] = []
    override = os.environ.get("TSB_RISH_DEX")
    if override:
        candidates.append(Path(override).expanduser())
    if rish is not None:
        candidates.append(rish.parent / "rish_shizuku.dex")
    candidates.extend(
        (
            Path.home() / "rish_shizuku.dex",
            Path.home() / ".local/share/rish/rish_shizuku.dex",
        )
    )
    prefix = os.environ.get("PREFIX")
    if prefix:
        candidates.append(Path(prefix) / "share/rish/rish_shizuku.dex")
    seen: set[str] = set()
    for candidate in candidates:
        try:
            path = candidate.resolve()
            key = str(path)
            if key not in seen:
                seen.add(key)
                if path.is_file():
                    return path
        except OSError:
            continue
    return None


def run_fixed_probe(rish: Path, command: str) -> dict[str, object]:
    """Run one command from the internal fixed diagnostic allowlist only."""
    from .constants import PROBES

    if command not in PROBES.values():
        return {
            "ok": False,
            "value": "Blocked: command is not in the fixed diagnostic allowlist",
        }
    env = os.environ.copy()
    env.setdefault("RISH_APPLICATION_ID", DEFAULT_APPLICATION_ID)
    # Preserve the remote environment's defaults; Termux paths are not valid
    # Android-system paths for the Android shell identity.
    env.setdefault("RISH_PRESERVE_ENV", "0")
    try:
        completed = subprocess.run(
            [str(rish), "-c", command],
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT_SECONDS,
            check=False,
            env=env,
        )
    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "value": f"Timed out after {COMMAND_TIMEOUT_SECONDS} seconds",
        }
    except OSError as exc:
        return {
            "ok": False,
            "value": f"Could not start rish: {exc.__class__.__name__}",
        }

    output = (completed.stdout or "").strip()
    if completed.returncode:
        error = (completed.stderr or output or f"rish exited {completed.returncode}").strip()
        return {"ok": False, "value": error[:500]}
    return {"ok": True, "value": output[:500]}
