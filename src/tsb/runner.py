"""Restricted rish discovery and execution."""
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
    candidates.extend((Path.home() / "rish", Path.home() / ".local/bin/rish", Path.cwd() / "rish"))
    seen: set[str] = set()
    for candidate in candidates:
        try:
            path = candidate.resolve()
            if str(path) not in seen and path.is_file() and os.access(path, os.X_OK):
                return path
            seen.add(str(path))
        except OSError:
            continue
    return None

def run_fixed_probe(rish: Path, command: str) -> dict[str, object]:
    """Run one caller-selected command from the internal fixed allowlist only."""
    from .constants import PROBES
    if command not in PROBES.values():
        return {"ok": False, "value": "Blocked: command is not in the fixed diagnostic allowlist"}
    env = os.environ.copy()
    env.setdefault("RISH_APPLICATION_ID", DEFAULT_APPLICATION_ID)
    env.setdefault("RISH_PRESERVE_ENV", "0")
    try:
        completed = subprocess.run(
            [str(rish), "-c", command], capture_output=True, text=True,
            timeout=COMMAND_TIMEOUT_SECONDS, check=False, env=env,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "value": f"Timed out after {COMMAND_TIMEOUT_SECONDS} seconds"}
    except OSError as exc:
        return {"ok": False, "value": f"Could not start rish: {exc.__class__.__name__}"}
    output = (completed.stdout or "").strip()
    if completed.returncode:
        return {"ok": False, "value": (completed.stderr or output or f"rish exited {completed.returncode}").strip()}
    return {"ok": True, "value": output}
