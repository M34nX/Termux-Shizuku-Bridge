# Troubleshooting

## Python CLI

Start with:

~~~bash
tsb doctor
tsb report
~~~

Check that Termux is current, Python is 3.10+, Shizuku is running, Termux is authorized in Shizuku, and the official rish helper plus companion DEX are exported.

### rish not found
1. Open Shizuku's terminal-app integration instructions.
2. Export the official rish helper for Termux.
3. Place it in ~/rish or a directory on PATH.
4. If it is stored elsewhere, set TSB_RISH to its exact path.

Do not download a helper from an untrusted source.

### Companion DEX missing
The official rish helper requires rish_shizuku.dex.
- Re-export both files using the instructions for your installed Shizuku version.
- Keep the DEX beside rish where possible.
- For a custom path, set TSB_RISH_DEX.
- On Android 14+, follow Shizuku's current export guidance. Writable DEX execution through app_process is restricted.

### Shizuku is stopped or Termux is unauthorized

On non-rooted devices, Shizuku's debugging-based service may need to be started again after a reboot. Follow the official Shizuku setup guide. Then explicitly authorize Termux in Shizuku. TSB does not start the service or grant permissions.

## Android app

### Shizuku appears unavailable
- Confirm that Shizuku is installed and its service is running.
- Open TSB Mobile again or tap Refresh.
- Confirm that the app includes the ShizukuProvider entry from the official API guide.
- Binder reachability is not proof of a working rish bridge.

### Termux appears missing

Install the official Termux app. Package visibility is checked against the package name com.termux.

### Android build fails
- Use JDK 17.
- Install Android SDK Platform 35 and Build Tools 35.0.0.
- Use Gradle 8.9 with Android Gradle Plugin 8.7.3.
- The app's minimum SDK is API 24 because the selected Shizuku API library declares that minimum.
- Ensure Java and Kotlin compiler targets both use JVM 17.

## Report privacy

The CLI redacts local paths and non-default application IDs by default. The app's report contains device model and package/Binder status. Review it before sharing.
