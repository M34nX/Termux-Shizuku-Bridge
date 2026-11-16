# Architecture

TSB has two independent clients sharing one privacy-first diagnostic goal.

## Python CLI
- runner.py discovers the official rish helper and companion DEX, then runs commands from a fixed internal allowlist only.
- checks.py collects a structured diagnostic snapshot.
- privacy.py removes local paths and non-default application IDs from support reports by default.
- report.py renders text and JSON output.
- cli.py exposes doctor, status, report, and version commands.

The CLI invokes rish as a subprocess with a finite timeout. User-supplied values are not interpolated into shell commands.

## Native Android app
- MainActivity.kt owns the screen, local language preference, Android package visibility checks, and device snapshot.
- Jetpack Compose renders the dashboard and English/Persian UI.
- Shizuku API + Provider obtains the Shizuku Binder so the app can report whether it is reachable.
- The clipboard report copies a small, locally generated snapshot after the user requests it.

The mobile MVP does not ask for Shizuku's privileged runtime permission, run a UserService, call rish, or execute remote commands. Binder reachability is reported separately from full bridge readiness.

## Data flow

All current checks are local to the device. No backend, analytics endpoint, telemetry, or automatic report upload is configured.

## Design constraints
- Read-only status inspection.
- Least privilege and explicit user control.
- Clear distinction between app installation, Binder reachability, and end-to-end rish connectivity.
- Privacy-preserving reports and local language preference.
