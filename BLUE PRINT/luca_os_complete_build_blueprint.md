# Luca OS — Complete Build Blueprint (v1.0)

**Project Type:** Android-Style PC Operating System (Custom Linux Distribution + Native Android Container)  
**Base System:** Ubuntu Desktop LTS (24.04 LTS / 26.04 LTS, 64-bit, Wayland)  
**Android Runtime:** Waydroid (LXC-based Android Container with Binder IPC)  
**Build Tool:** Cubic (Custom Ubuntu ISO Creator)  
**Target Output:** Bootable `luca-os-1.0-amd64.iso` (Live USB + Installable PC OS)

---

## 1. System Architecture

Luca OS combines full laptop hardware compatibility (Wi-Fi, Bluetooth, GPUs, desktop apps) with near-native Android app execution in resizable PC windows.

```text
+-----------------------------------------------------------------------+
|                       LUCA OS DESKTOP (GNOME Wayland)                 |
|   [ Bottom Android-Style Dock ]  [ App Drawer ]  [ Quick Settings ]   |
+----------------------------------+------------------------------------+
|       Native Linux PC Apps       |       Waydroid Android Layer       |
|  (Browser, VS Code, Terminal,    |   (Android Framework + Google Play |
|   Media Players, Dev Tools)      |    + ARM Translation via Houdini)  |
+----------------------------------+------------------------------------+
|             Shared Linux Kernel (with Binder & Ashmem IPC)            |
+-----------------------------------------------------------------------+
|            PC Hardware (Intel / AMD / Wi-Fi / Audio / Storage)        |
+-----------------------------------------------------------------------+
```

---

## 2. Prerequisites & Asset Checklist

### Host Machine Requirements
* **Host OS:** 64-bit Ubuntu Desktop (dual-boot or dedicated install recommended; avoid building full ISOs inside WSL)
* **Free Storage:** At least 40 GB free SSD space
* **RAM:** 8 GB minimum (16 GB recommended)
* **Base ISO:** Official **Ubuntu Desktop 24.04 LTS** or **26.04 LTS** (`amd64.iso`)
* **Deployment Drive:** 8 GB+ USB pendrive (formatted with **Ventoy** for easy multi-ISO testing)

### Branding Assets to Prepare First
Create a folder on your host machine (`~/luca-assets/`) with these three files:
1. `luca-wallpaper.png` — Desktop wallpaper (1920x1080 or 2560x1440 PNG)
2. `luca-logo.png` — Transparent OS logo (256x256 PNG) for the Plymouth startup animation
3. `luca-grub-bg.png` — Boot menu background (1920x1080 PNG, no transparency)

---

## 3. Phase 1 — Host Environment Setup

Install **Cubic** from its official PPA and install **QEMU/KVM** so you can test your ISO safely before flashing it to a USB drive.

```bash
# Install Cubic (Custom Ubuntu ISO Creator)
sudo apt-add-repository universe
sudo apt-add-repository ppa:cubic-wizard/release
sudo apt update
sudo apt install --no-install-recommends cubic

# Install QEMU + UEFI firmware for testing ISOs
sudo apt install -y qemu-system-x86 ovmf
```

> **Important:** Do **not** install Cubic via `snap install cubic`. The Snap package with that name is an unrelated virtual machine utility.

---

## 4. Phase 2 — Initialize the Luca OS Project in Cubic

1. Launch **Cubic** from your Applications menu.
2. Create and select a clean project directory: `~/luca-os-build`.
3. Select your downloaded Ubuntu Desktop LTS `.iso`.
4. Set your custom ISO metadata on the **Project Details** screen:
   * **Filename:** `luca-os-1.0-amd64.iso`
   * **Volume ID:** `LUCA_OS_1_0`
   * **Release Name:** `Luca OS`
   * **Disk Name:** `Luca OS 1.0 Desktop amd64`
5. Click **Next**. Cubic will unpack the SquashFS filesystem and open a root **Chroot Terminal**.

All commands in **Phases 3 through 7** are run **inside Cubic's Chroot Terminal**.

---

## 5. Phase 3 — Core Packages & Waydroid Setup

Update package lists and install desktop customization utilities, icons, and system info tools:

```bash
apt update
apt install -y \
  curl \
  ca-certificates \
  gnupg \
  git \
  python3 \
  python3-pip \
  sqlite3 \
  gnome-tweaks \
  gnome-shell-extension-manager \
  papirus-icon-theme \
  wl-clipboard \
  fastfetch
```

Add the official **Waydroid** repository and install the Android container engine:

```bash
curl -s https://repo.waydro.id | bash
apt update
apt install -y waydroid
```

> **Do not run `waydroid init` inside Cubic.** Initializing inside chroot bloats the ISO by ~1.5 GB and requires a live Wayland session. Instead, Luca OS ships with a 1-click setup script (Phase 7).

---

## 6. Phase 4 — System Rebranding to "Luca OS"

### 6.1 Update `/etc/os-release`
Keep `ID_LIKE=ubuntu` and `VERSION_CODENAME` intact so `apt` repositories and PPAs continue working seamlessly. Check your current Ubuntu codename first (`noble` for 24.04, `resolute` for 26.04) and adjust below accordingly:

```bash
cat << 'EOF' > /etc/os-release
PRETTY_NAME="Luca OS 1.0"
NAME="Luca OS"
VERSION_ID="1.0"
VERSION="1.0 (Desktop)"
VERSION_CODENAME=noble
ID=lucaos
ID_LIKE=ubuntu
HOME_URL="https://lucaos.local"
SUPPORT_URL="https://lucaos.local"
BUG_REPORT_URL="https://lucaos.local"
ANSI_COLOR="0;36"
EOF
```

### 6.2 Update `/etc/lsb-release`
```bash
cat << 'EOF' > /etc/lsb-release
DISTRIB_ID=LucaOS
DISTRIB_RELEASE=1.0
DISTRIB_CODENAME=noble
DISTRIB_DESCRIPTION="Luca OS 1.0"
EOF
```

### 6.3 Set Default Hostname
```bash
echo "luca-pc" > /etc/hostname
```

---

## 7. Phase 5 — Android-Style Desktop UX (GNOME Overrides)

1. Drag and drop `luca-wallpaper.png` from `~/luca-assets/` onto Cubic's terminal window and click **Copy**.
2. Move it to the system backgrounds directory:

```bash
mv luca-wallpaper.png /usr/share/backgrounds/luca-wallpaper.png
chmod 644 /usr/share/backgrounds/luca-wallpaper.png
```

3. Create a system-wide GNOME schema override so every new user automatically gets dark mode, Papirus icons, your wallpaper, and a floating Android/tablet-style bottom taskbar:

```bash
cat << 'EOF' > /usr/share/glib-2.0/schemas/99_luca-os.gschema.override
[org.gnome.desktop.background]
picture-uri='file:///usr/share/backgrounds/luca-wallpaper.png'
picture-uri-dark='file:///usr/share/backgrounds/luca-wallpaper.png'

[org.gnome.desktop.screensaver]
picture-uri='file:///usr/share/backgrounds/luca-wallpaper.png'

[org.gnome.desktop.interface]
color-scheme='prefer-dark'
icon-theme='Papirus-Dark'
clock-show-weekday=true
show-battery-percentage=true

[org.gnome.shell.extensions.dash-to-dock]
dock-position='BOTTOM'
extend-height=false
dash-max-icon-size=44
transparency-mode='FIXED'
background-opacity=0.65
show-apps-at-top=false
click-action='minimize-or-previews'
EOF

glib-compile-schemas /usr/share/glib-2.0/schemas/
```

---

## 8. Phase 6 — Custom Boot Experience (Plymouth & GRUB)

### 8.1 Custom Plymouth Startup Logo
1. Drag and drop `luca-logo.png` into Cubic's terminal and click **Copy**.
2. Create the custom Plymouth theme directory and copy the logo:

```bash
mkdir -p /usr/share/plymouth/themes/luca-os
mv luca-logo.png /usr/share/plymouth/themes/luca-os/logo.png
```

3. Create the theme descriptor file `/usr/share/plymouth/themes/luca-os/luca-os.plymouth`:

```bash
cat << 'EOF' > /usr/share/plymouth/themes/luca-os/luca-os.plymouth
[Plymouth Theme]
Name=Luca OS
Description=Luca OS Boot Splash
ModuleName=script

[script]
ImageDir=/usr/share/plymouth/themes/luca-os
ScriptFile=/usr/share/plymouth/themes/luca-os/luca-os.script
EOF
```

4. Create the minimal boot animation script `/usr/share/plymouth/themes/luca-os/luca-os.script`:

```bash
cat << 'EOF' > /usr/share/plymouth/themes/luca-os/luca-os.script
Window.SetBackgroundTopColor(0.05, 0.06, 0.09);
Window.SetBackgroundBottomColor(0.02, 0.03, 0.05);

logo.image = Image("logo.png");
logo.sprite = Sprite(logo.image);
logo.sprite.SetX(Window.GetWidth() / 2 - logo.image.GetWidth() / 2);
logo.sprite.SetY(Window.GetHeight() / 2 - logo.image.GetHeight() / 2);

progress = 0;
fun refresh_callback() {
  progress += 0.05;
  opacity = 0.65 + 0.35 * Math.Sin(progress);
  logo.sprite.SetOpacity(opacity);
}
Plymouth.SetRefreshFunction(refresh_callback);
EOF
```

5. Register and activate the Luca OS Plymouth theme, then rebuild initramfs:

```bash
update-alternatives --install \
  /usr/share/plymouth/themes/default.plymouth default.plymouth \
  /usr/share/plymouth/themes/luca-os/luca-os.plymouth 200

update-alternatives --set default.plymouth \
  /usr/share/plymouth/themes/luca-os/luca-os.plymouth

update-initramfs -u
```

### 8.2 Custom GRUB Background
Drag and drop `luca-grub-bg.png` into Cubic's terminal and place it for installed GRUB menus:

```bash
mkdir -p /boot/grub/themes/luca-os
mv luca-grub-bg.png /boot/grub/themes/luca-os/background.png
echo 'GRUB_BACKGROUND="/boot/grub/themes/luca-os/background.png"' >> /etc/default/grub
```

---

## 9. Phase 7 — Built-In Luca OS Helper Scripts

### 9.1 One-Click Android Subsystem Initializer (`luca-android-setup`)
Sets up Android with Google Play (`GAPPS`), configures firewall rules so Android apps have internet access, and enables PC multi-window mode:

```bash
cat << 'EOF' > /usr/local/bin/luca-android-setup
#!/bin/bash
set -e

echo "=============================================="
echo "   Luca OS — Android Subsystem Setup (GAPPS)  "
echo "=============================================="

sudo waydroid init -s GAPPS
sudo systemctl enable --now waydroid-container

if command -v ufw >/dev/null 2>&1; then
  sudo ufw allow 53/udp || true
  sudo ufw allow 67/udp || true
  sudo ufw default allow FORWARD || true
  sudo ufw allow in on waydroid0 || true
  sudo ufw route allow in on waydroid0 || true
fi

waydroid session start &
sleep 10
waydroid prop set persist.waydroid.multi_windows true
waydroid session stop

echo ""
echo "Setup complete!"
echo "1. Open Waydroid from your App Drawer to launch Android apps in windows."
echo "2. Run 'luca-play-id' if Google Play asks for device certification."
echo "3. Run 'luca-arm-enable' to add ARM app/game compatibility."
EOF

chmod +x /usr/local/bin/luca-android-setup
```

### 9.2 Google Play Certification Helper (`luca-play-id`)
Prints the Android GSF ID needed to register your Waydroid instance with Google Play:

```bash
cat << 'EOF' > /usr/local/bin/luca-play-id
#!/bin/bash
echo "Fetching your Luca OS Android GSF ID..."
sudo waydroid shell -- sh -c "ANDROID_RUNTIME_ROOT=/apex/com.android.runtime ANDROID_DATA=/data ANDROID_TZDATA_ROOT=/apex/com.android.tzdata ANDROID_I18N_ROOT=/apex/com.android.i18n sqlite3 /data/data/com.google.android.gsf/databases/gservices.db \"select * from main where name = 'android_id';\""
echo ""
echo "Copy the number after 'android_id|' and register it at:"
echo "https://www.google.com/android/uncertified/"
echo "Then restart Waydroid: waydroid session stop && sudo systemctl restart waydroid-container"
EOF

chmod +x /usr/local/bin/luca-play-id
```

### 9.3 ARM App & Game Compatibility Helper (`luca-arm-enable`)
Installs `libhoudini` (Intel CPUs) or `libndk` (AMD CPUs) using `waydroid_script` so ARM64 Android apps and games run on x86_64 PCs:

```bash
cat << 'EOF' > /usr/local/bin/luca-arm-enable
#!/bin/bash
set -e

CPU_VENDOR=$(grep -m1 "vendor_id" /proc/cpuinfo | awk '{print $3}')
WORKDIR="$HOME/.local/share/waydroid_script"

if [ ! -d "$WORKDIR" ]; then
  git clone https://github.com/casualsnek/waydroid_script "$WORKDIR"
fi

cd "$WORKDIR"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

if [ "$CPU_VENDOR" = "AuthenticAMD" ]; then
  echo "AMD CPU detected — installing libndk ARM translation layer..."
  sudo venv/bin/python3 main.py install libndk
else
  echo "Intel/x86 CPU detected — installing libhoudini ARM translation layer..."
  sudo venv/bin/python3 main.py install libhoudini
fi

echo "ARM compatibility installed! Restarting Waydroid container..."
sudo systemctl restart waydroid-container
echo "Done."
EOF

chmod +x /usr/local/bin/luca-arm-enable
```

---

## 10. Phase 8 — Cleanup & Building the ISO

Inside Cubic's Chroot Terminal, clear temporary caches to shrink the final image:

```bash
apt autoremove -y
apt clean
rm -rf /tmp/* /var/tmp/*
```

Now finish the build in the **Cubic GUI**:
1. Click **Next** (top-right).
2. **Packages Page:** Optionally uncheck apps you do not want in Luca OS (e.g., LibreOffice, Rhythmbox, Thunderbird) to make the ISO lighter. Click **Next**.
3. **Kernel & Boot Page:**
   * Keep the default LTS Linux kernel selected.
   * Click the **ISO Boot** tab and rename GRUB entries from `Try or Install Ubuntu` to `Try or Install Luca OS`.
   * Click **Next**.
4. **Compression:**
   * Select **zstd** (fast build, great for testing).
   * Select **xz** only for your final public release ISO (smaller file, slower build).
5. Click **Generate**. Your finished image is saved at:
   `~/luca-os-build/luca-os-1.0-amd64.iso`

---

## 11. Phase 9 — Testing & Flashing to Hardware

### 11.1 Test Inside QEMU First (No Reboot Needed)
```bash
qemu-system-x86_64 \
  -enable-kvm \
  -m 4096 \
  -smp 4 \
  -cdrom ~/luca-os-build/luca-os-1.0-amd64.iso \
  -vga virtio \
  -display gtk,gl=on
```

To test **UEFI boot** specifically:
```bash
qemu-system-x86_64 \
  -enable-kvm \
  -m 4096 \
  -smp 4 \
  -bios /usr/share/ovmf/OVMF.fd \
  -cdrom ~/luca-os-build/luca-os-1.0-amd64.iso \
  -vga virtio \
  -display gtk,gl=on
```

### 11.2 Flash to a USB Pendrive
* **Option A (Recommended — Ventoy):** Install **Ventoy** onto your USB pendrive once, then copy `luca-os-1.0-amd64.iso` onto the USB like a normal file. You can keep Windows, Ubuntu, Kali, and Luca OS ISOs on the same drive.
* **Option B (Direct Flash):** Use **Balena Etcher** or `dd`:
  ```bash
  sudo dd if=~/luca-os-build/luca-os-1.0-amd64.iso of=/dev/sdX bs=4M status=progress oflag=sync
  ```
  *(Replace `/dev/sdX` with your actual USB device from `lsblk` — never your main SSD.)*

### 11.3 First-Boot Checklist on Luca OS
After booting/installing Luca OS on your laptop:
1. Connect to Wi-Fi.
2. Open Terminal and run:
   ```bash
   luca-android-setup
   ```
3. Run `luca-arm-enable` if you plan to install ARM-only Android apps or games.
4. Open **Waydroid** from the app menu (or run `waydroid show-full-ui` for tablet mode).
5. To sideload any `.apk` file directly from Linux:
   ```bash
   waydroid app install ~/Downloads/app.apk
   ```

---

## 12. GPU Notes & Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| **Waydroid shows black screen on NVIDIA laptop** | Waydroid does not support proprietary NVIDIA GPU acceleration directly | Switch Waydroid to Intel/AMD integrated graphics (hybrid mode), or force software rendering: `waydroid prop set persist.waydroid.height_padding 0` and configure `ro.hardware.gralloc=default` + `ro.hardware.egl=swiftshader` in `/var/lib/waydroid/waydroid_base.prop` |
| **No internet inside Android apps** | Firewall (`ufw`) blocking `waydroid0` bridge traffic | Re-run `sudo ufw allow in on waydroid0 && sudo ufw route allow in on waydroid0 && sudo systemctl restart waydroid-container` |
| **Waydroid refuses to launch** | Logged into an X11 session instead of Wayland | Log out, click the gear icon at the login screen, and pick the **Wayland** session |
| **Google Play says "Device is not certified"** | Unregistered Android GSF ID | Run `luca-play-id`, submit the ID on Google's uncertified device page, wait 10–15 minutes, and restart Waydroid |
| **Plymouth splash not showing on boot** | Missing `quiet splash` kernel parameters | Verify `GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"` in `/etc/default/grub` and run `sudo update-grub` |

---

## 13. Version Roadmap

* **v1.0 (Current Blueprint):** Bootable Ubuntu-based ISO, Luca OS branding, Android-style GNOME dock, Plymouth splash, Waydroid + Google Play + ARM translation helper scripts.
* **v1.1:** Custom GTK/GNOME Shell theme, custom icon set, preconfigured keyboard shortcuts, and a graphical "Luca Welcome" onboarding app (built in Python + GTK4).
* **v1.2:** Replace default installer with a branded **Calamares** installer and add a custom APT repository for Luca OS OTA updates.
* **v2.0 (Advanced Systems Milestone):** Fork **Bliss OS (AOSP x86)** or compile a custom minimal Linux kernel tailored specifically for Luca OS hardware targets.