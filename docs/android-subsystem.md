# Android Subsystem & Application Guide

Luca OS integrates an LXC (Linux Containers) Android runtime powered by **Waydroid**. This document explains how Android applications run, how to sideload APKs, and how to configure Google Play certification.

---

## How It Works

Traditional Android emulators run an entire virtual machine (virtual CPU, virtual RAM, virtual disk, virtual graphics card). This causes heavy battery drain, high latency, and poor gaming performance.

**Luca OS takes a different approach:**
- Android runs inside an unprivileged LXC container directly on top of the host Linux kernel.
- Android IPC communicates through native Linux kernel **Binder** and **Ashmem** drivers.
- Hardware graphics are passed directly via the host Wayland compositor using hardware-accelerated DMA-BUF zero-copy buffers.
- Android apps appear as regular floating, resizable windows alongside Linux apps.

---

## 1. Initializing the Subsystem

To initialize Waydroid with Google Play Services (GAPPS):
```bash
luca-android-setup
```
This automated script:
1. Downloads official LineageOS-based Waydroid images with GAPPS pre-packaged.
2. Configures `waydroid-container.service` to start on boot.
3. Configures UFW firewall and iptables NAT routing for the `waydroid0` virtual bridge interface.
4. Enables freeform multi-window mode (`persist.waydroid.multi_windows=true`).

---

## 2. Enabling ARM Translation (for Mobile Games & ARM64 Apps)

Most Android games and mobile apps are compiled only for ARM64 processors. Because PC laptops use x86_64 CPUs, binary translation is required.

Run:
```bash
luca-arm-enable
```
This tool automatically detects your processor:
- **Intel Processors:** Installs Intel `libhoudini` translation.
- **AMD Processors:** Installs `libndk` translation.

Once installed, 99% of Android games and mobile apps run at full speed.

---

## 3. Google Play Certification (`luca-play-id`)

Because Waydroid runs on custom PC hardware, Google Play may initially report that your device is uncertified.

To certify:
1. Open Google Play Store once so Android generates its GSF identity.
2. Run the certification tool:
   ```bash
   luca-play-id
   ```
3. Copy the output ID (it is automatically copied to your clipboard if supported).
4. Go to [Google's Uncertified Device Portal](https://www.google.com/android/uncertified/).
5. Paste the ID and click **Register**.
6. Restart your Waydroid session:
   ```bash
   waydroid session stop
   sudo systemctl restart waydroid-container
   ```
7. Wait 10–15 minutes, then open Google Play and sign in.

---

## 4. Sideloading Android APKs

### Graphical Method:
Right-click any `.apk` file in the file manager and choose **"Open with Luca Package & APK Installer"**, or open the **Luca Installer** app from the dock and browse for the file.

### Terminal Method:
```bash
luca-apk-install ~/Downloads/myapp.apk
```
Or use native waydroid:
```bash
waydroid app install ~/Downloads/myapp.apk
```
Installed apps appear immediately in your GNOME Application Drawer and bottom dock!
