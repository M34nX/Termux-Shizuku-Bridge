# TSB — Termux Shizuku Bridge

**A privacy-first diagnostic companion for Termux and Shizuku.**

TSB (Termux Shizuku Bridge) explains which parts of the Termux → rish → Shizuku connection are working, identifies the remote execution identity, and produces sanitized support reports. It is a diagnostic tool, not a privilege manager.

## What makes TSB useful

- **Connection Observatory:** checks Termux detection, rish discovery, companion DEX presence, and fixed read-only probes.
- **Capability Fingerprint:** reports the remote UID and labels common identities accurately; Shizuku does not automatically mean root.
- **Privacy-first Support Report:** removes local paths and custom application IDs by default.
- **Offline by design:** no telemetry, automatic uploads, or network reporting.

## Safety boundaries

TSB only invokes a small, hard-coded allowlist of read-only probes. It does not accept arbitrary shell commands, grant Shizuku permissions, change Android settings, install or disable apps, or modify system data. Every rish subprocess has a timeout.

## Requirements

- Android with Termux and Python 3.10+
- Shizuku installed, running, and explicitly authorized for Termux
- The official `rish` helper and `rish_shizuku.dex` exported using Shizuku's terminal-app integration

See the [official rish documentation](https://github.com/RikkaApps/Shizuku-API/tree/master/rish).

## Install in Termux

```bash
pkg install python git
git clone https://github.com/M34nX/Termux-Shizuku-Bridge.git
cd Termux-Shizuku-Bridge
python -m pip install --user .
```

Or run from a source checkout without installing:

```bash
python tsb.py doctor
```

## Commands

```text
tsb doctor                 Run diagnostics and explain issues
tsb status                 Show connection status
tsb report                 Print a sanitized text report
tsb report --json          Print a sanitized JSON report
tsb report --output FILE   Save a report locally
tsb report --include-paths Explicitly include local paths
tsb version                Show version
```

The `report` command never uploads data. Review a report before sharing it.

## Development

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

CI runs the unit suite on Python 3.10–3.13. A real Android device with Shizuku is still required for end-to-end validation.

## Project layout

- `src/tsb/`: modular application package
- `tests/`: unit tests
- `docs/`: architecture, security, troubleshooting
- `.github/workflows/`: automated test workflow

## Status

**0.2.0 redesign in progress.** Unit tests and real-device behavior must be verified before calling this release production-ready.

## License

MIT. See [LICENSE](LICENSE).
