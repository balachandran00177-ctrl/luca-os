# Luca OS — Live Boot Pendrive & Persistence Guide

This guide explains how to create, run, and master the **Live Boot Pendrive Version** of Luca OS.

---

## 🌟 What is the Live Pendrive Version?

Unlike traditional live Linux USBs that reset every reboot, the **Luca OS Live Pendrive Version** is a fully functional, portable operating system carried on a USB flash drive:

- **💾 True Persistence (`casper-rw`):** All documents, downloads, installed Android apps, Google Play store sessions, and Wi-Fi networks survive computer shutdowns and reboots.
- **⚡ Zero Touch on Internal Disks:** Boots without modifying your PC's internal Windows or macOS drive.
- **🚀 RAM Boot Mode (`toram`):** Can copy the entire system into RAM upon boot for lightning-fast application launches.
- **🛡️ Safe Hardware Fallback:** Includes safe graphics mode for systems with unusual or legacy GPU hardware.

---

## 1. Creating the Live USB with Persistence

### Method 1: Using `luca-live-creator` (Recommended GUI)
Run the built-in creator tool:
```bash
python apps/luca-live-creator/luca_live_creator.py
```
1. **Select ISO:** Choose `luca-os-1.0-amd64.iso`.
2. **Select USB Drive:** Pick your USB pendrive (8 GB minimum; 16 GB–64 GB recommended).
3. **Persistence Slider:** Drag the slider to your desired persistent storage size (e.g., 4 GB, 8 GB, or 16 GB).
4. Click **"Create Live USB Pendrive"**.

### Method 2: Ventoy with Persistence Plugin
If using Ventoy:
1. Format your pendrive with Ventoy.
2. Copy `luca-os-1.0-amd64.iso` to the USB.
3. Create a `casper-rw` persistence image file using `luca-live-persist create 8 casper-rw.dat`.
4. Add the image to `ventoy/ventoy.json` under `persistence`.

---

## 2. Booting from the Pendrive

1. Insert your USB pendrive into the PC.
2. Power on the PC and press the boot selection key (`F12`, `F11`, `F9`, or `Esc`).
3. Select your USB drive under UEFI.
4. From the Luca OS Boot Menu, select:
   - **`Try or Install Luca OS (Live USB with Persistence)`**: Default mode with persistent storage.
   - **`Try Luca OS (Ultra-Fast RAM Mode - toram)`**: Loads OS into system RAM.
   - **`Try Luca OS (Safe Graphics / Software Fallback)`**: For laptops experiencing display issues.

---

## 3. Live Desktop Features

Once booted into the Live Desktop:
- **Luca Live Hub:** Displays live session health, persistence space remaining, and offers a 1-click option to permanently install to disk.
- **Luca App Store:** Browse and install both Android mobile apps and Linux PC software.
- **Luca Welcome:** Quick setup wizard for Wi-Fi and container initialization.

---

## 4. Upgrading to Permanent Installation
If you decide to install Luca OS onto your internal SSD or NVMe drive, launch the **Calamares Installer** from the Live Hub or application menu. The installer provides guided partitioning alongside Windows (dual boot) or full disk installation.
