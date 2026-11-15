# Compatibility and supported environment

This document separates upstream compatibility information from TSB's own test status.

## Current upstream reference points

| Component | Upstream reference | Notes |
|---|---|---|
| Termux app | v0.118.3 | Termux documents Android 7+ for the current app/package environment and recommends v0.118.0+. |
| Shizuku | v13.6.0 | Release notes include Android 16 QPR1 support and a changed service-start command. |
| Android wireless debugging | Android 11+ | Shizuku's official setup guide documents wireless-debugging startup on Android 11+. |
| TSB Python runtime | Python 3.10+ | The project CI matrix covers Python 3.10–3.13. |

These are upstream reference points, not a guarantee that every device, Android skin, or future release works identically.

## What TSB depends on

TSB does not integrate with Shizuku's Android API directly. It invokes the official rish client helper, which forwards a command to the remote shell. The helper and its rish_shizuku.dex companion must be exported for the terminal app using Shizuku's own integration instructions.

The current rish documentation describes rish -c 'command' and the RISH_PRESERVE_ENV environment variable. TSB uses RISH_PRESERVE_ENV=0 by default so Termux-specific paths are not injected into the remote Android shell.

## Android version notes

- **Android 7+:** baseline for the current Termux app/package environment.
- **Android 11+:** Shizuku can be started using Wireless debugging without a computer. Pairing and service-start steps are controlled by Shizuku.
- **Android 14+:** Shizuku's release notes warn that writable DEX files executed by app_process are restricted. Use the current official terminal-app export flow; do not rely on a writable DEX copied to shared storage.
- **Android 16 QPR1:** Shizuku v13.6.0 release notes list support. TSB still requires device-level validation with the current rish helper.

## Shizuku v13.6.0 service-start change

Shizuku v13.6.0 documents a changed command for starting the Shizuku service, using the installed app's libshizuku.so. This is a Shizuku service-start detail, not the TSB-to-rish command path. TSB does not run this command and does not start or restart Shizuku.

## Termux distribution signatures

Install Termux and its plugins from the same distribution source. APKs from F-Droid, GitHub, and other sources can use different signing keys and should not be mixed as in-place updates.

## Validation status

- Unit-test matrix: configured for Python 3.10–3.13; check the Actions tab for actual run results.
- Physical Android tests: not yet confirmed for this update.
- Device/vendor coverage: not claimed.
- Compatibility claims must be updated against upstream release notes rather than inferred from a version number alone.

## Official references

- [Termux app installation and compatibility](https://github.com/termux/termux-app)
- [Shizuku setup guide](https://shizuku.rikka.app/guide/setup/)
- [Shizuku releases](https://github.com/RikkaApps/Shizuku/releases)
- [Official rish usage](https://github.com/RikkaApps/Shizuku-API/tree/master/rish)
