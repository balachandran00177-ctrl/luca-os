# Troubleshooting & Frequently Asked Questions (FAQ)

Quick solutions to common questions and issues in Luca OS.

---

## Frequently Asked Questions

### Q: Does Luca OS replace my existing operating system?
**A:** Luca OS can run live directly from a USB flash drive without touching your internal hard drive ("Try Luca OS"). You can also choose to install it as your primary operating system or set up a dual-boot configuration alongside Windows.

### Q: Can I run games like Genshin Impact or PUBG Mobile?
**A:** Games that require hardware translation run smoothly after executing `luca-arm-enable`. Note that titles utilizing intrusive kernel-level mobile anti-cheat engines (such as Riot Vanguard or specific root-detecting games) may fail integrity checks without Magisk/KernelSU masking.

### Q: Can I install Linux Flatpaks, Snaps, and DEB packages?
**A:** Yes! Luca OS is 100% compatible with Ubuntu and Debian packages (`apt`), Flatpaks (`flatpak`), and Snap packages.

---

## Troubleshooting Common Issues

### 1. No Internet inside Android Apps
**Cause:** Host firewall (`ufw`) or iptables is blocking the virtual `waydroid0` network bridge.  
**Fix:**
```bash
sudo ufw allow in on waydroid0
sudo ufw route allow in on waydroid0
sudo systemctl restart waydroid-container
```

### 2. Android Apps Won't Open / Refuse to Launch
**Cause:** The current desktop session is using legacy X11 rather than Wayland.  
**Fix:**
Log out of your current session. At the login password screen, click the **Gear Icon** in the bottom-right corner and select **Ubuntu on Wayland** or **Wayland Desktop**.

### 3. Google Play Says "Device is Not Certified"
**Cause:** Android ID has not been registered on Google's certification portal.  
**Fix:**
Run:
```bash
luca-play-id
```
Submit the displayed ID to [https://www.google.com/android/uncertified/](https://www.google.com/android/uncertified/), wait 10 minutes, and restart the container:
```bash
waydroid session stop
sudo systemctl restart waydroid-container
```

### 4. Plymouth Splash Logo Not Visible on Boot
**Cause:** Kernel command-line parameters missing `quiet splash`.  
**Fix:**
Ensure `/etc/default/grub` contains:
```bash
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
```
Then update GRUB:
```bash
sudo update-grub
```
