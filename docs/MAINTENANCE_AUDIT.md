# Maintenance audit — November 2026

## Scope reviewed
Repository root, README, Python packaging metadata, the core unit-test module, and the Python CI workflow.

## Verified strengths
- The CLI is packaged through `pyproject.toml` and exposes the `tsb` entry point.
- The test suite covers the fixed probe allowlist, blocked-command behavior, report redaction (including nested paths), JSON/text rendering, and DEX discovery.
- CI runs the Python tests across Python 3.10–3.14.
- The project explicitly documents that the Android MVP does not verify rish or remote command execution.

## Findings and limitations
1. **Device validation remains outstanding.** The README identifies physical-device testing as required; hosted CI cannot establish Binder/Shizuku behavior on real Android devices.
2. **CLI regression coverage can be broadened.** Current tests exercise core helpers but do not, from the reviewed test file, demonstrate end-to-end CLI output and exit behavior for missing Termux, missing rish, or unavailable Shizuku.
3. **Release verification is not equivalent to device compatibility.** A passing Python test job does not validate Android/Kotlin builds or runtime behavior.

## Recommended next steps
- Add a documented Android device test matrix (Android/API level, Termux version, Shizuku version, rish version).
- Add CLI-level tests for exit codes and graceful handling of missing prerequisites.
- Keep all probes allowlisted and read-only; add regression tests before changing probe behavior.
- Publish a sanitized example report and verify that every new field passes through the privacy sanitizer.

## Status
This is a source-based maintenance review, not a claim that unexecuted tests passed. No Android device test was performed as part of this review.