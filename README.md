<div align="center">

<img src="assets/tsb-banner.svg" alt="Termux-Shizuku-Bridge — TSB" width="100%">

# Termux-Shizuku-Bridge

**Read-only diagnostics for the Termux → rish → Shizuku connection.**

[![Version](https://img.shields.io/badge/version-0.2.0-168f78?style=flat-square)](pyproject.toml) [![Python](https://img.shields.io/badge/python-3.10%2B-3776ab?style=flat-square&logo=python&logoColor=white)](https://www.python.org/) [![Platform](https://img.shields.io/badge/platform-Android-3ddc84?style=flat-square&logo=android&logoColor=white)](https://www.android.com/) [![License](https://img.shields.io/badge/license-MIT-64748b?style=flat-square)](LICENSE)

</div>

---

## Overview

**Termux-Shizuku-Bridge (TSB)** is a privacy-first diagnostic utility that helps you understand which parts of the Termux → rish → Shizuku connection are working. It identifies the remote execution identity and creates sanitized support reports.

> TSB is an observability and troubleshooting tool—not a root tool, privilege manager, or Shizuku replacement.

## Features

| Component | What it does |
|---|---|
| **Connection Observatory** | Checks Termux detection, rish discovery, companion DEX presence, and fixed read-only probes. |
| **Capability Fingerprint** | Reports the remote UID and identifies common execution identities without assuming Shizuku means root. |
| **Privacy-first Reports** | Redacts local paths and custom application IDs by default; supports text and JSON. |
| **Offline by Design** | No telemetry, automatic uploads, or network reporting. |

## Safety and privacy

- Runs only a small, hard-coded allowlist of read-only probes.
- Does **not** accept arbitrary shell commands or evaluate user-provided commands.
- Does **not** grant Shizuku permissions or change Android settings.
- Does **not** install, disable, or modify apps or system data.
- Applies a timeout to every rish subprocess.
- Keeps diagnostic reports local; nothing is uploaded automatically.

## Requirements

- Android device
- [Termux](https://github.com/termux/termux-app)
- Python 3.10 or newer
- [Shizuku](https://github.com/RikkaApps/Shizuku), running and explicitly authorized for Termux
- The official rish helper and rish_shizuku.dex exported through Shizuku's terminal-app integration

See the [official rish documentation](https://github.com/RikkaApps/Shizuku-API/tree/master/rish).

## Installation

In Termux:

```bash
pkg install python git
git clone https://github.com/M34nX/Termux-Shizuku-Bridge.git
cd Termux-Shizuku-Bridge
python -m pip install --user .
```

To run directly from a source checkout without installing:

```bash
python tsb.py doctor
```

## Usage

```bash
tsb doctor                 # Diagnose the Termux–Shizuku bridge
tsb status                 # Show connection status
tsb report                 # Print a sanitized text report
tsb report --json          # Print a sanitized JSON report
tsb report --output FILE   # Save a report locally
tsb report --include-paths # Explicitly include local paths
tsb version                # Show version
```

Review a report before sharing it. Reports are not uploaded by TSB.

## Development

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

The GitHub Actions workflow is configured for Python 3.10–3.13. A real Android device with a working Shizuku setup is required for end-to-end validation.

## Project structure

```text
.
├── src/tsb/              # Application package
├── tests/                # Unit tests
├── docs/                 # Architecture, security, troubleshooting
├── .github/workflows/    # CI workflow
├── assets/               # Project branding
├── install.sh
├── uninstall.sh
├── pyproject.toml
└── tsb.py                # Source-checkout launcher
```

## Project status

**Version 0.2.0 — redesign in progress.** Unit tests and real-device behavior must be verified before describing this release as production-ready.

## License

MIT. See [LICENSE](LICENSE).
