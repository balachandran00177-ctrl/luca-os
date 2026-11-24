# Contributing to Luca OS

Thank you for your interest in contributing to **Luca OS**! We are committed to building an open, user-friendly, high-performance operating system that bridges desktop Linux with the Android application ecosystem.

---

## Code of Conduct
All participants are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please treat all contributors with kindness, empathy, and respect.

---

## How Can You Help?

1. **Hardware Testing & Reports:** Test Luca OS on various laptops, convertibles, tablets, and desktops (Intel, AMD, NVIDIA, Apple Silicon x86 VMs).
2. **Developing Core Applications:** Enhance `luca-welcome`, `luca-installer`, or `luca-control` (Python, GTK4, Tkinter).
3. **Android Compatibility & Translation:** Help benchmark and optimize `libhoudini`, `libndk`, and Waydroid multi-window protocols.
4. **Themes & Artwork:** Contribute high-resolution wallpapers, icon designs, and Plymouth boot splash animations.
5. **Documentation & Localization:** Translate the Welcome app and documentation into other languages.

---

## Development Workflow

### 1. Fork & Clone
```bash
git clone https://github.com/your-username/luca-os.git
cd luca-os
```

### 2. Test Local Utilities
```bash
make test-gui
```

### 3. Making Changes
- Create a feature branch: `git checkout -b feature/awesome-addition`
- Ensure shell scripts follow `set -euo pipefail` standards.
- Run `make assets` if updating vector graphics.

### 4. Submitting a Pull Request
- Provide a clear description of the problem solved.
- Attach screenshots for any visual UI changes.
- Ensure all CI tests pass.
