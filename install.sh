#!/data/data/com.termux/files/usr/bin/bash
set -eu
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
command -v python >/dev/null 2>&1 || { echo "Install Python first: pkg install python" >&2; exit 1; }
python -m pip install --user "$ROOT"
echo "TSB installed. Run: tsb doctor"
