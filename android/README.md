# TSB Mobile

Native Android companion app for Termux-Shizuku-Bridge, built with Kotlin and Jetpack Compose.

## Features in 0.2.0

- English/Persian language switch; selection is saved locally.
- Detects whether the Termux and Shizuku packages are installed.
- Uses the official Shizuku API and ShizukuProvider to check Binder reachability.
- Shows Android release, SDK level, manufacturer, and model.
- Provides a concise setup checklist and shortcuts to open Termux or Shizuku.
- Copies a local diagnostic report to the clipboard after user action.

## Important scope limits

This MVP does **not** verify rish, the rish companion DEX, remote UID, or remote command execution. A reachable Shizuku Binder is not proof that the full Termux → rish → Shizuku bridge is ready.

The app does not request Shizuku's privileged permission, run shell commands, start a UserService, modify Android settings, or upload reports. It declares no INTERNET permission.

## Build requirements

- JDK 17
- Android SDK Platform 35 and Build Tools 35.0.0
- Android Gradle Plugin 8.7.3
- Gradle 8.9
- Minimum Android API 24

Open the android/ directory in Android Studio or build from this directory:

~~~bash
gradle :app:assembleDebug
~~~

The debug APK is generated at:

~~~text
app/build/outputs/apk/debug/app-debug.apk
~~~

GitHub Actions runs the same debug build. When the build succeeds on the project beta branch, the workflow uploads the APK artifact and publishes a GitHub prerelease.

## Install and test

Install only an APK you have reviewed and trust. After installing, open Shizuku and start its service through the official setup instructions. TSB Mobile refreshes the local status when the app resumes or when you tap Refresh.

Physical-device testing is required; CI only verifies that the Android project compiles and packages.
