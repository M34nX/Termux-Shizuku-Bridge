<div align="center">

<img src="assets/tsb-banner.svg" alt="Termux-Shizuku-Bridge" width="100%">

# Termux-Shizuku-Bridge

**Privacy-first diagnostics for the Termux → rish → Shizuku connection.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?style=flat-square&logo=python)](https://python.org/)
[![Android](https://img.shields.io/badge/Android-Native-3ddc84?style=flat-square&logo=android)](https://android.com/)
[![License](https://img.shields.io/badge/License-MIT-64748b?style=flat-square)](LICENSE)

</div>

## Overview

TSB is a local-first diagnostic toolkit with two complementary components:

- **TSB CLI:** Python diagnostics for Termux, the official rish helper, its companion DEX, and a small fixed set of read-only remote probes.
- **TSB Mobile:** A native Android app built with Kotlin and Jetpack Compose. It checks Termux/Shizuku app presence and Shizuku Binder reachability, shows device details, provides setup guidance, and copies a local report.

The mobile app does **not** currently verify rish, the companion DEX, remote UID, or remote command execution. Use the CLI for those checks.

## Features

### CLI
- Termux environment and version detection
- rish and companion DEX discovery
- Fixed, allowlisted, read-only remote probes
- Remote UID fingerprinting without assuming root
- Sanitized text and JSON reports
- Local-only operation; no telemetry or automatic uploads

### Android app
- Localized in-app interface with a saved language preference
- Termux and Shizuku package detection
- Shizuku Binder reachability via the official Shizuku API/provider
- Android version, API level, manufacturer, and device model
- Quick setup checklist and app launch shortcuts
- Clipboard report with explicit scope limitations
- No privileged Shizuku permission request, shell execution, network permission, or telemetry

## CLI installation

Requirements: Android with Termux, Python 3.10+, Shizuku running, Termux authorized in Shizuku, and the official rish helper plus rish_shizuku.dex.

~~~bash
pkg update && pkg upgrade
pkg install python git
git clone https://github.com/M34nX/Termux-Shizuku-Bridge.git
cd Termux-Shizuku-Bridge
python -m pip install .
~~~

Run:

~~~bash
tsb doctor
tsb status
tsb report
tsb report --json
tsb report --output tsb-report.txt
tsb version
~~~

For a source checkout without installation:

~~~bash
PYTHONPATH=src python -m tsb doctor
~~~

## Android app

See the [Android build guide](android/README.md).

- Minimum Android API: **24**.
- Build environment: JDK 17, Android SDK 35, Gradle 8.9.
- Build command from the android/ directory: `gradle :app:assembleDebug`.
- CI publishes a debug APK artifact and a GitHub beta release only after the Android build succeeds on the release branch.

A debug APK is not a Play Store release and is not production-signed. Review the source and install only builds you trust.

## Privacy and safety

- The CLI runs only fixed commands from an internal allowlist; user input is never interpolated into a shell command.
- The app reads package visibility and Binder availability only; it does not request privileged Shizuku access.
- Reports are copied locally and are not uploaded.
- No telemetry, arbitrary shell execution, permission granting, or Android settings modification.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Security model](docs/SECURITY.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Compatibility](docs/COMPATIBILITY.md)

## Project status

TSB CLI and TSB Mobile are at version 0.2.1. Python CI and Android build CI run separately. The Android APK remains a debug build, not a production-signed release. Physical-device validation is still required; Binder reachability is not proof that the complete rish bridge works.

## License

MIT. See [LICENSE](LICENSE).
