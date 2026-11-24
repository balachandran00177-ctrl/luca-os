#!/usr/bin/env bash
# ==============================================================================
# Luca OS — Safe USB Pendrive Flasher (scripts/build/flash-usb.sh)
# Safe, interactive tool to flash Luca OS to a USB flash drive with
# partition protection to prevent accidental overwriting of system drives.
# ==============================================================================

set -euo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

BUILD_DIR="${BUILD_DIR:-$HOME/luca-os-build}"
ISO_PATH="${1:-$BUILD_DIR/luca-os-1.0-amd64.iso}"

echo -e "${CYAN}======================================================================${NC}"
echo -e "${CYAN}             ⚡ Luca OS — Safe USB Pendrive Flasher                    ${NC}"
echo -e "${CYAN}======================================================================${NC}"

if [ ! -f "$ISO_PATH" ]; then
    echo -e "${RED}[Error]${NC} ISO file not found: $ISO_PATH"
    echo "Usage: sudo bash scripts/build/flash-usb.sh [path-to-iso]"
    exit 1
fi

if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[Error]${NC} This script must be run as root (or with sudo) to write to raw disks."
    exit 1
fi

echo -e "Selected ISO: ${CYAN}$ISO_PATH${NC} ($(du -h "$ISO_PATH" | cut -f1))"
echo ""
echo "Scanning for removable USB drives..."
echo "----------------------------------------------------------------------"

# Detect USB storage devices only (exclude internal nvme, sata, mmc)
USB_DEVICES=$(lsblk -d -p -n -l -o NAME,SIZE,MODEL,TRAN 2>/dev/null | grep -i "usb" || true)

if [ -z "$USB_DEVICES" ]; then
    echo -e "${YELLOW}No removable USB storage devices detected.${NC}"
    echo "Please plug in a USB pendrive (8 GB or larger) and run this script again."
    exit 1
fi

echo "$USB_DEVICES"
echo "----------------------------------------------------------------------"
echo ""

read -rp "Enter target disk path (e.g., /dev/sdb - DO NOT enter partitions like /dev/sdb1): " TARGET_DISK

# Validate target disk exists
if [ ! -b "$TARGET_DISK" ]; then
    echo -e "${RED}[Error]${NC} Device '$TARGET_DISK' does not exist or is not a block device."
    exit 1
fi

# Safety check: Prevent writing to nvme0n1 or sda if it is root mount
ROOT_DEV=$(findmnt -n -o SOURCE / | sed -E 's/p?[0-9]+$//')
if [ "$TARGET_DISK" = "$ROOT_DEV" ]; then
    echo -e "${RED}[FATAL ERROR]${NC} Target device '$TARGET_DISK' contains your active ROOT '/' filesystem!"
    echo "Aborting to prevent system destruction."
    exit 1
fi

echo ""
echo -e "${RED}!!!!!!!!!!!!!!!!!!!!!!!! WARNING !!!!!!!!!!!!!!!!!!!!!!!!${NC}"
echo -e "ALL DATA ON ${YELLOW}$TARGET_DISK${NC} WILL BE COMPLETELY ERASED."
echo -e "${RED}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!${NC}"
echo ""
read -rp "Are you absolutely sure you want to write Luca OS to $TARGET_DISK? [type YES to proceed]: " CONFIRM

if [ "$CONFIRM" != "YES" ]; then
    echo "Operation cancelled by user."
    exit 0
fi

# Unmount any automounted partitions on the target disk
echo "Unmounting existing partitions on $TARGET_DISK..."
umount "${TARGET_DISK}"* 2>/dev/null || true

echo "Flashing Luca OS ISO to $TARGET_DISK..."
dd if="$ISO_PATH" of="$TARGET_DISK" bs=4M status=progress oflag=sync conv=fsync

echo ""
echo -e "${GREEN}======================================================================${NC}"
echo -e "${GREEN}  ✓ Luca OS successfully flashed to $TARGET_DISK!                     ${NC}"
echo -e "${GREEN}======================================================================${NC}"
echo "You can now safely unplug your USB drive and boot from it on any PC/laptop."
echo ""
