# Luca OS System Architecture

Luca OS combines the rock-solid hardware support of enterprise Linux with the versatility of an unprivileged Android container runtime.

---

## Architecture Stack

```text
+-------------------------------------------------------------------------+
|                       DESKTOP ENVIRONMENT (GNOME 46+)                   |
|   Mutter Wayland Compositor • Dash-to-Dock • Quick Settings • GTK4      |
+------------------------------------+------------------------------------+
|         HOST LINUX APPS            |          WAYDROID APPS             |
|   Terminal, Firefox, VS Code,      |   Android Framework (AOSP 11/13),  |
|   LibreOffice, Steam, Flatpaks     |   Google Play, Mobile Games        |
+------------------------------------+------------------------------------+
|                 WAYLAND CLIENT GRAPHICS PROTOCOL                        |
|             (wl_surface, xdg_toplevel, linux_dmabuf)                    |
+-------------------------------------------------------------------------+
|                  HOST LINUX KERNEL WITH BINDER IPC                      |
|         binder_linux • ashmem • namespaces • cgroups • LXC              |
+-------------------------------------------------------------------------+
|                        PC HARDWARE PLATFORM                             |
|          x86_64 CPU • DRM/KMS GPU Drivers • Wi-Fi • Audio               |
+-------------------------------------------------------------------------+
```

---

## Key Subsystems

### 1. Mutter Wayland Compositor
Luca OS operates exclusively on Wayland. Wayland provides per-window buffer management, tear-free rendering, fractional display scaling for 4K laptop screens, and secure application sandboxing.

### 2. LXC Container & Namespaces
The Android subsystem is contained within an unprivileged Linux container (LXC). Android runs its own user space (init, zygote, surfaceflinger, system_server) without interfering with the host system libraries (`glibc`, `systemd`).

### 3. Binder & Ashmem Kernel Drivers
Inter-process communication between Android services uses the Linux kernel's in-tree `binder_linux` module. Shared memory allocations use `ashmem` or `memfd`, enabling instantaneous data sharing with zero memory duplication.

### 4. Zero-Copy DMA-BUF Graphics
When an Android application renders a frame, SurfaceFlinger exports the graphical buffer as a Linux `DMA-BUF` file descriptor. Mutter (the desktop compositor) imports the buffer directly into the GPU pipeline. This enables 60–120 FPS windowed execution with virtually zero CPU overhead.

### 5. GSettings Schema Overrides
Luca OS applies configuration overrides via `/usr/share/glib-2.0/schemas/99_luca-os.gschema.override`. When a user logs in, default dark mode, bottom dock alignment, touchpad gestures, and custom wallpapers are applied automatically without modifying user dotfiles.
