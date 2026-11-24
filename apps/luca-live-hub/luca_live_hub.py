#!/usr/bin/env python3
"""
Luca OS — Live Session Assistant (luca-live-hub)
Floating desktop companion for users booting Luca OS directly from a Live USB pendrive.
Monitors persistence health, battery, and offers 1-click permanent installation.
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

VERSION = "1.0.0"

COLORS = {
    "bg": "#0B101D",
    "card_bg": "#131C31",
    "card_border": "#1E2C4B",
    "accent_cyan": "#00F2FE",
    "accent_blue": "#3B82F6",
    "accent_green": "#10B981",
    "accent_yellow": "#F59E0B",
    "text_primary": "#F8FAFC",
    "text_secondary": "#94A3B8",
    "button_bg": "#1E293B",
    "button_hover": "#2D3E5E",
}

class LucaLiveHubApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Luca OS Live Hub")
        self.geometry("640x440")
        self.minsize(560, 380)
        self.configure(bg=COLORS["bg"])

        self.is_live = False
        self.is_persistent = False
        self._detect_environment()
        self._init_ui()

    def _detect_environment(self):
        if sys.platform != "win32":
            self.is_live = os.path.exists("/run/casper") or os.path.exists("/run/live")
            try:
                out = subprocess.check_output(["mount"], text=True)
                self.is_persistent = "casper-rw" in out or "cow" in out
            except Exception:
                self.is_persistent = False
        else:
            self.is_live = True
            self.is_persistent = True

    def _init_ui(self):
        # Header Banner
        hdr = tk.Frame(self, bg=COLORS["card_bg"], padx=20, pady=16)
        hdr.pack(fill="x")

        title = tk.Label(
            hdr,
            text="⚡ Luca OS — Live USB Session Active",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 14, "bold"),
            fg=COLORS["accent_cyan"],
            bg=COLORS["card_bg"]
        )
        title.pack(anchor="w")

        sub = tk.Label(
            hdr,
            text="Running directly from USB flash memory with hardware passthrough.",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9),
            fg=COLORS["text_secondary"],
            bg=COLORS["card_bg"]
        )
        sub.pack(anchor="w", pady=(2, 0))

        # Main Body
        body = tk.Frame(self, bg=COLORS["bg"], padx=20, pady=16)
        body.pack(fill="both", expand=True)

        # Persistence Status Card
        p_card = tk.Frame(body, bg=COLORS["card_bg"], padx=16, pady=14, highlightbackground=COLORS["card_border"], highlightthickness=1)
        p_card.pack(fill="x", pady=6)

        p_row = tk.Frame(p_card, bg=COLORS["card_bg"])
        p_row.pack(fill="x")

        tk.Label(p_row, text="💾 Persistent Storage Status:", font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 11, "bold"), fg=COLORS["text_primary"], bg=COLORS["card_bg"]).pack(side="left")

        if self.is_persistent:
            pill = tk.Label(p_row, text="● PERSISTENCE ACTIVE", font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9, "bold"), fg=COLORS["accent_green"], bg="#0E3024", padx=8, pady=2)
            pill.pack(side="right")
            msg = "All files, Wi-Fi passwords, and installed Android apps are safely saved to your USB drive."
        else:
            pill = tk.Label(p_row, text="⚠ TEMPORARY (READ-ONLY)", font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9, "bold"), fg=COLORS["accent_yellow"], bg="#2E240E", padx=8, pady=2)
            pill.pack(side="right")
            msg = "Running in temporary mode. Changes will be reset upon reboot."

        tk.Label(p_card, text=msg, font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9), fg=COLORS["text_secondary"], bg=COLORS["card_bg"]).pack(anchor="w", pady=(6, 0))

        # Action Cards
        actions_frame = tk.Frame(body, bg=COLORS["bg"])
        actions_frame.pack(fill="x", pady=10)

        # 1. Install to PC Hard Drive
        self._action_card(
            actions_frame,
            title="💻 Install to Internal Hard Drive (SSD/NVMe)",
            desc="Love Luca OS? Install it alongside or replacing Windows for maximum performance.",
            btn_text="Launch Installer",
            btn_cmd=self._launch_installer,
            highlight=True
        )

        # 2. Open Android Subsystem
        self._action_card(
            actions_frame,
            title="🤖 Launch Android App Subsystem",
            desc="Start Waydroid to run mobile apps and Google Play Store directly on your PC.",
            btn_text="Open Android",
            btn_cmd=lambda: self._exec("luca-control"),
            highlight=False
        )

    def _action_card(self, parent, title, desc, btn_text, btn_cmd, highlight=False):
        c = tk.Frame(parent, bg=COLORS["card_bg"], padx=16, pady=12, highlightbackground=COLORS["card_border"], highlightthickness=1)
        c.pack(fill="x", pady=4)

        t = tk.Label(c, text=title, font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 11, "bold"), fg=COLORS["accent_cyan"] if highlight else COLORS["text_primary"], bg=COLORS["card_bg"])
        t.pack(anchor="w")

        d = tk.Label(c, text=desc, font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9), fg=COLORS["text_secondary"], bg=COLORS["card_bg"])
        d.pack(anchor="w", pady=(2, 6))

        b_bg = COLORS["accent_cyan"] if highlight else COLORS["button_hover"]
        b_fg = COLORS["bg"] if highlight else COLORS["text_primary"]
        b = tk.Button(
            c,
            text=btn_text,
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9, "bold"),
            fg=b_fg,
            bg=b_bg,
            bd=0,
            padx=14,
            pady=6,
            cursor="hand2",
            command=btn_cmd
        )
        b.pack(anchor="w")

    def _launch_installer(self):
        if sys.platform != "win32":
            cmd = "calamares || ubiquity || sudo /usr/bin/luca-installer"
            subprocess.Popen(["/bin/bash", "-c", cmd])
        else:
            messagebox.showinfo("Simulation", "Launching Calamares / Luca OS System Installer.")

    def _exec(self, cmd):
        if sys.platform != "win32":
            subprocess.Popen(["/bin/bash", "-c", cmd])
        else:
            messagebox.showinfo("Simulation", f"Executing: {cmd}")

def main():
    app = LucaLiveHubApp()
    if "--test" in sys.argv:
        app.update()
        print("Luca Live Hub GUI initialized and tested successfully!")
        app.destroy()
    else:
        app.mainloop()

if __name__ == "__main__":
    main()
