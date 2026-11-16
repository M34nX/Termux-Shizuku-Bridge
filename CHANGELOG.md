# Changelog

## TSB 0.2.1 — Privacy and CI maintenance (2026-11-16)
- Expanded default path redaction to common Android app-data, shared-storage, Linux home, and macOS user paths, including nested report text.
- Kept explicit `--include-paths` behavior: local paths are included only when the user opts in.
- Added regression coverage for path redaction and the fixed-command allowlist.
- Bumped CLI and Android app versions to 0.2.1; Android versionCode is now 3.
- Enabled Android build CI on pushes to `main` and extended the Python CI matrix to 3.14.
- Clarified the mobile status label to say Binder is reachable, not that the full bridge is online.

## یادداشت تغییرات

### TSB 0.2.1 — بهبود حریم خصوصی و CI
- پالایش مسیرهای خصوصی اندروید، حافظهٔ اشتراکی، پوشهٔ خانگی لینوکس و پوشهٔ کاربر macOS در گزارش‌ها گسترش یافت.
- گزینهٔ `--include-paths` فقط با انتخاب صریح کاربر مسیرها را حفظ می‌کند.
- تست‌های بازگشت برای پالایش مسیر و محدودماندن فرمان‌ها به فهرست ثابت اضافه شد.
- نسخهٔ CLI و اپ اندروید به ۰٫۲٫۱ ارتقا یافت و versionCode اندروید به ۳ رسید.
- ساخت اندروید روی push به شاخهٔ `main` نیز اجرا می‌شود و ماتریس پایتون تا ۳٫۱۴ گسترش یافت.
- برچسب وضعیت موبایل دقیق‌تر شد: فقط دسترسی Binder را نشان می‌دهد، نه آنلاین‌بودن کل پل.

## TSB Mobile 0.2.0-beta.1 — Native Android companion
- Added a Kotlin and Jetpack Compose Android application.
- Added a Persian/English in-app language switch with a locally saved preference.
- Added Termux/Shizuku package detection, Shizuku Binder reachability, and device information.
- Added setup guidance, app shortcuts, and a local clipboard diagnostic report.
- Registered the official ShizukuProvider and aligned Android minimum SDK and JVM build targets.
- Added Android build CI and a beta-release workflow.
- The mobile MVP does not yet verify rish or remote command execution.

## TSB CLI 0.2.0 — Repository redesign
- Introduced a modular Python package.
- Added fixed read-only diagnostics and structured reports.
- Added privacy sanitization, tests, CI, security documentation, and Termux install/uninstall scripts.

## یادداشت تغییرات

### TSB Mobile 0.2.0-beta.1
- اپ بومی اندروید با Kotlin و Jetpack Compose اضافه شد.
- تغییر زبان فارسی/انگلیسی با ذخیرهٔ محلی انتخاب کاربر اضافه شد.
- تشخیص نصب Termux و Shizuku، دسترسی Binder و اطلاعات دستگاه اضافه شد.
- راهنمای راه‌اندازی، میانبر برنامه‌ها و گزارش تشخیصی محلی اضافه شد.
- ShizukuProvider رسمی ثبت و حداقل SDK و هدف‌های کامپایل هماهنگ شدند.
- CI ساخت اندروید و workflow انتشار بتا اضافه شد.
- نسخهٔ فعلی اپ موبایل هنوز اجرای rish یا فرمان راه‌دور را تأیید نمی‌کند.

### TSB CLI 0.2.0
- بستهٔ پایتون ماژولار معرفی شد.
- بررسی‌های ثابت فقط‌خواندنی و گزارش‌های ساختاریافته اضافه شدند.
- پالایش حریم خصوصی، تست‌ها، CI و مستندات امنیتی و نصب Termux اضافه شدند.
