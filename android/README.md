# TSB Mobile

Native Android companion app for Termux-Shizuku-Bridge, built with Kotlin and Jetpack Compose.

## Current MVP

- Detects whether the Termux and Shizuku apps are installed.
- Checks whether the Shizuku binder is reachable using the official Shizuku API.
- Provides a concise setup checklist.
- Copies a local diagnostic report to the clipboard.
- Makes no network requests and sends no telemetry.

The MVP does **not** claim to verify rish, its companion DEX, remote UID, or remote command execution. Those checks remain in the Python TSB CLI until a separately reviewed native implementation is added.

## Build

Requirements: Android Studio (or Android SDK), JDK 17, and Android SDK 35.

From this directory:

```bash
gradle :app:assembleDebug
```

The APK is generated at `app/build/outputs/apk/debug/app-debug.apk`.

## Safety and privacy

The app performs local, read-only checks. It does not request Shizuku privileged permission, execute shell commands, alter Android settings, start services, or upload reports.
