#!/usr/bin/env python3
"""
Luca OS Asset Generator (Pure Python - No External Dependencies)
Generates high-definition SVGs and renders valid PNGs for:
- Desktop Wallpaper (1920x1080)
- Plymouth Boot Splash Logo (256x256 RGBA)
- GRUB Bootloader Background (1920x1080 RGB)
- App Icons (48x48, 128x128 RGBA)
"""

import os
import math
import struct
import zlib
import shutil

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def write_png(filepath, width, height, pixel_data, is_rgba=True):
    """
    Writes an uncompressed/zlib-compressed PNG file directly from raw bytes.
    pixel_data is a flat list/bytes of RGBA or RGB bytes.
    """
    bpp = 4 if is_rgba else 3
    color_type = 6 if is_rgba else 2

    # PNG Signature
    png_bytes = bytearray(b"\x89PNG\r\n\x1a\n")

    # IHDR Chunk
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, color_type, 0, 0, 0)
    ihdr_crc = zlib.crc32(b"IHDR" + ihdr_data)
    png_bytes += struct.pack(">I", len(ihdr_data)) + b"IHDR" + ihdr_data + struct.pack(">I", ihdr_crc)

    # Scanlines with filter byte 0x00
    raw_scanlines = bytearray()
    row_bytes_len = width * bpp
    for y in range(height):
        raw_scanlines.append(0) # Filter byte 0 (None)
        start = y * row_bytes_len
        raw_scanlines.extend(pixel_data[start : start + row_bytes_len])

    # IDAT Chunk (zlib compressed)
    compressed_data = zlib.compress(bytes(raw_scanlines), level=6)
    idat_crc = zlib.crc32(b"IDAT" + compressed_data)
    png_bytes += struct.pack(">I", len(compressed_data)) + b"IDAT" + compressed_data + struct.pack(">I", idat_crc)

    # IEND Chunk
    iend_crc = zlib.crc32(b"IEND")
    png_bytes += struct.pack(">I", 0) + b"IEND" + struct.pack(">I", iend_crc)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(png_bytes)
    print(f"Generated PNG: {filepath} ({width}x{height})")


def generate_logo_rgba(size=256):
    """
    Generates a 256x256 glowing futuristic 'L' logo on transparent background.
    Colors: Electric Cyan (#00E5FF) to Neon Purple (#7C4DFF).
    """
    pixels = bytearray(size * size * 4)
    cx, cy = size / 2.0, size / 2.0
    r_outer = size * 0.44
    r_inner = size * 0.36

    for y in range(size):
        for x in range(size):
            idx = (y * size + x) * 4
            dx = x - cx
            dy = y - cy
            dist = math.sqrt(dx * dx + dy * dy)

            # Gradient calculation
            t = (x + y) / (2.0 * size)
            cr = int(0x00 * (1.0 - t) + 0x7C * t)
            cg = int(0xE5 * (1.0 - t) + 0x4D * t)
            cb = int(0xFF)

            alpha = 0

            # Ring glow
            if r_inner - 2 <= dist <= r_outer + 2:
                # Anti-aliased ring edge
                edge_dist = abs(dist - (r_inner + r_outer) / 2.0)
                ring_thickness = (r_outer - r_inner) / 2.0
                intensity = max(0.0, 1.0 - (edge_dist / ring_thickness))
                alpha = int(240 * intensity)

            # Modern geometric 'L' inside the ring
            # Vertical bar of L: x in [80, 110], y in [75, 175]
            # Horizontal bar of L: x in [80, 175], y in [145, 175]
            # Stylized cut: rounded corner / modern slash
            is_vert = (78 <= x <= 108 and 75 <= y <= 175)
            is_horiz = (78 <= x <= 175 and 145 <= y <= 175)
            is_notch = (150 <= x <= 180 and 125 <= y <= 145 and (x - y) > 10)

            # Robot android dots (eyes/nodes)
            dist_node1 = math.sqrt((x - 145)**2 + (y - 95)**2)
            dist_node2 = math.sqrt((x - 145)**2 + (y - 125)**2)

            if is_vert or is_horiz or dist_node1 <= 9 or dist_node2 <= 7:
                cr = min(255, cr + 40)
                cg = min(255, cg + 20)
                alpha = 255
            elif is_notch:
                alpha = 200

            # Ambient soft outer glow
            if alpha == 0 and dist < size * 0.48:
                glow = max(0.0, 1.0 - (dist / (size * 0.48)))
                alpha = int(45 * (glow ** 2))
                cr, cg, cb = 0, 200, 255

            pixels[idx] = cr
            pixels[idx + 1] = cg
            pixels[idx + 2] = cb
            pixels[idx + 3] = alpha

    return pixels


def generate_wallpaper_rgb(width=1920, height=1080):
    """
    Renders high quality 1920x1080 wallpaper.
    Deep slate / midnight cyberpunk aesthetic with gradient orbs and cybernetic lattice.
    """
    pixels = bytearray(width * height * 3)
    cx, cy = width / 2.0, height / 2.0

    for y in range(height):
        # Vertical subtle gradient: #080B12 to #0F172A
        vy = y / float(height)
        base_r = int(8 + (15 - 8) * vy)
        base_g = int(11 + (23 - 11) * vy)
        base_b = int(18 + (42 - 18) * vy)

        for x in range(width):
            idx = (y * width + x) * 3
            vx = x / float(width)

            # Left cyan ambient light orb at (0.28 * width, 0.45 * height)
            dx1 = x - (0.30 * width)
            dy1 = y - (0.42 * height)
            d1 = math.sqrt(dx1 * dx1 + dy1 * dy1) / (0.45 * height)
            glow1 = math.exp(-2.2 * d1 * d1)

            # Right indigo/purple light orb at (0.72 * width, 0.58 * height)
            dx2 = x - (0.70 * width)
            dy2 = y - (0.58 * height)
            d2 = math.sqrt(dx2 * dx2 + dy2 * dy2) / (0.48 * height)
            glow2 = math.exp(-2.5 * d2 * d2)

            # Center emblem halo
            dc = math.sqrt((x - cx)**2 + (y - cy)**2) / (0.25 * height)
            glow_c = math.exp(-4.0 * dc * dc)

            # Grid line accent (subtle dark grid)
            grid = 0
            if (x % 64 == 0 or y % 64 == 0) and 0.15 < vx < 0.85 and 0.15 < vy < 0.85:
                grid = 8

            r = min(255, int(base_r + glow1 * 10 + glow2 * 68 + glow_c * 25 + grid))
            g = min(255, int(base_g + glow1 * 85 + glow2 * 20 + glow_c * 65 + grid))
            b = min(255, int(base_b + glow1 * 130 + glow2 * 120 + glow_c * 110 + grid))

            pixels[idx] = r
            pixels[idx + 1] = g
            pixels[idx + 2] = b

    return pixels


def generate_grub_rgb(width=1920, height=1080):
    """
    Renders bootloader background: dark tech theme with frame guide for GRUB menu.
    """
    pixels = bytearray(width * height * 3)
    cx, cy = width / 2.0, height / 2.0

    for y in range(height):
        vy = y / float(height)
        # Deep dark vignette
        base_r = int(5 + 10 * math.sin(vy * math.pi))
        base_g = int(7 + 12 * math.sin(vy * math.pi))
        base_b = int(12 + 20 * math.sin(vy * math.pi))

        for x in range(width):
            idx = (y * width + x) * 3
            vx = x / float(width)

            # Menu boundary guide glow (box centered around middle)
            # Center menu box is roughly x in [480, 1440], y in [300, 780]
            in_box_x = (0.24 * width <= x <= 0.76 * width)
            in_box_y = (0.26 * height <= y <= 0.74 * height)

            accent = 0
            # Border highlight
            if (abs(x - 0.24 * width) < 2 or abs(x - 0.76 * width) < 2) and in_box_y:
                accent = 90
            elif (abs(y - 0.26 * height) < 2 or abs(y - 0.74 * height) < 2) and in_box_x:
                accent = 90

            # Header glow at top
            top_glow = max(0.0, 1.0 - (y / 180.0)) * 40

            r = min(255, int(base_r + accent * 0.2 + top_glow * 0.2))
            g = min(255, int(base_g + accent * 0.7 + top_glow * 0.6))
            b = min(255, int(base_b + accent * 1.0 + top_glow * 0.9))

            pixels[idx] = r
            pixels[idx + 1] = g
            pixels[idx + 2] = b

    return pixels


def write_svg_files():
    """Generates clean, scalable SVG vector assets."""
    # 1. Luca Logo SVG
    logo_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <linearGradient id="cyberGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F2FE" />
      <stop offset="50%" stop-color="#4FACFE" />
      <stop offset="100%" stop-color="#7F00FF" />
    </linearGradient>
    <linearGradient id="ringGrad" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00F2FE" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#7F00FF" stop-opacity="0.3" />
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="12" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Ambient Outer Glow -->
  <circle cx="256" cy="256" r="210" fill="none" stroke="url(#ringGrad)" stroke-width="4" opacity="0.6" />
  <circle cx="256" cy="256" r="190" fill="#0A0E17" stroke="url(#cyberGrad)" stroke-width="10" filter="url(#glow)" />

  <!-- Futuristic Orbit Accents -->
  <circle cx="256" cy="66" r="8" fill="#00F2FE" />
  <circle cx="446" cy="256" r="6" fill="#7F00FF" />
  <circle cx="256" cy="446" r="8" fill="#4FACFE" />

  <!-- Stylized Monogram 'L' + Android Circuit Elements -->
  <g filter="url(#glow)">
    <!-- Vertical Spine -->
    <path d="M 170 140 C 170 128 180 120 192 120 L 220 120 C 232 120 242 128 242 140 L 242 310 L 330 310 C 342 310 352 320 352 332 L 352 352 C 352 364 342 374 330 374 L 192 374 C 180 374 170 364 170 352 Z"
          fill="url(#cyberGrad)" />
    <!-- Android Eye / Quantum Core -->
    <circle cx="310" cy="180" r="22" fill="#00F2FE" />
    <circle cx="310" cy="180" r="10" fill="#FFFFFF" />
    <!-- Interconnect Line -->
    <line x1="242" y1="210" x2="310" y2="210" stroke="#00F2FE" stroke-width="6" stroke-dasharray="6,4" />
    <circle cx="310" cy="245" r="14" fill="#7F00FF" />
  </g>
</svg>"""

    # 2. Wallpaper SVG
    wallpaper_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <defs>
    <radialGradient id="bgGlow1" cx="30%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#0052D4" stop-opacity="0.35" />
      <stop offset="50%" stop-color="#4364F7" stop-opacity="0.10" />
      <stop offset="100%" stop-color="#070A10" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="bgGlow2" cx="75%" cy="60%" r="55%">
      <stop offset="0%" stop-color="#7F00FF" stop-opacity="0.30" />
      <stop offset="60%" stop-color="#6B11FF" stop-opacity="0.05" />
      <stop offset="100%" stop-color="#070A10" stop-opacity="0" />
    </radialGradient>
    <linearGradient id="neonCyan" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F2FE" />
      <stop offset="100%" stop-color="#4FACFE" />
    </linearGradient>
  </defs>

  <!-- Deep Background -->
  <rect width="1920" height="1080" fill="#070A10" />
  <rect width="1920" height="1080" fill="url(#bgGlow1)" />
  <rect width="1920" height="1080" fill="url(#bgGlow2)" />

  <!-- Subtle Horizon Curves -->
  <path d="M 0 850 Q 480 750, 960 820 T 1920 780 L 1920 1080 L 0 1080 Z" fill="#0B101D" opacity="0.8" />
  <path d="M 0 920 Q 560 860, 1120 900 T 1920 870 L 1920 1080 L 0 1080 Z" fill="#0F172A" opacity="0.9" />

  <!-- Center Watermark Logo & Text -->
  <g transform="translate(960, 480)" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Ubuntu, sans-serif">
    <!-- Emblem -->
    <circle cx="0" cy="-40" r="70" fill="#0E1626" stroke="url(#neonCyan)" stroke-width="4" />
    <text x="0" y="-18" font-size="64" font-weight="900" fill="#00F2FE" letter-spacing="4">L</text>
    <circle cx="28" cy="-55" r="8" fill="#7F00FF" />

    <!-- Typography -->
    <text x="0" y="80" font-size="38" font-weight="800" fill="#FFFFFF" letter-spacing="12">LUCA OS</text>
    <text x="0" y="115" font-size="14" font-weight="500" fill="#64748B" letter-spacing="4">DESKTOP LINUX  •  NATIVE ANDROID SUBSYSTEM</text>
  </g>
</svg>"""

    # 3. GRUB Background SVG
    grub_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <defs>
    <linearGradient id="grubGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#080C14" />
      <stop offset="50%" stop-color="#0D1322" />
      <stop offset="100%" stop-color="#05080E" />
    </linearGradient>
    <linearGradient id="neonLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00F2FE" stop-opacity="0" />
      <stop offset="50%" stop-color="#00F2FE" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#7F00FF" stop-opacity="0" />
    </linearGradient>
  </defs>

  <rect width="1920" height="1080" fill="url(#grubGrad)" />
  <rect x="0" y="0" width="1920" height="4" fill="url(#neonLine)" />
  <rect x="0" y="1076" width="1920" height="4" fill="url(#neonLine)" />

  <!-- Menu Box Area Frame -->
  <rect x="440" y="260" width="1040" height="520" rx="16" fill="#0B111D" fill-opacity="0.65" stroke="#1E293B" stroke-width="2" />

  <!-- Top Branding Header -->
  <g transform="translate(960, 180)" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">
    <text x="0" y="0" font-size="34" font-weight="800" fill="#FFFFFF" letter-spacing="8">LUCA OS BOOT MANAGER</text>
    <text x="0" y="32" font-size="14" font-weight="500" fill="#00E5FF" letter-spacing="3">SECURE UEFI / BIOS FAST BOOT</text>
  </g>
</svg>"""

    files = {
        os.path.join(BASE_DIR, "assets", "branding", "luca-logo.svg"): logo_svg,
        os.path.join(BASE_DIR, "assets", "wallpapers", "luca-wallpaper.svg"): wallpaper_svg,
        os.path.join(BASE_DIR, "assets", "grub", "luca-grub-bg.svg"): grub_svg,
    }

    for path, content in files.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generated SVG: {path}")


def main():
    print("=" * 60)
    print("   Luca OS Visual Assets & Themes Build Generator")
    print("=" * 60)

    # 1. Generate SVGs
    write_svg_files()

    # 2. Generate 256x256 Logo PNG (for Plymouth, Icons, UI)
    print("\n[1/3] Rendering Plymouth / System Logo (256x256 RGBA)...")
    logo_data = generate_logo_rgba(256)
    logo_png_path = os.path.join(BASE_DIR, "assets", "branding", "luca-logo.png")
    write_png(logo_png_path, 256, 256, logo_data, is_rgba=True)

    # Copy to Plymouth theme and overlay
    plymouth_logo = os.path.join(BASE_DIR, "overlay", "usr", "share", "plymouth", "themes", "luca-os", "logo.png")
    shutil.copyfile(logo_png_path, plymouth_logo)
    print(f"Copied logo to: {plymouth_logo}")

    # Copy to icons directory
    app_icon = os.path.join(BASE_DIR, "assets", "icons", "luca-os.png")
    shutil.copyfile(logo_png_path, app_icon)
    print(f"Copied icon to: {app_icon}")

    # 3. Generate Wallpaper PNG (1920x1080 RGB)
    print("\n[2/3] Rendering Desktop Wallpaper (1920x1080 RGB)...")
    wallpaper_data = generate_wallpaper_rgb(1920, 1080)
    wallpaper_png_path = os.path.join(BASE_DIR, "assets", "wallpapers", "luca-wallpaper.png")
    write_png(wallpaper_png_path, 1920, 1080, wallpaper_data, is_rgba=False)

    overlay_wallpaper = os.path.join(BASE_DIR, "overlay", "usr", "share", "backgrounds", "luca-wallpaper.png")
    shutil.copyfile(wallpaper_png_path, overlay_wallpaper)
    print(f"Copied wallpaper to: {overlay_wallpaper}")

    # 4. Generate GRUB Background PNG (1920x1080 RGB)
    print("\n[3/3] Rendering GRUB Bootloader Background (1920x1080 RGB)...")
    grub_data = generate_grub_rgb(1920, 1080)
    grub_png_path = os.path.join(BASE_DIR, "assets", "grub", "luca-grub-bg.png")
    write_png(grub_png_path, 1920, 1080, grub_data, is_rgba=False)

    overlay_grub = os.path.join(BASE_DIR, "overlay", "boot", "grub", "themes", "luca-os", "background.png")
    shutil.copyfile(grub_png_path, overlay_grub)
    print(f"Copied GRUB background to: {overlay_grub}")

    print("\nAll Luca OS branding and artwork assets generated successfully!")

if __name__ == "__main__":
    main()
