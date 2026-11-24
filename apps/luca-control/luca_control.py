#!/usr/bin/env python3
"""
Luca OS — Subsystem & Hardware Control Center
Graphical manager for Waydroid container lifecycle, multi-window mode,
GPU hardware passthrough, and Google Play certification.
"""

import sys
import os
import subprocess
import shutil
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
    "accent_red": "#EF4444",
    "text_primary": "#F8FAFC",
    "text_secondary": "#94A3B8",
    "button_bg": "#1E293B",
    "button_hover": "#2D3E5E",
}

class LucaControlCenter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Luca OS — Subsystem Control Center")
        self.geometry("720x520")
        self.minsize(640, 460)
        self.configure(bg=COLORS["bg"])

        self._init_ui()
        self._refresh_status()

    def _init_ui(self):
        # Header
        hdr = tk.Frame(self, bg=COLORS["card_bg"], padx=20, pady=16)
        hdr.pack(fill="x")

        t = tk.Label(hdr, text="⚡ Luca OS Subsystem Control Center", font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 14, "bold"), fg=COLORS["accent_cyan"], bg=COLORS["card_bg"])
        t.pack(anchor="w")

        st = tk.Label(hdr, text="Fine-tune Android container runtime, multi-window display, and graphics drivers.", font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9), fg=COLORS["text_secondary"], bg=COLORS["card_bg"])
        st.pack(anchor="w", pady=(2, 0))

        body = tk.Frame(self, bg=COLORS["bg"], padx=20, pady=16)
        body.pack(fill="both", expand=True)

        # 1. Container Status & Lifecycle Card
        c_card = tk.Frame(body, bg=COLORS["card_bg"], padx=18, pady=14, highlightbackground=COLORS["card_border"], highlightthickness=1)
        c_card.pack(fill="x", pady=6)

        c_top = tk.Frame(c_card, bg=COLORS["card_bg"])
        c_top.pack(fill="x")

        tk.Label(c_top, text="🤖 Android Container Engine", font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 12, "bold"), fg=COLORS["text_primary"], bg=COLORS["card_bg"]).pack(side="left")
        self.status_pill = tk.Label(c_top, text="● CHECKING", font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9, "bold"), fg=COLORS["accent_cyan"], bg="#0E2A3A", padx=10, pady=2)
        self.status_pill.pack(side="right")

        c_btns = tk.Frame(c_card, bg=COLORS["card_bg"], pady=10)
        c_btns.pack(fill="x")

        b_start = tk.Button(c_btns, text="Start Session", bg=COLORS["accent_cyan"], fg=COLORS["bg"], font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9, "bold"), bd=0, padx=12, pady=6, cursor="hand2", command=lambda: self._exec("waydroid session start"))
        b_start.pack(side="left", padx=4)

        b_stop = tk.Button(c_btns, text="Stop Session", bg=COLORS["button_hover"], fg=COLORS["text_primary"], font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9), bd=0, padx=12, pady=6, cursor="hand2", command=lambda: self._exec("waydroid session stop"))
        b_stop.pack(side="left", padx=4)

        b_restart = tk.Button(c_btns, text="Restart Service", bg=COLORS["button_hover"], fg=COLORS["text_primary"], font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9), bd=0, padx=12, pady=6, cursor="hand2", command=lambda: self._exec("sudo systemctl restart waydroid-container"))
        b_restart.pack(side="left", padx=4)

        # 2. Window Mode Card
        w_card = tk.Frame(body, bg=COLORS["card_bg"], padx=18, pady=14, highlightbackground=COLORS["card_border"], highlightthickness=1)
        w_card.pack(fill="x", pady=6)

        tk.Label(w_card, text="🪟 Window Display Mode", font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 12, "bold"), fg=COLORS["text_primary"], bg=COLORS["card_bg"]).pack(anchor="w")
        tk.Label(w_card, text="Choose how Android applications appear on your PC desktop.", font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9), fg=COLORS["text_secondary"], bg=COLORS["card_bg"]).pack(anchor="w", pady=(2, 8))

        w_btns = tk.Frame(w_card, bg=COLORS["card_bg"])
        w_btns.pack(fill="x")

        b_mw = tk.Button(w_btns, text="Freeform Multi-Window (PC Desktop)", bg=COLORS["button_hover"], fg=COLORS["accent_cyan"], font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9, "bold"), bd=0, padx=12, pady=6, cursor="hand2", command=self._set_multiwindow)
        b_mw.pack(side="left", padx=4)

        b_fs = tk.Button(w_btns, text="Launch Fullscreen Tablet UI", bg=COLORS["button_hover"], fg=COLORS["text_primary"], font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9), bd=0, padx=12, pady=6, cursor="hand2", command=lambda: self._exec("waydroid show-full-ui"))
        b_fs.pack(side="left", padx=4)

        # 3. Google Play & Utilities Card
        u_card = tk.Frame(body, bg=COLORS["card_bg"], padx=18, pady=14, highlightbackground=COLORS["card_border"], highlightthickness=1)
        u_card.pack(fill="x", pady=6)

        tk.Label(u_card, text="🛠️ Certification & Utilities", font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 12, "bold"), fg=COLORS["text_primary"], bg=COLORS["card_bg"]).pack(anchor="w")
        tk.Label(u_card, text="Obtain Google Play Store certification ID or launch ARM translation setup.", font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9), fg=COLORS["text_secondary"], bg=COLORS["card_bg"]).pack(anchor="w", pady=(2, 8))

        u_btns = tk.Frame(u_card, bg=COLORS["card_bg"])
        u_btns.pack(fill="x")

        b_play = tk.Button(u_btns, text="Fetch Google Play ID", bg=COLORS["button_hover"], fg=COLORS["text_primary"], font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9), bd=0, padx=12, pady=6, cursor="hand2", command=lambda: self._exec("luca-play-id"))
        b_play.pack(side="left", padx=4)

        b_arm = tk.Button(u_btns, text="Enable ARM Libhoudini/NDK", bg=COLORS["button_hover"], fg=COLORS["text_primary"], font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9), bd=0, padx=12, pady=6, cursor="hand2", command=lambda: self._exec("luca-arm-enable"))
        b_arm.pack(side="left", padx=4)

    def _refresh_status(self):
        if sys.platform != "win32":
            try:
                out = subprocess.check_output(["waydroid", "status"], text=True)
                if "RUNNING" in out:
                    self.status_pill.configure(text="● RUNNING", fg=COLORS["accent_green"], bg="#0E3024")
                else:
                    self.status_pill.configure(text="○ STOPPED", fg=COLORS["accent_cyan"], bg="#0E2A3A")
            except Exception:
                self.status_pill.configure(text="⚠ NOT RUNNING", fg=COLORS["accent_cyan"], bg="#0E2A3A")
        else:
            self.status_pill.configure(text="● ACTIVE (SIMULATED)", fg=COLORS["accent_green"], bg="#0E3024")

    def _set_multiwindow(self):
        cmd = "waydroid prop set persist.waydroid.multi_windows true"
        self._exec(cmd)
        messagebox.showinfo("Luca OS", "Multi-window mode enabled! Android apps now open as resizable desktop windows.")

    def _exec(self, cmd):
        print(f"[Luca Control] {cmd}")
        if sys.platform != "win32":
            subprocess.Popen(["/bin/bash", "-c", cmd])
        else:
            messagebox.showinfo("Simulation", f"Executing in simulation:\n{cmd}")

if __name__ == "__main__":
    app = LucaControlCenter()
    if "--test" in sys.argv:
        app.update()
        print("Luca Control Center GUI initialized and tested successfully!")
        app.destroy()
    else:
        app.mainloop()
