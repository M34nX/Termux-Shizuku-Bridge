"""Fixed, read-only probes and application constants."""
from __future__ import annotations
VERSION = "0.2.0"
DEFAULT_APPLICATION_ID = "com.termux"
COMMAND_TIMEOUT_SECONDS = 8
PROBES = {
    "uid": "id -u",
    "android_release": "getprop ro.build.version.release",
    "android_sdk": "getprop ro.build.version.sdk",
    "manufacturer": "getprop ro.product.manufacturer",
}
