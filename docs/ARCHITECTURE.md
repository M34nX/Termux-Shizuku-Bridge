# Architecture

TSB separates environment discovery, the restricted rish runner, diagnostic checks, privacy filtering, report rendering, and CLI orchestration.

- `runner.py`: locates rish and runs only commands present in the internal allowlist.
- `checks.py`: assembles a structured diagnostic snapshot.
- `privacy.py`: removes local paths and custom application identifiers by default.
- `report.py`: renders text and JSON.
- `cli.py`: exposes doctor, status, report, and version.

The application performs no network requests and does not change Android settings or grant permissions.
