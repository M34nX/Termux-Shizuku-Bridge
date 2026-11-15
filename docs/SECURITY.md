# Security model

TSB is a diagnostic tool, not a privilege manager.

- Only fixed read-only probes are passed to rish.
- User input is never interpolated into shell commands.
- Subprocesses have a finite timeout.
- No shell=True, eval, remote telemetry, automatic uploads, or privilege escalation.
- Support reports redact local paths and non-default application IDs unless the user explicitly opts in.

Shizuku authorization is controlled by the Shizuku application. Review every authorization prompt yourself.
