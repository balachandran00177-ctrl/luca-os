# Changelog — Luca OS

All notable changes to the Luca OS project are documented in this file.

## [1.0.0] - 2026-11-24

### Added
- **Base System Architecture:** Custom Ubuntu Desktop LTS live ISO blueprint with Wayland desktop compositor and LXC-based Waydroid container runtime.
- **Android Subsystem Automation (`luca-android-setup`):** 1-click initialization with Google Play (`GAPPS`), network bridge configuration, and multi-window mode.
- **Google Play Certification Helper (`luca-play-id`):** Automated retrieval of Android GSF ID with automatic clipboard copy for device certification.
- **ARM Translation Engine (`luca-arm-enable`):** Automated CPU architecture detection (Intel vs AMD) with seamless installation of `libhoudini` and `libndk`.
- **Graphical Application Suite:**
  - `luca-welcome`: Interactive first-boot onboarding wizard with hardware inspection, essential app installer, and subsystem toggles.
  - `luca-installer`: 1-click APK and Linux package manager with drag-and-drop support.
  - `luca-control`: Subsystem control center for Waydroid container state and GPU acceleration modes.
- **Branding & Visual Themes:**
  - High-resolution SVG and PNG cyber-dark wallpapers (`luca-wallpaper.png`).
  - Animated Plymouth boot splash theme (`luca-os.plymouth`).
  - Modern high-contrast GRUB bootloader theme (`theme.txt`).
  - Android-style bottom dock with GNOME schema overrides.
- **Build & Test Automation Toolchain:**
  - `setup-host.sh`: Automated dependency installation for Cubic, QEMU, KVM, and image utilities.
  - `build-iso.sh`: Automated staging and chroot injection pipeline.
  - `test-qemu.sh`: 1-click VM launcher supporting both UEFI and BIOS modes.
  - `flash-usb.sh`: Protected interactive USB pendrive flasher.
