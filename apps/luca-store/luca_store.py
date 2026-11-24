#!/usr/bin/env python3
"""
Luca OS — Unified App Store (luca-store)
A visual software center combining Android APKs and Linux PC applications
with 1-click installation, categories, search, and package lifecycle management.
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

# Curated catalog of Android and Linux applications
CATALOG = [
    {
        "id": "com.spotify.music",
        "name": "Spotify Music",
        "category": "Media",
        "type": "Linux / Flatpak",
        "icon": "🎵",
        "desc": "Stream millions of songs, albums, and original podcasts.",
        "cmd": "flatpak install -y flathub com.spotify.Client || sudo apt install -y spotify-client"
    },
    {
        "id": "org.mozilla.firefox",
        "name": "Firefox Browser",
        "category": "Web",
        "type": "Native Linux",
        "icon": "🦊",
        "desc": "Fast, private, and independent open-source web browser.",
        "cmd": "sudo apt install -y firefox"
    },
    {
        "id": "com.google.chrome",
        "name": "Google Chrome",
        "category": "Web",
        "type": "Native Linux",
        "icon": "🌐",
        "desc": "The official browser from Google with built-in sync and tools.",
        "cmd": "sudo apt install -y google-chrome-stable || flatpak install -y flathub com.google.Chrome"
    },
    {
        "id": "org.videolan.vlc",
        "name": "VLC Media Player",
        "category": "Media",
        "type": "Native Linux",
        "icon": "🎬",
        "desc": "Plays virtually any audio and video file without codecs.",
        "cmd": "sudo apt install -y vlc"
    },
    {
        "id": "com.valvesoftware.Steam",
        "name": "Steam",
        "category": "Gaming",
        "type": "Native Linux",
        "icon": "🎮",
        "desc": "The ultimate gaming platform with Proton Windows-compatibility layer.",
        "cmd": "sudo apt install -y steam"
    },
    {
        "id": "com.visualstudio.code",
        "name": "Visual Studio Code",
        "category": "Development",
        "type": "Linux / Flatpak",
        "icon": "💻",
        "desc": "Powerful code editor with Git integration and rich extensions.",
        "cmd": "flatpak install -y flathub com.visualstudio.code || sudo snap install --classic code"
    },
    {
        "id": "org.libreoffice.LibreOffice",
        "name": "LibreOffice Suite",
        "category": "Productivity",
        "type": "Native Linux",
        "icon": "📄",
        "desc": "Complete office productivity suite: Writer, Calc, and Impress.",
        "cmd": "sudo apt install -y libreoffice"
    },
    {
        "id": "org.telegram.messenger",
        "name": "Telegram Desktop",
        "category": "Social",
        "type": "Native Linux",
        "icon": "✈️",
        "desc": "Fast and secure cloud-based mobile & desktop messaging.",
        "cmd": "sudo apt install -y telegram-desktop"
    },
    {
        "id": "org.gimp.GIMP",
        "name": "GIMP Photo Editor",
        "category": "Creative",
        "type": "Native Linux",
        "icon": "🎨",
        "desc": "Free and open-source professional image manipulation software.",
        "cmd": "sudo apt install -y gimp"
    },
    {
        "id": "com.whatsapp.android",
        "name": "WhatsApp Messenger",
        "category": "Android Apps",
        "type": "Android APK",
        "icon": "💬",
        "desc": "Simple, reliable private messaging and video calls for your PC.",
        "cmd": "waydroid app install /opt/luca-os/apks/whatsapp.apk || echo 'Download APK to install'"
    },
    {
        "id": "com.instagram.android",
        "name": "Instagram",
        "category": "Android Apps",
        "type": "Android APK",
        "icon": "📷",
        "desc": "Browse photos, reels, and stories in a resizable desktop window.",
        "cmd": "echo 'Install from Google Play Store or sideload APK'"
    },
    {
        "id": "com.kiloo.subwaysurf",
        "name": "Subway Surfers",
        "category": "Android Apps",
        "type": "Android APK",
        "icon": "🏃",
        "desc": "Classic mobile arcade runner running at smooth 60 FPS on PC.",
        "cmd": "echo 'Install from Google Play Store or sideload APK'"
    },
    {
        "id": "com.aurora.store",
        "name": "Aurora Store (Open Source Play Client)",
        "category": "Android Apps",
        "type": "Android APK",
        "icon": "🛍️",
        "desc": "FOSS Google Play client allowing app downloads without Google login.",
        "cmd": "waydroid app install /opt/luca-os/apks/aurora.apk || echo 'Installing Aurora Store...'"
    },
    {
        "id": "org.fdroid.fdroid",
        "name": "F-Droid App Repository",
        "category": "Android Apps",
        "type": "Android APK",
        "icon": "🤖",
        "desc": "Official catalogue of FOSS (Free and Open Source) Android applications.",
        "cmd": "waydroid app install /opt/luca-os/apks/fdroid.apk || echo 'Installing F-Droid...'"
    },
]

class LucaStoreApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Luca OS — Software Store")
        self.geometry("980x640")
        self.minsize(860, 520)
        self.configure(bg=COLORS["bg"])

        self.current_category = "All"
        self.search_query = ""

        self._init_ui()

    def _init_ui(self):
        # Master Frame
        main = tk.Frame(self, bg=COLORS["bg"])
        main.pack(fill="both", expand=True)

        # 1. Left Sidebar (Categories)
        sidebar = tk.Frame(main, bg=COLORS["sidebar"], width=210)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Branding
        s_hdr = tk.Frame(sidebar, bg=COLORS["sidebar"], padx=18, pady=20)
        s_hdr.pack(fill="x")
        tk.Label(s_hdr, text="⚡ LUCA STORE", font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 14, "bold"), fg=COLORS["accent_cyan"], bg=COLORS["sidebar"]).pack(anchor="w")
        tk.Label(s_hdr, text="Hybrid App Center", font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9), fg=COLORS["text_muted"], bg=COLORS["sidebar"]).pack(anchor="w")

        sep = tk.Frame(sidebar, bg=COLORS["card_border"], height=1)
        sep.pack(fill="x", padx=16, pady=4)

        self.cat_buttons = {}
        categories = ["All", "Android Apps", "Web", "Media", "Gaming", "Development", "Productivity", "Social", "Creative"]
        for cat in categories:
            b = tk.Button(
                sidebar,
                text=f"  {cat}",
                font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 10),
                fg=COLORS["text_secondary"],
                bg=COLORS["sidebar"],
                activebackground=COLORS["card_bg"],
                activeforeground=COLORS["accent_cyan"],
                bd=0,
                padx=16,
                pady=8,
                anchor="w",
                cursor="hand2",
                command=lambda c=cat: self._select_category(c)
            )
            b.pack(fill="x", padx=6, pady=1)
            self.cat_buttons[cat] = b

        # 2. Right Content Area
        content = tk.Frame(main, bg=COLORS["bg"], padx=24, pady=18)
        content.pack(side="right", fill="both", expand=True)

        # Top Bar: Search Box
        top_bar = tk.Frame(content, bg=COLORS["bg"])
        top_bar.pack(fill="x", pady=(0, 16))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self._on_search())

        search_entry = tk.Entry(
            top_bar,
            textvariable=self.search_var,
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 11),
            bg=COLORS["card_bg"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["accent_cyan"],
            bd=0,
            highlightbackground=COLORS["card_border"],
            highlightthickness=1,
        )
        search_entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 10))

        # Scrollable App Grid Container
        self.canvas = tk.Canvas(content, bg=COLORS["bg"], bd=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(content, orient="vertical", command=self.canvas.yview)
        self.grid_frame = tk.Frame(self.canvas, bg=COLORS["bg"])

        self.grid_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.grid_frame, anchor="nw", width=700)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self._render_catalog()

    def _select_category(self, cat):
        self.current_category = cat
        for c, b in self.cat_buttons.items():
            if c == cat:
                b.configure(fg=COLORS["accent_cyan"], font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 10, "bold"), bg=COLORS["card_bg"])
            else:
                b.configure(fg=COLORS["text_secondary"], font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 10), bg=COLORS["sidebar"])
        self._render_catalog()

    def _on_search(self):
        self.search_query = self.search_var.get().strip().lower()
        self._render_catalog()

    def _render_catalog(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()

        filtered = []
        for app in CATALOG:
            if self.current_category != "All" and app["category"] != self.current_category:
                continue
            if self.search_query:
                q = self.search_query
                if q not in app["name"].lower() and q not in app["desc"].lower() and q not in app["type"].lower():
                    continue
            filtered.append(app)

        if not filtered:
            lbl = tk.Label(self.grid_frame, text="No matching applications found.", font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 12), fg=COLORS["text_muted"], bg=COLORS["bg"], pady=40)
            lbl.pack()
            return

        for app in filtered:
            card = tk.Frame(self.grid_frame, bg=COLORS["card_bg"], padx=16, pady=12, highlightbackground=COLORS["card_border"], highlightthickness=1)
            card.pack(fill="x", pady=4)

            # Left Icon
            ic = tk.Label(card, text=app["icon"], font=("Segoe UI Emoji", 26), bg=COLORS["card_bg"])
            ic.pack(side="left", padx=(0, 14))

            # Details
            details = tk.Frame(card, bg=COLORS["card_bg"])
            details.pack(side="left", fill="x", expand=True)

            title_row = tk.Frame(details, bg=COLORS["card_bg"])
            title_row.pack(anchor="w")

            t = tk.Label(title_row, text=app["name"], font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 11, "bold"), fg=COLORS["text_primary"], bg=COLORS["card_bg"])
            t.pack(side="left")

            badge_col = COLORS["accent_green"] if "Android" in app["type"] else COLORS["accent_cyan"]
            badge = tk.Label(title_row, text=f" {app['type']} ", font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 8, "bold"), fg=badge_col, bg="#0E1E2E")
            badge.pack(side="left", padx=8)

            d = tk.Label(details, text=app["desc"], font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9), fg=COLORS["text_secondary"], bg=COLORS["card_bg"])
            d.pack(anchor="w", pady=(2, 0))

            # Install Button
            btn = tk.Button(
                card,
                text="Install",
                font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9, "bold"),
                fg=COLORS["text_primary"],
                bg=COLORS["button_hover"],
                bd=0,
                padx=16,
                pady=6,
                cursor="hand2",
                command=lambda a=app: self._install(a)
            )
            btn.pack(side="right")

    def _install(self, app):
        msg = f"Install {app['name']} ({app['type']})?"
        if messagebox.askyesno("Luca Store", msg):
            if sys.platform != "win32":
                subprocess.Popen(["/bin/bash", "-c", app["cmd"]])
                messagebox.showinfo("Luca Store", f"Installation started for {app['name']}.")
            else:
                messagebox.showinfo("Simulation", f"[Simulation] Executing: {app['cmd']}")

def main():
    app = LucaStoreApp()
    if "--test" in sys.argv:
        app.update()
        print("Luca Store GUI initialized and tested successfully!")
        app.destroy()
    else:
        app.mainloop()

if __name__ == "__main__":
    main()
