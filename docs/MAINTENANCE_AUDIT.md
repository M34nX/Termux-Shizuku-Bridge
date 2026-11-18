# Maintenance audit — November 2026

## Scope reviewed
Repository tree, CLI modules, Python packaging and tests, Python and Android CI workflows, Android manifest/Gradle configuration, native activity, and compatibility/security documentation.

## Verified strengths
- The CLI is packaged through `pyproject.toml` and exposes the `tsb` entry point.
- The test suite covers the fixed probe allowlist, blocked-command behavior, report redaction (including nested paths), JSON/text rendering, and DEX discovery.
- CI runs the Python tests across Python 3.10–3.14.
- The project explicitly documents that the Android MVP does not verify rish or remote command execution.

## Findings and limitations
1. **Device validation remains outstanding (P1).** Hosted CI can build the Android app, but it cannot establish Shizuku Binder, rish, companion-DEX, or remote-probe behavior on physical devices. The mobile app explicitly reports only package visibility and Binder reachability.
2. **CLI regression coverage can be broadened (P2).** Current tests cover core helpers but do not demonstrate end-to-end CLI output and exit behavior for missing Termux, missing rish, or unavailable Shizuku.
3. **Android release artifact mutability (P2).** `.github/workflows/android.yml` publishes to the fixed `v0.2.1` tag on every qualifying push to `main` and uses `gh release upload --clobber` when the release exists. A later Android change can therefore replace the APK attached to the same release tag. Prefer immutable version tags or a manual/tag-triggered release process.
4. **Compatibility documentation mismatch (P3, corrected in this PR).** `docs/COMPATIBILITY.md` said Python 3.10–3.13 while `.github/workflows/tests.yml` already tested 3.10–3.14. The documentation now matches the workflow.
5. **Python test success is not Android runtime validation.** The Android build workflow verifies compilation/package assembly only; physical-device behavior remains unverified.

## Recommended next steps
- Add a documented Android device test matrix (Android/API level, Termux version, Shizuku version, rish version) and record results from real hardware.
- Add CLI-level tests for exit codes and graceful handling of missing prerequisites.
- Make Android release tags immutable; publish each APK against a new version tag rather than overwriting an existing release asset.
- Keep all probes allowlisted and read-only; add regression tests before changing probe behavior.
- Publish a sanitized example report and verify that every new field passes through the privacy sanitizer.

## Status
This is a source-based maintenance review. The compatibility-matrix wording was corrected in this PR. CI must validate the updated branch; no physical Android device test was performed as part of this review.