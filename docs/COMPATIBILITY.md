# Compatibility and supported environment

This page distinguishes upstream compatibility information from TSB's own test status.

## Python CLI

| Component | Requirement or reference |
|---|---|
| Termux app | Current official Termux release; follow the upstream Android support policy |
| Python | 3.10 or newer |
| Shizuku | Installed, running, and explicitly authorizing Termux |
| rish | Official helper exported through Shizuku's terminal-app integration |
| Companion | rish_shizuku.dex exported for the terminal app |

The Python CI matrix covers Python 3.10–3.14. Check GitHub Actions for the result of each commit.

## Native Android app

| Component | Version |
|---|---|
| Minimum Android SDK | 24 |
| Compile SDK | 35 |
| Target SDK | 35 |
| JDK | 17 |
| Android Gradle Plugin | 8.7.3 |
| Gradle | 8.9 |
| Kotlin | 2.0.21 |
| Shizuku API / Provider | 13.1.5 |

The selected Shizuku API 13.1.5 dependency declares minSdk 24; the app therefore uses API 24 as its minimum. The app uses the official ShizukuProvider mechanism to acquire the Binder.

## Android and Shizuku notes
- Shizuku can be started through Wireless debugging on Android 11+.
- On non-rooted devices, the debugging-based service generally needs to be started again after a reboot.
- The app only reports Shizuku Binder reachability. It does not report remote UID or prove rish execution.
- TSB CLI uses the official rish helper and its companion DEX. Follow Shizuku's current export instructions, especially on Android 14+.

## Validation status
- Python unit tests: use the Actions tab for the current commit's result.
- Android debug build: use the Android app build workflow for the current commit.
- Physical-device tests: still required for each supported device family and Android release.
- No universal device/vendor compatibility guarantee is made.

## Official references
- [Shizuku API developer guide](https://github.com/RikkaApps/Shizuku-API)
- [Shizuku API 13.1.5 on Maven Central](https://central.sonatype.com/artifact/dev.rikka.shizuku/api/versions)
- [Android Gradle Plugin compatibility](https://developer.android.com/build/releases/about-agp)
- [Termux app](https://github.com/termux/termux-app)
- [Shizuku setup guide](https://shizuku.rikka.app/guide/setup/)
