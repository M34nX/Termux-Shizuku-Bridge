"""TSB command-line interface."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from . import __version__
from .checks import collect_diagnostics
from .privacy import sanitize_report
from .report import render_json, render_text

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tsb", description="Privacy-first, read-only Termux/Shizuku diagnostics.")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("doctor", help="Run diagnostics and explain problems")
    sub.add_parser("status", help="Show current connection status")
    report = sub.add_parser("report", help="Create a sanitized support report")
    report.add_argument("--json", action="store_true", help="Write JSON instead of text")
    report.add_argument("--output", type=Path, help="Save report to a local file")
    report.add_argument("--include-paths", action="store_true", help="Include local paths in the report")
    sub.add_parser("version", help="Show version")
    return parser

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    command = args.command or "doctor"
    if command == "version":
        print(__version__)
        return 0
    data = collect_diagnostics()
    if command == "report":
        data = sanitize_report(data, include_paths=args.include_paths)
        output = render_json(data) if args.json else render_text(data)
        if args.output:
            try:
                args.output.write_text(output + "\n", encoding="utf-8")
            except OSError as exc:
                reason = exc.strerror or exc.__class__.__name__
                print(f"Could not write report: {reason}", file=sys.stderr)
                return 2
            print(f"Report saved to {args.output}")
        else:
            print(output)
    else:
        print(render_text(data))
    return 0 if data["ready"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
