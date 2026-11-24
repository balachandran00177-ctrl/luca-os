# GPU Acceleration & Hardware Graphics Guide

Hardware GPU acceleration is essential for 60+ FPS window rendering, fluid animations, and smooth 3D gaming in Luca OS.

---

## 1. Supported GPU Architectures

| Hardware | Status | Driver Backend | Notes |
|---|---|---|---|
| **Intel HD / UHD / Iris / Arc** | ⭐ Optimal | Mesa (Iris / ANV) | Native zero-copy DMA-BUF; works out of the box. |
| **AMD Radeon (Vega / RDNA / RDNA2 / RDNA3)** | ⭐ Optimal | Mesa (RadeonSI / RADV) | Native high-performance Vulkan/OpenGL acceleration. |
| **NVIDIA Hybrid Laptop (Optimus)** | ✔ Supported | Intel/AMD iGPU passthrough | Route Waydroid display through integrated GPU for stability. |
| **NVIDIA Dedicated Desktop** | ✔ Supported | SwiftShader / EGL GBM | Requires Wayland-compatible proprietary driver (555+). |

---

## 2. Using `luca-gpu-config`

Luca OS includes an intelligent graphics manager to configure the Waydroid container:

### Auto Mode (Default)
Let Luca OS detect the best hardware renderer automatically:
```bash
luca-gpu-config auto
```

### Integrated GPU Mode (Recommended for NVIDIA Laptops)
On hybrid laptops equipped with both Intel/AMD graphics and an NVIDIA GeForce card, route Android rendering through the power-efficient integrated GPU to eliminate black screens:
```bash
luca-gpu-config igpu
```

### Software Fallback Mode (SwiftShader)
If you encounter graphics corruption or a frozen container on experimental GPU configurations, enable Google SwiftShader CPU software rendering:
```bash
luca-gpu-config software
```

### Check Active Graphics Status
```bash
luca-gpu-config status
```

---

## 3. Resolving Black Screens on NVIDIA Hardware

If Waydroid opens with a blank or black window:
1. Ensure your desktop is running on **Wayland** (log out and verify the gear icon in the login screen).
2. Force integrated graphics mode:
   ```bash
   luca-gpu-config igpu
   ```
3. Disable height padding override in `/var/lib/waydroid/waydroid_base.prop`:
   ```bash
   waydroid prop set persist.waydroid.height_padding 0
   ```
4. Restart the container:
   ```bash
   waydroid session stop
   sudo systemctl restart waydroid-container
   ```
