# ⚡ Luca OS

<div align="center">

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Base: Ubuntu LTS](https://img.shields.io/badge/Base-Ubuntu%20LTS%20(Wayland)-E95420.svg)](https://ubuntu.com)
[![Android: Waydroid](https://img.shields.io/badge/Android-Waydroid%20LXC-3DDC84.svg)](https://waydro.id)
[![Architecture: x86__64](https://img.shields.io/badge/Arch-x86__64%20(Intel%2FAMD)-555555.svg)]()
[![Edition: Live Pendrive + Persistent](https://img.shields.io/badge/Edition-Live%20Pendrive%20%2B%20Persistent-00F2FE.svg)]()

**An Advanced, User-Friendly, Open-Source Operating System with Native Android Container and High-Performance Live USB Boot with Persistent Storage.**

[Features](#-key-features) • [Live Boot Pendrive](#-live-boot-pendrive-edition) • [Architecture](#-system-architecture) • [App Store](#-unified-app-store) • [Getting Started](#-getting-started) • [Documentation](#-documentation)

</div>

---

## 🌟 Overview

**Luca OS** is a cutting-edge hybrid PC operating system designed to give you the ultimate computing freedom:
1. **Desktop Linux Stability & Power:** Full multi-monitor support, terminal, dev tools, and native PC gaming with Steam and Proton.
2. **Native Android App Execution:** Run millions of Android mobile apps and games side-by-side in resizable desktop windows via an unprivileged LXC container (**Waydroid**) with zero CPU emulation overhead.
3. **Advanced Live Boot Pendrive Version:** Carry your entire operating system on an 8 GB–64 GB USB pendrive. Boot on any PC with **True Persistent Storage (`casper-rw`)** so your files, Wi-Fi networks, and installed Android apps are never lost.

```text
+---------------------------------------------------------------------------------+
|                         LUCA OS DESKTOP (GNOME Wayland)                         |
|   [ Floating Bottom Dock ]    [ Luca App Store ]    [ Quick Settings Panel ]    |
+------------------------------------+--------------------------------------------+
|        Native Linux Apps           |           Waydroid Android Layer           |
|   (Browser, Dev Tools, Steam,      |   (Android Framework + Google Play Store   |
|    Media Players, Flatpaks, DEB)   |    + ARM Translation via Libhoudini/NDK)   |
+------------------------------------+--------------------------------------------+
|             Shared Linux Kernel (Binder & Ashmem IPC, Zero-Copy GPU)            |
+---------------------------------------------------------------------------------+
|   PC Hardware / Live USB Pendrive (Casper Persistence Overlay / ZRAM Optimizer) |
+---------------------------------------------------------------------------------+
```

---

## 💾 Live Boot Pendrive Edition

The **Live Boot Pendrive Edition** allows you to plug Luca OS into any laptop or desktop and boot into a fully functional, personalized environment without touching the host's internal storage:

- **🔄 True Persistent Storage:** Files, settings, browser logins, and downloaded Android apps persist across reboots via an ext4 `casper-rw` container.
- **⚡ Ultra-Fast RAM Mode (`toram`):** Load the entire live system into system RAM at boot for instantaneous responsiveness and zero disk read delay.
- **🛡️ Safe Graphics Fallback:** Includes a dedicated boot mode for troubleshooting tricky hybrid or legacy GPUs.
- **🛠️ Luca Live USB Creator:** Cross-platform graphical tool to format, partition, and create your bootable persistent USB pendrive with 1 click.
- **🖥️ Luca Live Hub:** Desktop assistant displaying live persistence health, free storage, and a 1-click option to permanently install to disk.

---

## ✨ Key Features

- **🛍️ Unified Luca App Store (`luca-store`):** Browse, search, and install both Android mobile apps (WhatsApp, Instagram, Subway Surfers, Aurora Store, F-Droid) and Linux software (Firefox, VS Code, Steam, Spotify, LibreOffice, GIMP) in one place.
- **🚀 Native Android Multi-Window:** Run mobile apps alongside Linux desktop windows with full 60–120 FPS hardware GPU acceleration.
- **🎮 Auto-Configuring ARM Translation:** Hardware-sensing engine (`luca-arm-enable`) auto-detects Intel vs. AMD processors to enable `libhoudini` or `libndk`.
- **🧙 Luca Welcome Onboarding Wizard:** First-boot companion guiding users through Wi-Fi connection, Google Play certification, and theme customization.
- **📦 Drag-and-Drop Sideloading (`luca-installer`):** Sideload any `.apk` or `.deb` file with a single click.
- **🎨 Modern Android-Style UI:** Centered floating dock, Papirus-Dark icons, smooth Plymouth boot animation, and high-contrast dark theme.
- **💿 Branded Calamares Installer:** Professional, guided graphical installer for permanent dual-boot or dedicated disk installation.

---

## 🧰 Software Suite & Helper Utilities

| Application / Script | Role |
|---|---|
| `luca-live-creator` | Graphical Live USB flasher with configurable persistence slider |
| `luca-store` | Visual software center for Android APKs and Linux Flatpaks/APTs |
| `luca-live-hub` | Floating live session assistant and persistence monitor |
| `luca-welcome` | First-boot desktop onboarding wizard and specs dashboard |
| `luca-installer` | 1-click APK and DEB application sideload manager |
| `luca-control` | Subsystem controller for Waydroid and GPU passthrough |
| `luca-live-detect` | Live USB detection, zram memory optimizer, and persistence checker |
| `luca-live-persist` | Utility to create, resize, or inspect `casper-rw` persistence containers |
| `luca-android-setup` | Production initializer for Waydroid + GAPPS + network bridge |
| `luca-arm-enable` | Installs Intel `libhoudini` or AMD `libndk` ARM translation |
| `luca-play-id` | Google Play certification extractor with auto-copy |
| `luca-gpu-config` | Multi-GPU switcher (Auto / iGPU / Discrete / Software SwiftShader) |

---

## 🚀 Creating & Booting the Live USB

### 1. Create with Luca Live USB Creator (Recommended)
Launch the graphical creator:
```bash
make live-creator
# Or run directly: python apps/luca-live-creator/luca_live_creator.py
```
1. Select your `luca-os-1.0-amd64.iso`.
2. Choose your target USB pendrive (8 GB or larger).
3. Adjust the **Persistence Slider** (e.g. 4 GB, 8 GB, 16 GB).
4. Click **Create Live USB Pendrive**.

### 2. Booting on PC
1. Plug the pendrive into your PC and press the boot key (`F12`, `F11`, `F9`, or `Esc`).
2. Select your USB drive under UEFI.
3. Choose **`🚀 Try or Install Luca OS (Live USB with Persistence)`**.

---

## 🔨 Developer Commands

```bash
make assets        # Regenerate all SVGs, wallpapers, and Plymouth/GRUB branding
make test-gui      # Run verification tests on all 6 GUI applications
make live-creator  # Launch the Live USB Creator application
make store         # Launch the Unified Luca App Store
make host-setup    # Install host build dependencies (Cubic, QEMU, KVM)
make iso           # Package and generate the bootable ISO
make qemu-uefi     # Test the generated ISO in QEMU virtual machine
```

---

## 📚 Documentation
- [Live Boot Pendrive & Persistence Guide](docs/live-boot-pendrive-guide.md)
- [Getting Started Guide](docs/getting-started.md)
- [Android Subsystem & APK Guide](docs/android-subsystem.md)
- [GPU Acceleration & NVIDIA Optimus Guide](docs/gpu-guide.md)
- [System Architecture](docs/architecture.md)
- [Troubleshooting & FAQ](docs/troubleshooting.md)

---

## ⚖️ License
Distributed under the **GNU General Public License v3.0 (GPL-3.0)**. See [LICENSE](LICENSE).
