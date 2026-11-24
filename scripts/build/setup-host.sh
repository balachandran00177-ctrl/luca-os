#!/usr/bin/env bash
# ==============================================================================
# Luca OS — Host Environment Setup Script (scripts/build/setup-host.sh)
# Prepares host Ubuntu / Debian system for building and testing Luca OS ISOs.
# ==============================================================================

set -euo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}======================================================================${NC}"
echo -e "${CYAN}          ⚡ Luca OS — Host Builder & Testing Environment Setup        ${NC}"
echo -e "${CYAN}======================================================================${NC}"

# Check sudo
if [ "$EUID" -ne 0 ]; then
    SUDO="sudo"
else
    SUDO=""
fi

echo -e "${CYAN}[1/4]${NC} Updating host package repositories..."
$SUDO apt-get update

echo -e "${CYAN}[2/4]${NC} Installing ISO authoring and image manipulation tools..."
$SUDO apt-get install -y --no-install-recommends \
    software-properties-common \
    curl \
    ca-certificates \
    wget \
    git \
    python3 \
    python3-pip \
    xorriso \
    squashfs-tools \
    mtools \
    dosfstools \
    isolinux \
    syslinux-utils

echo -e "${CYAN}[3/4]${NC} Adding Cubic (Custom Ubuntu ISO Creator) PPA..."
# Add universe repository
$SUDO add-apt-repository -y universe
# Add Cubic Wizard official PPA
$SUDO add-apt-repository -y ppa:cubic-wizard/release
$SUDO apt-get update
$SUDO apt-get install -y --no-install-recommends cubic

echo -e "${CYAN}[4/4]${NC} Installing QEMU & OVMF UEFI emulation for ISO testing..."
$SUDO apt-get install -y \
    qemu-system-x86 \
    ovmf \
    qemu-utils

# Check KVM hardware virtualization
echo ""
echo "Checking KVM hardware acceleration:"
if [ -e "/dev/kvm" ]; then
    echo -e "${GREEN}✓ KVM hardware acceleration is available (/dev/kvm exists).${NC}"
    if [ -n "${SUDO_USER:-}" ]; then
        $SUDO usermod -aG kvm "$SUDO_USER" || true
        echo "Added user $SUDO_USER to 'kvm' group."
    fi
else
    echo -e "${YELLOW}⚠ /dev/kvm not found.${NC} ISO testing will run in software emulation mode."
    echo "  (Enable Intel VT-x or AMD-V in BIOS if running on bare metal)."
fi

echo ""
echo -e "${GREEN}======================================================================${NC}"
echo -e "${GREEN}  ✓ Host environment successfully configured for Luca OS!            ${NC}"
echo -e "${GREEN}======================================================================${NC}"
echo ""
echo "Next step: Run 'bash scripts/build/build-iso.sh' to start the build."
echo ""
