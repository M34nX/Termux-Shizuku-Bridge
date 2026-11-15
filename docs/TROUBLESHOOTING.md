# Troubleshooting

## Start with the basics

Run:

~~~bash
tsb doctor
tsb report
~~~

Check that Termux is current, Python is 3.10+, Shizuku is running, and Termux is authorized in Shizuku.

## rish not found

1. Open Shizuku's terminal-app integration instructions.
2. Export the current official rish helper for Termux.
3. Place it in ~/rish or a directory on PATH.
4. If it is stored elsewhere, set TSB_RISH to its exact path.

Do not download a helper from an untrusted source.

## Companion DEX missing

The official rish helper requires its companion rish_shizuku.dex file.

- Re-export both files using the instructions for your installed Shizuku version.
- Keep the DEX beside rish where possible.
- For a custom path, set TSB_RISH_DEX.
- On Android 14+, follow Shizuku's current export guidance. Writable DEX execution through app_process is restricted; do not weaken file permissions or system security to bypass this.

## Shizuku is stopped

On non-rooted devices, Shizuku's debugging-based service may need to be started again after a reboot. Follow the official Shizuku setup guide for your Android version. TSB does not start the service.

## Termux is not authorized

Open Shizuku and explicitly authorize Termux in its application list. TSB cannot grant its own Shizuku permission.

## Probe fails or times out

- Verify Shizuku displays its service as running.
- Verify the rish helper and companion came from Shizuku's integration flow.
- Check that the remote UID is what you expect; Shizuku may run with Android shell identity rather than root.
- Re-run tsb doctor.

## Unexpected UID

TSB reports the UID returned by the remote shell. It does not assume UID 0. A UID of 2000 commonly represents Android shell; another UID should be reported as-is.

## Report privacy

Reports redact local paths and non-default application IDs by default. Review the report before sharing it. Use --include-paths only when you intentionally want those paths included.

## Official references

- [Shizuku setup](https://shizuku.rikka.app/guide/setup/)
- [Official rish usage](https://github.com/RikkaApps/Shizuku-API/tree/master/rish)
- [Termux installation](https://github.com/termux/termux-app)
