#!/usr/bin/env bash
# ==============================================================================
# Luca OS — QEMU Virtual Machine Test Runner (scripts/build/test-qemu.sh)
# Rapidly tests the generated Luca OS ISO in both UEFI and BIOS modes.
# ==============================================================================

set -euo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

BUILD_DIR="${BUILD_DIR:-$HOME/luca-os-build}"
ISO_PATH="${1:-$BUILD_DIR/luca-os-1.0-amd64.iso}"
RAM_SIZE="${RAM_SIZE:-4096}"
SMP_CORES="${SMP_CORES:-4}"
BOOT_MODE="${BOOT_MODE:-uefi}"

echo -e "${CYAN}======================================================================${NC}"
echo -e "${CYAN}              ⚡ Luca OS — QEMU ISO Test Runner                       ${NC}"
echo -e "${CYAN}======================================================================${NC}"

if [ ! -f "$ISO_PATH" ]; then
    echo -e "${RED}[Error]${NC} Target ISO file not found: $ISO_PATH"
    echo "Please provide the path to your ISO: bash scripts/build/test-qemu.sh /path/to/luca-os.iso"
    exit 1
fi

echo "Testing ISO: $ISO_PATH"
echo "Allocated RAM: ${RAM_SIZE} MB"
echo "Allocated CPU Cores: $SMP_CORES"
echo "Boot Mode: $BOOT_MODE"

# Check KVM acceleration
KVM_FLAGS=""
if [ -e "/dev/kvm" ] && [ -r "/dev/kvm" ] && [ -w "/dev/kvm" ]; then
    echo -e "${GREEN}✓ Hardware KVM acceleration enabled.${NC}"
    KVM_FLAGS="-enable-kvm -cpu host"
else
    echo -e "${YELLOW}⚠ Running without KVM acceleration (slower emulation).${NC}"
    KVM_FLAGS="-cpu qemu64"
fi

# Detect UEFI firmware path
OVMF_PATH=""
for p in /usr/share/OVMF/OVMF_CODE.fd /usr/share/ovmf/OVMF.fd /usr/share/edk2/ovmf/OVMF_CODE.fd; do
    if [ -f "$p" ]; then
        OVMF_PATH="$p"
        break
    fi
done

QEMU_CMD=(
    qemu-system-x86_64
    $KVM_FLAGS
    -m "$RAM_SIZE"
    -smp "$SMP_CORES"
    -cdrom "$ISO_PATH"
    -boot d
    -vga virtio
    -display default,gl=on
    -device intel-hda
    -device hda-duplex
    -net nic,model=virtio
    -net user
)

if [ "$BOOT_MODE" = "uefi" ]; then
    if [ -n "$OVMF_PATH" ]; then
        echo -e "Using UEFI firmware: $OVMF_PATH"
        QEMU_CMD+=(-bios "$OVMF_PATH")
    else
        echo -e "${YELLOW}Warning: OVMF UEFI firmware not found. Falling back to BIOS mode.${NC}"
    fi
fi

echo ""
echo "Launching QEMU VM..."
"${QEMU_CMD[@]}"
