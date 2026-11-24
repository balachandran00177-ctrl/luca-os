#!/usr/bin/env bash
# ==============================================================================
# Luca OS — Automated ISO Build Pipeline (scripts/build/build-iso.sh)
# Automates overlay merging, package staging, Plymouth branding,
# schema compilation, and ISO packaging.
# ==============================================================================

set -euo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
BUILD_DIR="${BUILD_DIR:-$HOME/luca-os-build}"
OUTPUT_ISO="$BUILD_DIR/luca-os-1.0-amd64.iso"

echo -e "${CYAN}======================================================================${NC}"
echo -e "${CYAN}                ⚡ Luca OS 1.0 — ISO Build System                     ${NC}"
echo -e "${CYAN}======================================================================${NC}"
echo "Project Root: $ROOT_DIR"
echo "Build Directory: $BUILD_DIR"
echo ""

# Ensure assets are up-to-date
echo -e "${CYAN}[Step 1/5]${NC} Generating latest branding assets and wallpapers..."
python3 "$SCRIPT_DIR/generate-assets.py"

mkdir -p "$BUILD_DIR/staging"

# Mode Selection: Cubic GUI helper or Headless Chroot setup
echo ""
echo "Select Build Method:"
echo "  1) Launch / Prepare for Cubic GUI (Recommended for visual ISO customization)"
echo "  2) Prepare automated staging overlay bundle"
echo "  3) Help / Documentation"
read -rp "Enter choice [1-3] (Default: 1): " CHOICE
CHOICE="${CHOICE:-1}"

case "$CHOICE" in
    1)
        echo -e "${CYAN}[Step 2/5]${NC} Preparing Cubic Project Workspace..."
        mkdir -p "$BUILD_DIR/assets"
        
        # Copy assets into a convenient staging folder for Cubic drag-and-drop
        cp -r "$ROOT_DIR/assets" "$BUILD_DIR/"
        cp -r "$ROOT_DIR/overlay" "$BUILD_DIR/"
        cp -r "$ROOT_DIR/scripts/bin" "$BUILD_DIR/"
        cp -r "$ROOT_DIR/apps" "$BUILD_DIR/"

        # Generate a 1-click in-chroot injector script
        cat << 'EOF' > "$BUILD_DIR/inject-luca-into-chroot.sh"
#!/usr/bin/env bash
# Run this script INSIDE Cubic's Chroot terminal to apply Luca OS customizations
set -euo pipefail

echo "==> [Luca OS Injector] Updating package lists..."
apt-get update
apt-get install -y \
  curl ca-certificates gnupg git python3 python3-pip sqlite3 \
  gnome-tweaks gnome-shell-extension-manager papirus-icon-theme \
  wl-clipboard fastfetch

echo "==> [Luca OS Injector] Installing Waydroid container runtime..."
curl -s https://repo.waydro.id | bash
apt-get update
apt-get install -y waydroid

echo "==> [Luca OS Injector] Installing Luca OS CLI tools to /usr/local/bin..."
cp -r /luca-stage/scripts/bin/* /usr/local/bin/
chmod +x /usr/local/bin/luca-*

echo "==> [Luca OS Injector] Installing Luca Desktop Applications..."
mkdir -p /opt/luca-os/apps
cp -r /luca-stage/apps/* /opt/luca-os/apps/

# Symlinks for applications
ln -sf /opt/luca-os/apps/luca-welcome/luca_welcome.py /usr/local/bin/luca-welcome
ln -sf /opt/luca-os/apps/luca-installer/luca_installer.py /usr/local/bin/luca-installer
ln -sf /opt/luca-os/apps/luca-control/luca_control.py /usr/local/bin/luca-control
chmod +x /usr/local/bin/luca-welcome /usr/local/bin/luca-installer /usr/local/bin/luca-control

echo "==> [Luca OS Injector] Applying System Configuration Overlay..."
cp -r /luca-stage/overlay/* /

echo "==> [Luca OS Injector] Compiling GNOME GSettings schemas..."
glib-compile-schemas /usr/share/glib-2.0/schemas/

echo "==> [Luca OS Injector] Activating Plymouth Theme..."
update-alternatives --install \
  /usr/share/plymouth/themes/default.plymouth default.plymouth \
  /usr/share/plymouth/themes/luca-os/luca-os.plymouth 200

update-alternatives --set default.plymouth \
  /usr/share/plymouth/themes/luca-os/luca-os.plymouth

update-initramfs -u

echo "==> [Luca OS Injector] Cleaning up apt cache..."
apt-get autoremove -y
apt-get clean
rm -rf /tmp/* /var/tmp/*

echo "==> [Luca OS Injector] Done! You can now click Next in Cubic."
EOF
        chmod +x "$BUILD_DIR/inject-luca-into-chroot.sh"

        echo ""
        echo -e "${GREEN}✓ Cubic workspace files staged at: $BUILD_DIR${NC}"
        echo ""
        echo "Instructions to build with Cubic:"
        echo "  1. Launch Cubic: sudo cubic"
        echo "  2. Select project directory: $BUILD_DIR"
        echo "  3. Select Ubuntu 24.04 / 26.04 Desktop ISO"
        echo "  4. Set Metadata:"
        echo "     - Filename: luca-os-1.0-amd64.iso"
        echo "     - Volume ID: LUCA_OS_1_0"
        echo "     - Release Name: Luca OS 1.0"
        echo "  5. In Cubic chroot terminal, drag the folder '$BUILD_DIR' as '/luca-stage' and run:"
        echo "     bash /luca-stage/inject-luca-into-chroot.sh"
        echo "  6. Click Next -> Generate ISO!"
        ;;

    2)
        echo -e "${CYAN}[Step 2/5]${NC} Creating self-contained overlay tarball for deployment..."
        BUNDLE_TAR="$BUILD_DIR/luca-os-overlay-v1.0.tar.gz"
        tar -czf "$BUNDLE_TAR" -C "$ROOT_DIR" overlay scripts/bin apps assets
        echo -e "${GREEN}✓ Created bundle: $BUNDLE_TAR${NC}"
        ;;

    3)
        echo "See documentation in docs/getting-started.md"
        ;;
esac

echo ""
echo -e "${GREEN}Build pipeline ready.${NC}"
