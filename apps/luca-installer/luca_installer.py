#!/usr/bin/env python3
"""
Luca OS — Package & APK Manager (Graphical & CLI)
Enables 1-click sideloading of Android APK packages and Linux application management.
"""

import sys
import os
import subprocess
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

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

class LucaInstallerApp(tk.Tk):
    def __init__(self, target_file=None):
        super().__init__()
        self.title("Luca OS — Package & APK Installer")
        self.geometry("680x480")
        self.minsize(580, 400)
        self.configure(bg=COLORS["bg"])

        self.selected_file = target_file
        self._init_ui()

        if target_file and os.path.exists(target_file):
            self._set_file(target_file)

    def _init_ui(self):
        # Header
        header = tk.Frame(self, bg=COLORS["card_bg"], padx=20, pady=16)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="⚡ Luca OS Application Installer",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 14, "bold"),
            fg=COLORS["accent_cyan"],
            bg=COLORS["card_bg"]
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            header,
            text="Install Android packages (.apk), Debian packages (.deb), or Flatpaks",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9),
            fg=COLORS["text_secondary"],
            bg=COLORS["card_bg"]
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        # Main Body
        body = tk.Frame(self, bg=COLORS["bg"], padx=24, pady=20)
        body.pack(fill="both", expand=True)

        # File Drop/Select Card
        self.drop_card = tk.Frame(body, bg=COLORS["card_bg"], padx=20, pady=24, highlightbackground=COLORS["card_border"], highlightthickness=1)
        self.drop_card.pack(fill="x", pady=10)

        self.file_icon = tk.Label(self.drop_card, text="📦", font=("Segoe UI Emoji", 32), bg=COLORS["card_bg"])
        self.file_icon.pack()

        self.file_label = tk.Label(
            self.drop_card,
            text="Choose an APK or Linux package to install",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 12, "bold"),
            fg=COLORS["text_primary"],
            bg=COLORS["card_bg"]
        )
        self.file_label.pack(pady=(6, 4))

        self.path_label = tk.Label(
            self.drop_card,
            text="No file currently selected",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 9),
            fg=COLORS["text_secondary"],
            bg=COLORS["card_bg"],
            wraplength=500
        )
        self.path_label.pack(pady=(0, 14))

        browse_btn = tk.Button(
            self.drop_card,
            text="Browse Files...",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 10),
            fg=COLORS["text_primary"],
            bg=COLORS["button_hover"],
            bd=0,
            padx=16,
            pady=6,
            cursor="hand2",
            command=self._browse_file
        )
        browse_btn.pack()

        # Log Output / Status
        self.log_text = tk.Text(body, height=6, bg="#070A10", fg=COLORS["accent_cyan"], font=("Consolas" if sys.platform == "win32" else "monospace", 9), bd=0, padx=10, pady=8)
        self.log_text.pack(fill="both", expand=True, pady=10)
        self.log_text.insert("end", "[Luca Installer Ready] Select an APK or DEB file to begin installation.\n")
        self.log_text.configure(state="disabled")

        # Bottom Button Bar
        btn_bar = tk.Frame(self, bg=COLORS["bg"], padx=24, pady=16)
        btn_bar.pack(fill="x", side="bottom")

        self.install_btn = tk.Button(
            btn_bar,
            text="🚀 Install Now",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 11, "bold"),
            fg=COLORS["bg"],
            bg=COLORS["accent_cyan"],
            activebackground=COLORS["accent_blue"],
            activeforeground="#FFFFFF",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
            state="disabled",
            command=self._do_install
        )
        self.install_btn.pack(side="right")

        quit_btn = tk.Button(
            btn_bar,
            text="Cancel",
            font=("Segoe UI" if sys.platform == "win32" else "Ubuntu", 10),
            fg=COLORS["text_secondary"],
            bg=COLORS["button_bg"],
            bd=0,
            padx=14,
            pady=8,
            cursor="hand2",
            command=self.destroy
        )
        quit_btn.pack(side="right", padx=10)

    def _browse_file(self):
        f = filedialog.askopenfilename(
            title="Select Application Package",
            filetypes=[
                ("Supported Packages", "*.apk;*.deb;*.flatpakref"),
                ("Android Package (*.apk)", "*.apk"),
                ("Debian Package (*.deb)", "*.deb"),
                ("All Files", "*.*")
            ]
        )
        if f:
            self._set_file(f)

    def _set_file(self, filepath):
        self.selected_file = filepath
        basename = os.path.basename(filepath)
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        ext = os.path.splitext(filepath)[1].lower()

        if ext == ".apk":
            self.file_icon.configure(text="🤖")
            self.file_label.configure(text=f"Android Package: {basename}")
        elif ext == ".deb":
            self.file_icon.configure(text="🐧")
            self.file_label.configure(text=f"Debian Package: {basename}")
        else:
            self.file_icon.configure(text="📦")
            self.file_label.configure(text=f"Package: {basename}")

        self.path_label.configure(text=f"{filepath} ({size_mb:.1f} MB)")
        self.install_btn.configure(state="normal")
        self._log(f"Loaded target package: {filepath} ({size_mb:.1f} MB)")

    def _log(self, text):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"> {text}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _do_install(self):
        if not self.selected_file or not os.path.exists(self.selected_file):
            messagebox.showerror("Error", "No valid file selected.")
            return

        ext = os.path.splitext(self.selected_file)[1].lower()
        self.install_btn.configure(state="disabled")

        if ext == ".apk":
            self._log("Installing Android application via Waydroid...")
            cmd = f"waydroid app install '{self.selected_file}'"
        elif ext == ".deb":
            self._log("Installing Linux debian package via apt...")
            cmd = f"sudo apt install -y '{self.selected_file}'"
        else:
            cmd = f"echo 'Unsupported file extension: {ext}'"

        if sys.platform != "win32":
            try:
                out = subprocess.check_output(["/bin/bash", "-c", cmd], stderr=subprocess.STDOUT, text=True)
                self._log(out)
                self._log("Installation completed successfully!")
                messagebox.showinfo("Success", "Installation completed!")
            except subprocess.CalledProcessError as e:
                self._log(f"Error during installation:\n{e.output}")
                messagebox.showerror("Installation Failed", f"Command failed:\n{e.output}")
        else:
            self._log(f"[Windows Simulation Mode] Executed: {cmd}")
            messagebox.showinfo("Simulation Mode", f"Simulated execution:\n{cmd}")

        self.install_btn.configure(state="normal")

def cli_main():
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        target = sys.argv[1]
        print(f"Installing {target} in CLI mode...")
        ext = os.path.splitext(target)[1].lower()
        if ext == ".apk":
            cmd = f"waydroid app install '{target}'"
        elif ext == ".deb":
            cmd = f"sudo apt install -y '{target}'"
        else:
            print(f"Unsupported package: {ext}")
            sys.exit(1)
        if sys.platform != "win32":
            subprocess.run(["/bin/bash", "-c", cmd], check=True)
        else:
            print(f"[Simulated] {cmd}")
        print("Installed.")
        return

    target = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else None
    app = LucaInstallerApp(target)
    if "--test" in sys.argv:
        app.update()
        print("Luca Installer GUI initialized and tested successfully!")
        app.destroy()
    else:
        app.mainloop()

if __name__ == "__main__":
    cli_main()
