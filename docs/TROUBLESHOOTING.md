# Troubleshooting

## rish not found
Export the rish helper using Shizuku's terminal-app integration and place it in `~/rish` or a directory on PATH.

## DEX companion missing
Check that `rish_shizuku.dex` is beside rish or in the Termux home directory.

## Authorization or connection failure
Open Shizuku, verify that its service is running, and authorize Termux in Shizuku's own interface. TSB cannot grant authorization.

## Wrong application ID
Check `RISH_APPLICATION_ID`. TSB defaults it to `com.termux` if unset.
