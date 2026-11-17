"""Privacy filters for support reports."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any


_PATH_PATTERNS = tuple(
    re.compile(pattern)
    for pattern in (
        r"/data/(?:user(?:_de)?(?:/\d+)?|data)/[^\s:,'\"<>)]*",
        r"/storage/emulated/\d+(?:/[^\s:,'\"<>)]*)?",
        r"/sdcard(?:/[^\s:,'\"<>)]*)?",
        r"/home/[^/\s:,'\"<>]+(?:/[^\s:,'\"<>)]*)?",
        r"/Users/[^/\s:,'\"<>]+(?:/[^\s:,'\"<>)]*)?",
        r"/private/var/[^\\s:,'\"<>)]*",
        r"/var/folders/[^\\s:,'\"<>)]*",
    )
)


def _redact_local_paths(text: str) -> str:
    for pattern in _PATH_PATTERNS:
        text = pattern.sub("[path]", text)
    return text


def _redact_nested(value: Any) -> Any:
    """Redact paths from strings inside dictionaries and sequences."""
    if isinstance(value, dict):
        return {key: _redact_nested(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_redact_nested(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_redact_nested(item) for item in value)
    if isinstance(value, str):
        return _redact_local_paths(value)
    return value


def sanitize_report(data: dict[str, Any], *, include_paths: bool = False) -> dict[str, Any]:
    clean = deepcopy(data)

    app_id = clean.get("application_id")
    if app_id and app_id != "com.termux":
        clean["application_id"] = "[redacted]"

    if not include_paths:
        # Keep useful filenames while omitting their parent directories.
        for key in ("rish_path", "dex_path"):
            value = clean.get(key)
            if isinstance(value, str) and value:
                clean[key] = Path(value).name

        # Probe output and notes can also contain paths; sanitize all nested text.
        for key, value in tuple(clean.items()):
            if key not in ("rish_path", "dex_path"):
                clean[key] = _redact_nested(value)

    return clean
