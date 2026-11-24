# ==============================================================================
# Luca OS — Developer & Automation Makefile
# ==============================================================================

.PHONY: help assets test test-gui iso qemu-uefi qemu-bios live-creator store clean

help:
	@echo "Luca OS Developer Commands:"
	@echo "  make assets        - Regenerate SVGs, wallpapers, Plymouth logo, and GRUB art"
	@echo "  make test-gui      - Test Welcome, Installer, Control Center, Live Creator, Store, and Live Hub"
	@echo "  make live-creator  - Launch Live USB Pendrive Creator tool"
	@echo "  make store         - Launch unified Luca App Store"
	@echo "  make host-setup    - Install Cubic, QEMU, KVM, and build tools on host"
	@echo "  make iso           - Prepare workspace and trigger ISO build"
	@echo "  make qemu-uefi     - Launch latest ISO in QEMU (UEFI mode)"
	@echo "  make qemu-bios     - Launch latest ISO in QEMU (BIOS mode)"
	@echo "  make flash         - Interactively flash ISO to USB pendrive"

assets:
	python3 scripts/build/generate-assets.py

test-gui:
	python3 apps/luca-welcome/luca_welcome.py --test
	python3 apps/luca-installer/luca_installer.py --test
	python3 apps/luca-control/luca_control.py --test
	python3 apps/luca-live-creator/luca_live_creator.py --test
	python3 apps/luca-store/luca_store.py --test
	python3 apps/luca-live-hub/luca_live_hub.py --test
	@echo "All Luca OS GUI applications passed verification tests!"

live-creator:
	python3 apps/luca-live-creator/luca_live_creator.py

store:
	python3 apps/luca-store/luca_store.py

host-setup:
	bash scripts/build/setup-host.sh

iso:
	bash scripts/build/build-iso.sh

qemu-uefi:
	BOOT_MODE=uefi bash scripts/build/test-qemu.sh

qemu-bios:
	BOOT_MODE=bios bash scripts/build/test-qemu.sh

flash:
	sudo bash scripts/build/flash-usb.sh

clean:
	rm -rf build/staging
	@echo "Cleaned build staging files."
