# Getting Started with Luca OS

This guide walks you through acquiring, testing, and installing **Luca OS 1.0** on your computer.

---

## 1. System Requirements

- **Processor:** 64-bit Intel or AMD processor (2 cores minimum, 4 cores recommended).
- **Virtualization Support:** Intel VT-x or AMD-V enabled in your BIOS/UEFI settings.
- **RAM:** 4 GB minimum (8 GB+ recommended for running multiple Android apps simultaneously).
- **Storage:** 25 GB free disk space (NVMe or SATA SSD highly recommended).
- **Display:** 1280x720 minimum (1920x1080 or higher recommended).

---

## 2. Creating a Bootable USB Pendrive

### Method A: Ventoy (Recommended Multi-Boot Setup)
Ventoy is the easiest and cleanest way to test and install Luca OS:
1. Download **[Ventoy](https://www.ventoy.net/)** and install it on your USB drive (8 GB or larger).
2. Once Ventoy is installed, your USB drive acts like a normal flash drive.
3. Simply drag and drop `luca-os-1.0-amd64.iso` onto the USB drive.
4. You can keep multiple ISOs (Luca OS, Windows, Ubuntu) on the same drive without reformatting!

### Method B: Direct Flash (Linux / macOS)
Use the included safe flasher script:
```bash
sudo bash scripts/build/flash-usb.sh path/to/luca-os-1.0-amd64.iso
```
The script will list only removable USB drives and ask for explicit confirmation before writing.

### Method C: Direct Flash (Windows)
1. Download **Balena Etcher** or **Rufus**.
2. Select `luca-os-1.0-amd64.iso`.
3. Select your USB drive and click **Flash**.

---

## 3. Booting into Luca OS

1. Plug the bootable USB drive into your target laptop or desktop.
2. Power on the PC and immediately press your motherboard's boot menu key:
   - **Dell:** `F12`
   - **HP:** `F9` or `Esc`
   - **Lenovo:** `F12` or `Fn + F12`
   - **ASUS:** `F8` or `Esc`
   - **Acer:** `F12`
3. Select your USB drive from the UEFI boot options.
4. From the Luca OS GRUB boot menu, select **"Try or Install Luca OS"**.

---

## 4. First-Boot Onboarding

Upon reaching the desktop:
1. The **Luca OS Welcome** application will launch automatically.
2. Connect to your Wi-Fi network using the top-right Quick Settings panel.
3. Click **"Run Setup"** in the Welcome app or run `luca-android-setup` in the terminal to initialize the Android subsystem.
4. Open the bottom application dock to start launching apps!
