# Security model

TSB is a diagnostic utility, not a privilege manager or a root tool.

## Python CLI
- Only fixed, read-only probes from an internal allowlist are passed to rish.
- User input is never interpolated into shell commands.
- Subprocesses have a finite timeout.
- No shell=True, eval, arbitrary command field, telemetry, or automatic report upload.
- Local paths and custom application IDs are redacted by default.

## Native Android app
- The app checks package visibility for Termux and Shizuku and checks Shizuku Binder reachability through its official API/provider.
- It does not call Shizuku.requestPermission, execute shell commands, start a UserService, or change Android settings.
- Device details and status are displayed locally.
- A report is copied to the clipboard only after the user taps the button.
- The app declares no INTERNET permission and makes no network requests.

## User control

Shizuku authorization is controlled by Shizuku. Review every authorization prompt yourself. TSB does not grant authorization on the user's behalf.

## Scope limitations

A reachable Binder does not prove that the rish helper, its DEX companion, Termux authorization, or remote probes are working. Use the Python CLI's fixed diagnostics for end-to-end bridge checks. Never interpret the mobile status badge as proof of root access.
