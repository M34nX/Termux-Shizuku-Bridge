<div align="center">

<img src="assets/tsb-banner.svg" alt="Termux-Shizuku-Bridge" width="100%">

# Termux-Shizuku-Bridge

**تشخیص امن و محلی ارتباط Termux، rish و Shizuku | Privacy-first diagnostics**

[English](README.en.md) · [فارسی](README.fa.md)

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?style=flat-square&logo=python)](https://python.org/)
[![Android](https://img.shields.io/badge/Android-Native-3ddc84?style=flat-square&logo=android)](https://android.com/)
[![License](https://img.shields.io/badge/License-MIT-64748b?style=flat-square)](LICENSE)

</div>

---

## فارسی

**TSB (Termux-Shizuku-Bridge)** مجموعه‌ای متن‌باز برای بررسی محلی محیط Termux و ارتباط آن با Shizuku از طریق ابزار رسمی rish است.

### اجزای پروژه
- **TSB CLI:** ابزار پایتونی برای بررسی Termux، rish، فایل DEX همراه و probeهای ثابت و فقط‌خواندنی.
- **TSB Mobile:** اپلیکیشن بومی اندروید با Kotlin و Jetpack Compose؛ نمایش وضعیت نصب Termux و Shizuku، دسترسی Binder، اطلاعات دستگاه، راهنمای راه‌اندازی و گزارش محلی.
- **مستندات دو‌زبانه:** راهنماهای فارسی و انگلیسی.

اپ موبایل در نسخهٔ فعلی وجود rish و اجرای فرمان از راه دور را تأیید نمی‌کند؛ این موارد همچنان از طریق TSB CLI بررسی می‌شوند.

## English

**TSB (Termux-Shizuku-Bridge)** is an open-source, privacy-first toolkit for inspecting the local Termux environment and its Shizuku connection through the official rish helper.

### Project components
- **TSB CLI:** Python diagnostics for Termux, rish, its companion DEX, and fixed read-only probes.
- **TSB Mobile:** A native Kotlin and Jetpack Compose Android companion. It displays Termux/Shizuku installation status, Shizuku Binder reachability, device details, setup guidance, and a local diagnostic report.
- **Bilingual documentation:** English and Persian guides.

The current mobile MVP does not verify rish or remote command execution; use TSB CLI for those checks.

## شروع سریع / Quick links

- [English guide](README.en.md)
- [راهنمای فارسی](README.fa.md)
- [Android app / اپ اندروید](android/README.md)
- [Android app فارسی](android/README.fa.md)
- [Documentation / مستندات](docs/)
- [Security / امنیت](docs/SECURITY.md)
- [Compatibility / سازگاری](docs/COMPATIBILITY.md)
- [GitHub Actions](../../actions)

## Project status / وضعیت پروژه

TSB CLI and TSB Mobile are at version 0.2.1. The Android app remains an early beta; CI verifies builds, but physical-device testing is still required. The mobile app is read-only and makes no network requests or telemetry uploads.

TSB CLI و TSB Mobile در نسخهٔ ۰٫۲٫۱ هستند. اپ اندروید همچنان بتاست؛ CI ساخت را بررسی می‌کند، اما آزمایش روی دستگاه واقعی لازم است. اپ فعلی فقط وضعیت‌ها را می‌خواند و داده‌ای به سرور ارسال نمی‌کند.

## License

MIT — see [LICENSE](LICENSE).
