#!/usr/bin/env python3
"""
Luca OS — Welcome & Onboarding Wizard
A user-friendly desktop application for onboarding, hardware overview,
Android subsystem configuration, essential app installation, and personalization.
"""

import sys
import os
import subprocess
import shutil
import platform
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

VERSION = "1.0.0"
CONFIG_DIR = os.path.expanduser("~/.config/luca-os")
AUTOSTART_FILE = os.path.expanduser("~/.config/autostart/luca-welcome.desktop")

# Modern Cyber Dark Theme Palette
COLORS = {
    "bg": "#0B101D",
    "card_bg": "#131C31",
    "card_border": "#1E2C4B",
    "sidebar": "#080C17",
    "accent_cyan": "#00F2FE",
    "accent_blue": "#3B82F6",
    "accent_purple": "#8B5CF6",
    "accent_green": "#10B981",
    "accent_red": "#EF4444",
    "text_primary": "#F8FAFC",
    "text_secondary": "#94A3B8",
    "text_muted": "#64748B",
    "button_bg": "#1E293B",
    "button_hover": "#2D3E5E",
}

class LucaWelcomeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Welcome to Luca OS")
        self.geometry("980x640")
        self.minsize(860, 540)
        self.configure(bg=COLORS["bg"])

        # Try to set window icon
        icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "branding", "luca-logo.png")
        if os.path.exists(icon_path):
            try:
                self.iconphoto(False, tk.PhotoImage(file=icon_path))
            except Exception:
                pass

        self.active_tab = "overview"
        self._init_layout()
        self._detect_system_specs()

    def _init_layout(self):
        # Master Container
        self.container = tk.Frame(self, bg=COLORS["bg"])
        self.container.pack(fill="both", expand=True)

        # 1. Left Sidebar Navigation
        self.sidebar = tk.Frame(self.container, bg=COLORS["sidebar"], width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Sidebar Header Branding
        brand_frame = tk.Frame(self.sidebar, bg=COLORS["sidebar"], pady=24, padx=16)
        brand_frame.pack(fill="x")

        brand_logo = tk.Label(
            brand_frame,
            text="⚡ LUCA OS",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 17, "bold"),
            fg=COLORS["accent_cyan"],
            bg=COLORS["sidebar"]
        )
        brand_logo.pack(anchor="w")

        brand_subtitle = tk.Label(
            brand_frame,
            text="Desktop + Android Hybrid",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9),
            fg=COLORS["text_muted"],
            bg=COLORS["sidebar"]
        )
        brand_subtitle.pack(anchor="w", pady=(2, 0))

        # Separator line
        sep = tk.Frame(self.sidebar, bg=COLORS["card_border"], height=1)
        sep.pack(fill="x", padx=16, pady=8)

        # Navigation Buttons
        self.nav_buttons = {}
        nav_items = [
            ("overview", "🏠  Overview", self._show_overview),
            ("android", "🤖  Android Subsystem", self._show_android),
            ("apps", "📦  Essential Apps", self._show_apps),
            ("desktop", "🎨  Personalization", self._show_desktop),
            ("diagnostics", "🔍  System Info & GPU", self._show_diagnostics),
            ("community", "🌐  Help & Community", self._show_community),
        ]

        for key, label, cmd in nav_items:
            btn = tk.Button(
                self.sidebar,
                text=label,
                font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 11),
                fg=COLORS["text_secondary"],
                bg=COLORS["sidebar"],
                activebackground=COLORS["card_bg"],
                activeforeground=COLORS["accent_cyan"],
                bd=0,
                padx=16,
                pady=10,
                anchor="w",
                cursor="hand2",
                command=lambda k=key, c=cmd: self._nav_click(k, c)
            )
            btn.pack(fill="x", padx=8, pady=2)
            self.nav_buttons[key] = btn

        # Sidebar Footer
        sidebar_footer = tk.Frame(self.sidebar, bg=COLORS["sidebar"], pady=16, padx=16)
        sidebar_footer.pack(side="bottom", fill="x")

        self.autostart_var = tk.BooleanVar(value=True)
        chk = tk.Checkbutton(
            sidebar_footer,
            text="Launch on boot",
            variable=self.autostart_var,
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9),
            fg=COLORS["text_muted"],
            bg=COLORS["sidebar"],
            activebackground=COLORS["sidebar"],
            activeforeground=COLORS["text_secondary"],
            selectcolor=COLORS["card_bg"],
            command=self._toggle_autostart
        )
        chk.pack(anchor="w")

        # 2. Right Content Area
        self.content_area = tk.Frame(self.container, bg=COLORS["bg"], padx=32, pady=24)
        self.content_area.pack(side="right", fill="both", expand=True)

        self._show_overview()

    def _nav_click(self, key, cmd):
        self.active_tab = key
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(
                    bg=COLORS["card_bg"],
                    fg=COLORS["accent_cyan"],
                    font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 11, "bold")
                )
            else:
                btn.configure(
                    bg=COLORS["sidebar"],
                    fg=COLORS["text_secondary"],
                    font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 11)
                )
        cmd()

    def _clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def _detect_system_specs(self):
        self.specs = {
            "os": "Luca OS 1.0 (amd64)",
            "kernel": platform.release(),
            "cpu": platform.processor() or "x86_64 Processor",
            "wayland": bool(os.environ.get("WAYLAND_DISPLAY")),
            "waydroid_installed": shutil.which("waydroid") is not None,
        }

    # ==================== TAB: OVERVIEW ====================
    def _show_overview(self):
        self._clear_content()

        header = tk.Label(
            self.content_area,
            text="Welcome to your new Luca OS Desktop",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 20, "bold"),
            fg=COLORS["text_primary"],
            bg=COLORS["bg"]
        )
        header.pack(anchor="w")

        sub = tk.Label(
            self.content_area,
            text="The open-source operating system combining Linux desktop stability with native Android apps.",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 11),
            fg=COLORS["text_secondary"],
            bg=COLORS["bg"]
        )
        sub.pack(anchor="w", pady=(4, 20))

        # Feature Cards Grid
        cards_frame = tk.Frame(self.content_area, bg=COLORS["bg"])
        cards_frame.pack(fill="x", pady=10)

        self._create_card(
            cards_frame,
            title="📱 Android App Container",
            desc="Run millions of Android APKs and Google Play apps side-by-side with Linux desktop windows with full GPU speed.",
            btn_text="Configure Android →",
            btn_cmd=lambda: self._nav_click("android", self._show_android),
            side="left"
        )

        self._create_card(
            cards_frame,
            title="⚡ Linux Power & Freedom",
            desc="Full PC terminal, VS Code, Steam gaming, Flatpaks, and native hardware drivers for Wi-Fi, Bluetooth, and audio.",
            btn_text="Install Apps →",
            btn_cmd=lambda: self._nav_click("apps", self._show_apps),
            side="right"
        )

        # Quick Start Checklist Card
        checklist_card = tk.Frame(self.content_area, bg=COLORS["card_bg"], padx=20, pady=16, highlightbackground=COLORS["card_border"], highlightthickness=1)
        checklist_card.pack(fill="x", pady=20)

        cl_title = tk.Label(
            checklist_card,
            text="🚀 Recommended First Steps",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 13, "bold"),
            fg=COLORS["accent_cyan"],
            bg=COLORS["card_bg"]
        )
        cl_title.pack(anchor="w", pady=(0, 10))

        steps = [
            ("1. Initialize Android Subsystem", "Downloads official container with Google Play Store support.", "Run Setup", lambda: self._run_command("luca-android-setup")),
            ("2. Enable ARM Translation", "Run ARM64 mobile apps and games seamlessly on your Intel or AMD CPU.", "Enable ARM", lambda: self._run_command("luca-arm-enable")),
            ("3. Register Google Play ID", "Certify your device with Google to enable Play Store downloads.", "Get ID", lambda: self._run_command("luca-play-id")),
        ]

        for step_title, step_desc, b_text, b_action in steps:
            row = tk.Frame(checklist_card, bg=COLORS["card_bg"], pady=6)
            row.pack(fill="x")

            txt_box = tk.Frame(row, bg=COLORS["card_bg"])
            txt_box.pack(side="left", fill="x", expand=True)

            t1 = tk.Label(txt_box, text=step_title, font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 10, "bold"), fg=COLORS["text_primary"], bg=COLORS["card_bg"])
            t1.pack(anchor="w")
            t2 = tk.Label(txt_box, text=step_desc, font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9), fg=COLORS["text_secondary"], bg=COLORS["card_bg"])
            t2.pack(anchor="w")

            act_btn = tk.Button(
                row,
                text=b_text,
                font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9, "bold"),
                fg=COLORS["bg"],
                bg=COLORS["accent_cyan"],
                activebackground=COLORS["accent_blue"],
                activeforeground=COLORS["text_primary"],
                bd=0,
                padx=14,
                pady=5,
                cursor="hand2",
                command=b_action
            )
            act_btn.pack(side="right")

    # ==================== TAB: ANDROID SUBSYSTEM ====================
    def _show_android(self):
        self._clear_content()

        header = tk.Label(
            self.content_area,
            text="Android Subsystem Control",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 20, "bold"),
            fg=COLORS["text_primary"],
            bg=COLORS["bg"]
        )
        header.pack(anchor="w")

        sub = tk.Label(
            self.content_area,
            text="Manage your container, install APKs, and tune mobile performance.",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 11),
            fg=COLORS["text_secondary"],
            bg=COLORS["bg"]
        )
        sub.pack(anchor="w", pady=(4, 20))

        # Status & Action Panel
        status_box = tk.Frame(self.content_area, bg=COLORS["card_bg"], padx=20, pady=16, highlightbackground=COLORS["card_border"], highlightthickness=1)
        status_box.pack(fill="x", pady=10)

        s_title = tk.Label(status_box, text="Container State & Controls", font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 13, "bold"), fg=COLORS["text_primary"], bg=COLORS["card_bg"])
        s_title.pack(anchor="w", pady=(0, 10))

        btn_row = tk.Frame(status_box, bg=COLORS["card_bg"])
        btn_row.pack(fill="x", pady=6)

        actions = [
            ("⚡ Start Android Session", COLORS["accent_cyan"], lambda: self._run_command("waydroid session start")),
            ("⏹️ Stop Android Session", COLORS["button_bg"], lambda: self._run_command("waydroid session stop")),
            ("🔄 Restart Container Service", COLORS["button_bg"], lambda: self._run_command("sudo systemctl restart waydroid-container")),
            ("📱 Fullscreen Tablet Mode", COLORS["button_bg"], lambda: self._run_command("waydroid show-full-ui")),
        ]

        for text, color, cmd in actions:
            fg_col = COLORS["bg"] if color == COLORS["accent_cyan"] else COLORS["text_primary"]
            b = tk.Button(
                btn_row,
                text=text,
                font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9, "bold"),
                fg=fg_col,
                bg=color,
                bd=0,
                padx=12,
                pady=7,
                cursor="hand2",
                command=cmd
            )
            b.pack(side="left", padx=4)

        # Sideload APK Card
        apk_card = tk.Frame(self.content_area, bg=COLORS["card_bg"], padx=20, pady=16, highlightbackground=COLORS["card_border"], highlightthickness=1)
        apk_card.pack(fill="x", pady=16)

        apk_title = tk.Label(apk_card, text="📦 Sideload Android APK", font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 13, "bold"), fg=COLORS["accent_cyan"], bg=COLORS["card_bg"])
        apk_title.pack(anchor="w")

        apk_desc = tk.Label(apk_card, text="Select an Android .apk package from your PC and install it directly into Luca OS.", font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9), fg=COLORS["text_secondary"], bg=COLORS["card_bg"])
        apk_desc.pack(anchor="w", pady=(2, 10))

        apk_btn = tk.Button(
            apk_card,
            text="Choose .APK File to Install...",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 10, "bold"),
            fg=COLORS["text_primary"],
            bg=COLORS["button_hover"],
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
            command=self._sideload_apk
        )
        apk_btn.pack(anchor="w")

    # ==================== TAB: ESSENTIAL APPS ====================
    def _show_apps(self):
        self._clear_content()

        header = tk.Label(
            self.content_area,
            text="Essential Software Store",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 20, "bold"),
            fg=COLORS["text_primary"],
            bg=COLORS["bg"]
        )
        header.pack(anchor="w")

        sub = tk.Label(
            self.content_area,
            text="One-click installations for curated PC desktop and developer tools.",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 11),
            fg=COLORS["text_secondary"],
            bg=COLORS["bg"]
        )
        sub.pack(anchor="w", pady=(4, 20))

        apps = [
            ("Google Chrome", "The most popular web browser with synchronization.", "sudo apt install -y google-chrome-stable || flatpak install -y flathub com.google.Chrome"),
            ("VS Code", "Code editing redefined for development and scripting.", "sudo snap install --classic code || flatpak install -y flathub com.visualstudio.code"),
            ("VLC Media Player", "Plays every video and audio format flawlessly.", "sudo apt install -y vlc"),
            ("Spotify", "Stream millions of songs and podcasts on your desktop.", "flatpak install -y flathub com.spotify.Client || sudo snap install spotify"),
            ("Steam", "The premier PC gaming platform with Proton compatibility.", "sudo apt install -y steam"),
            ("LibreOffice", "Free office productivity suite (Docs, Sheets, Slides).", "sudo apt install -y libreoffice"),
        ]

        apps_frame = tk.Frame(self.content_area, bg=COLORS["bg"])
        apps_frame.pack(fill="both", expand=True)

        for i, (name, desc, install_cmd) in enumerate(apps):
            card = tk.Frame(apps_frame, bg=COLORS["card_bg"], padx=14, pady=12, highlightbackground=COLORS["card_border"], highlightthickness=1)
            card.pack(fill="x", pady=4)

            info = tk.Frame(card, bg=COLORS["card_bg"])
            info.pack(side="left", fill="x", expand=True)

            n = tk.Label(info, text=name, font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 11, "bold"), fg=COLORS["text_primary"], bg=COLORS["card_bg"])
            n.pack(anchor="w")

            d = tk.Label(info, text=desc, font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9), fg=COLORS["text_secondary"], bg=COLORS["card_bg"])
            d.pack(anchor="w")

            b = tk.Button(
                card,
                text="Install",
                font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9, "bold"),
                fg=COLORS["text_primary"],
                bg=COLORS["button_hover"],
                bd=0,
                padx=14,
                pady=5,
                cursor="hand2",
                command=lambda cmd=install_cmd, nm=name: self._install_app(nm, cmd)
            )
            b.pack(side="right")

    # ==================== TAB: PERSONALIZATION ====================
    def _show_desktop(self):
        self._clear_content()

        header = tk.Label(
            self.content_area,
            text="Personalize Luca OS",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 20, "bold"),
            fg=COLORS["text_primary"],
            bg=COLORS["bg"]
        )
        header.pack(anchor="w")

        sub = tk.Label(
            self.content_area,
            text="Customize dock position, dark mode, icons, and display settings.",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 11),
            fg=COLORS["text_secondary"],
            bg=COLORS["bg"]
        )
        sub.pack(anchor="w", pady=(4, 20))

        opts = [
            ("🌙 System Dark Mode", "Toggle deep OLED dark theme across desktop apps.", lambda: self._run_command("gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'")),
            ("☀️ System Light Mode", "Switch desktop applications to clean daylight theme.", lambda: self._run_command("gsettings set org.gnome.desktop.interface color-scheme 'default'")),
            ("📌 Bottom Dock (Android Style)", "Align application launcher dock to center bottom.", lambda: self._run_command("gsettings set org.gnome.shell.extensions.dash-to-dock dock-position 'BOTTOM'")),
            ("🖼️ Reset Luca Wallpaper", "Restore the official Luca OS desktop background.", lambda: self._run_command("gsettings set org.gnome.desktop.background picture-uri 'file:///usr/share/backgrounds/luca-wallpaper.png'")),
            ("⚙️ Open GNOME Tweaks", "Access fine-grained font, window, and gesture settings.", lambda: self._run_command("gnome-tweaks")),
        ]

        for title, desc, action in opts:
            row = tk.Frame(self.content_area, bg=COLORS["card_bg"], padx=16, pady=12, highlightbackground=COLORS["card_border"], highlightthickness=1)
            row.pack(fill="x", pady=4)

            lbl_frame = tk.Frame(row, bg=COLORS["card_bg"])
            lbl_frame.pack(side="left", fill="x", expand=True)

            t = tk.Label(lbl_frame, text=title, font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 11, "bold"), fg=COLORS["text_primary"], bg=COLORS["card_bg"])
            t.pack(anchor="w")
            d = tk.Label(lbl_frame, text=desc, font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9), fg=COLORS["text_secondary"], bg=COLORS["card_bg"])
            d.pack(anchor="w")

            btn = tk.Button(
                row,
                text="Apply",
                font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9, "bold"),
                fg=COLORS["accent_cyan"],
                bg=COLORS["button_bg"],
                bd=0,
                padx=16,
                pady=6,
                cursor="hand2",
                command=action
            )
            btn.pack(side="right")

    # ==================== TAB: DIAGNOSTICS & GPU ====================
    def _show_diagnostics(self):
        self._clear_content()

        header = tk.Label(
            self.content_area,
            text="System Specifications & GPU Mode",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 20, "bold"),
            fg=COLORS["text_primary"],
            bg=COLORS["bg"]
        )
        header.pack(anchor="w")

        sub = tk.Label(
            self.content_area,
            text="Hardware compatibility diagnostics and graphics acceleration mode.",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 11),
            fg=COLORS["text_secondary"],
            bg=COLORS["bg"]
        )
        sub.pack(anchor="w", pady=(4, 20))

        info_box = tk.Frame(self.content_area, bg=COLORS["card_bg"], padx=20, pady=16, highlightbackground=COLORS["card_border"], highlightthickness=1)
        info_box.pack(fill="x", pady=10)

        diag_items = [
            ("Operating System", self.specs["os"]),
            ("Linux Kernel", self.specs["kernel"]),
            ("CPU Architecture", self.specs["cpu"]),
            ("Wayland Display Session", "Active (Optimal for Android Multi-Window)" if self.specs["wayland"] else "X11 (Switch to Wayland for best performance)"),
            ("Waydroid Engine Status", "Installed & Configured" if self.specs["waydroid_installed"] else "Standby (Run Android Setup)"),
        ]

        for label, val in diag_items:
            r = tk.Frame(info_box, bg=COLORS["card_bg"], pady=4)
            r.pack(fill="x")
            l1 = tk.Label(r, text=label, font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 10, "bold"), fg=COLORS["text_secondary"], bg=COLORS["card_bg"], width=24, anchor="w")
            l1.pack(side="left")
            l2 = tk.Label(r, text=val, font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 10), fg=COLORS["text_primary"], bg=COLORS["card_bg"], anchor="w")
            l2.pack(side="left")

        # GPU Mode Selector
        gpu_box = tk.Frame(self.content_area, bg=COLORS["card_bg"], padx=20, pady=16, highlightbackground=COLORS["card_border"], highlightthickness=1)
        gpu_box.pack(fill="x", pady=16)

        g_title = tk.Label(gpu_box, text="🎮 Graphics Passthrough & GPU Tuning", font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 12, "bold"), fg=COLORS["accent_cyan"], bg=COLORS["card_bg"])
        g_title.pack(anchor="w", pady=(0, 6))

        g_desc = tk.Label(gpu_box, text="On hybrid laptops (e.g. Intel/AMD + NVIDIA), select which graphics card powers Android apps.", font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9), fg=COLORS["text_secondary"], bg=COLORS["card_bg"])
        g_desc.pack(anchor="w", pady=(0, 10))

        g_btn_row = tk.Frame(gpu_box, bg=COLORS["card_bg"])
        g_btn_row.pack(fill="x")

        gpu_opts = [
            ("Auto Hardware (Default)", lambda: self._run_command("luca-gpu-config auto")),
            ("Integrated GPU (Intel/AMD)", lambda: self._run_command("luca-gpu-config igpu")),
            ("Software EGL (Compatibility)", lambda: self._run_command("luca-gpu-config software")),
        ]

        for g_text, g_cmd in gpu_opts:
            b = tk.Button(g_btn_row, text=g_text, font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9), fg=COLORS["text_primary"], bg=COLORS["button_hover"], bd=0, padx=12, pady=6, cursor="hand2", command=g_cmd)
            b.pack(side="left", padx=4)

    # ==================== TAB: COMMUNITY ====================
    def _show_community(self):
        self._clear_content()

        header = tk.Label(
            self.content_area,
            text="Open Source Community & Support",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 20, "bold"),
            fg=COLORS["text_primary"],
            bg=COLORS["bg"]
        )
        header.pack(anchor="w")

        sub = tk.Label(
            self.content_area,
            text="Luca OS is 100% Free and Open Source Software. Join our community!",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 11),
            fg=COLORS["text_secondary"],
            bg=COLORS["bg"]
        )
        sub.pack(anchor="w", pady=(4, 20))

        links = [
            ("📖 Official Documentation", "Full installation, troubleshooting, and developer guides.", "https://github.com/luca-os/luca-os#readme"),
            ("🐛 Bug Tracker & Issues", "Report hardware incompatibilities, bugs, or request features.", "https://github.com/luca-os/luca-os/issues"),
            ("💬 Community Discussion", "Chat with other Luca OS users and developers.", "https://github.com/luca-os/luca-os/discussions"),
            ("📜 License (GPL-3.0)", "Complete transparency, freedom to modify, study, and distribute.", "https://www.gnu.org/licenses/gpl-3.0.html"),
        ]

        for t, d, url in links:
            card = tk.Frame(self.content_area, bg=COLORS["card_bg"], padx=16, pady=12, highlightbackground=COLORS["card_border"], highlightthickness=1)
            card.pack(fill="x", pady=4)

            info = tk.Frame(card, bg=COLORS["card_bg"])
            info.pack(side="left", fill="x", expand=True)

            t_lbl = tk.Label(info, text=t, font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 11, "bold"), fg=COLORS["accent_cyan"], bg=COLORS["card_bg"])
            t_lbl.pack(anchor="w")
            d_lbl = tk.Label(info, text=d, font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9), fg=COLORS["text_secondary"], bg=COLORS["card_bg"])
            d_lbl.pack(anchor="w")

            btn = tk.Button(
                card,
                text="Open Link",
                font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9),
                fg=COLORS["text_primary"],
                bg=COLORS["button_hover"],
                bd=0,
                padx=12,
                pady=6,
                cursor="hand2",
                command=lambda u=url: self._open_url(u)
            )
            btn.pack(side="right")

    # ==================== HELPERS ====================
    def _create_card(self, parent, title, desc, btn_text, btn_cmd, side="left"):
        card = tk.Frame(parent, bg=COLORS["card_bg"], padx=18, pady=16, highlightbackground=COLORS["card_border"], highlightthickness=1)
        card.pack(side=side, fill="both", expand=True, padx=6)

        t = tk.Label(card, text=title, font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 12, "bold"), fg=COLORS["accent_cyan"], bg=COLORS["card_bg"])
        t.pack(anchor="w")

        d = tk.Label(card, text=desc, font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9), fg=COLORS["text_secondary"], bg=COLORS["card_bg"], wraplength=310, justify="left")
        d.pack(anchor="w", pady=(4, 14))

        b = tk.Button(
            card,
            text=btn_text,
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9, "bold"),
            fg=COLORS["text_primary"],
            bg=COLORS["button_bg"],
            activebackground=COLORS["button_hover"],
            activeforeground=COLORS["accent_cyan"],
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            command=btn_cmd
        )
        b.pack(anchor="w")

    def _sideload_apk(self):
        file_path = filedialog.askopenfilename(
            title="Select Android Package (.apk)",
            filetypes=[("Android APK", "*.apk"), ("All Files", "*.*")]
        )
        if file_path:
            cmd = f"waydroid app install '{file_path}'"
            self._run_command(cmd)

    def _run_command(self, cmd):
        print(f"[Luca OS Welcome] Running: {cmd}")
        if sys.platform != "win32":
            subprocess.Popen(["/bin/bash", "-c", cmd])
            messagebox.showinfo("Luca OS", f"Command executed:\n{cmd}")
        else:
            messagebox.showinfo("Luca OS (Simulation)", f"Running in simulated Windows environment:\n{cmd}")

    def _install_app(self, name, cmd):
        resp = messagebox.askyesno("Install Application", f"Install {name} via system package manager?")
        if resp:
            self._run_command(cmd)

    def _open_url(self, url):
        import webbrowser
        webbrowser.open(url)

    def _toggle_autostart(self):
        enabled = self.autostart_var.get()
        os.makedirs(os.path.dirname(AUTOSTART_FILE), exist_ok=True)
        if enabled:
            content = """[Desktop Entry]
Type=Application
Name=Luca OS Welcome
Exec=/usr/local/bin/luca-welcome
Icon=luca-os
Terminal=false
Categories=Utility;System;
"""
            with open(AUTOSTART_FILE, "w", encoding="utf-8") as f:
                f.write(content)
        else:
            if os.path.exists(AUTOSTART_FILE):
                os.remove(AUTOSTART_FILE)

if __name__ == "__main__":
    app = LucaWelcomeApp()
    # If run in test mode (or headless), avoid blocking indefinitely
    if "--test" in sys.argv:
        app.update()
        print("Luca Welcome GUI initialized and tested successfully!")
        app.destroy()
    else:
        app.mainloop()
