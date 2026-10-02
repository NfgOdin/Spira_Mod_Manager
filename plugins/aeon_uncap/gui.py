import os
import json
import tkinter as tk
from tkinter import ttk

class AeonUncapTab:
    def __init__(self, parent_frame, manager_gui):
        self.parent = parent_frame
        self.manager = manager_gui

        # Load themes
        self.bg_color = self.manager.bg_color
        self.card_color = self.manager.card_color
        self.accent_color = self.manager.accent_color
        self.accent_hover = self.manager.accent_hover
        self.text_color = self.manager.text_color
        self.text_dim = self.manager.text_dim
        self.border_color = self.manager.border_color
        self.success_color = self.manager.success_color

        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(self.plugin_dir, "aeon_uncap_config.json")

        self.is_enabled = tk.BooleanVar(value=True)
        self.load_config()

        self.create_widgets()

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    self.is_enabled.set(cfg.get("enabled", True))
            except Exception:
                pass

    def save_config(self):
        cfg = {"enabled": self.is_enabled.get()}
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=2)
            self.manager.log("Aeon Stat Uncapper settings saved.", "success")
        except Exception as e:
            self.manager.log(f"Failed to save Aeon Uncapper config: {e}", "error")

    def retheme(self):
        self.bg_color = self.manager.bg_color
        self.card_color = self.manager.card_color
        self.accent_color = self.manager.accent_color
        self.accent_hover = self.manager.accent_hover
        self.text_color = self.manager.text_color
        self.text_dim = self.manager.text_dim
        self.border_color = self.manager.border_color
        self.success_color = self.manager.success_color

        if hasattr(self, "card_panel"):
            self.card_panel.configure(bg=self.card_color, highlightbackground=self.border_color)
        if hasattr(self, "lbl_title"):
            self.lbl_title.configure(fg=self.accent_color, bg=self.bg_color)
        if hasattr(self, "lbl_desc"):
            self.lbl_desc.configure(fg=self.text_color, bg=self.bg_color)

        self.manager.update_widget_colors(self.parent)

    def create_widgets(self):
        # Header
        self.lbl_title = tk.Label(
            self.parent,
            text="🐉 Aeon Stat Uncapper *WIP*",
            font=("Segoe UI", 14, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        self.lbl_title._is_title = True
        self.lbl_title.pack(anchor="w", pady=(10, 5))

        self.lbl_desc = tk.Label(
            self.parent,
            text="⚠️ [Untested / Work in Progress]\nUnlocks Yuna's stat evaluation cap when deriving Aeon power. In vanilla FFX, Aeons stop scaling once Yuna reaches 9,999 HP and 999 MP. With this plugin active, Aeons continue scaling with Yuna up to 99,999 HP and 9,999 MP.",
            font=("Segoe UI", 10),
            fg=self.text_color,
            bg=self.bg_color,
            justify="left",
            wraplength=700
        )
        self.lbl_desc.pack(anchor="w", pady=(0, 15))

        # Card container
        self.card_panel = tk.Frame(
            self.parent,
            bd=1,
            relief="solid",
            highlightthickness=0,
            bg=self.card_color,
            padx=20,
            pady=20
        )
        self.card_panel._is_card = True
        self.card_panel.pack(fill="x", pady=5)

        # Status row
        row_status = tk.Frame(self.card_panel, bg=self.card_color)
        row_status.pack(fill="x", pady=(0, 15))

        lbl_status_title = tk.Label(
            row_status,
            text="Plugin Status:",
            font=("Segoe UI", 10, "bold"),
            fg=self.text_color,
            bg=self.card_color
        )
        lbl_status_title.pack(side="left", padx=(0, 10))

        lbl_status_val = tk.Label(
            row_status,
            text="Active (Hooks automatically when FFX launches)",
            font=("Segoe UI", 10),
            fg=self.success_color,
            bg=self.card_color
        )
        lbl_status_val._is_status_pill = True
        lbl_status_val.pack(side="left")

        # Feature highlights
        info_box = tk.Label(
            self.card_panel,
            text="• Vanilla: Yuna HP clamp = 9,999 (PBase max contribution: 99)\n"
                 "• Uncapped: Yuna HP clamp = 99,999 (PBase max contribution: 999)\n\n"
                 "• Vanilla: Yuna MP clamp = 999 (PBase max contribution: 99)\n"
                 "• Uncapped: Yuna MP clamp = 9,999 (PBase max contribution: 999)\n\n"
                 "• Zero risk to game saves: patches memory in RAM on launch without modifying FFX.exe on disk.",
            font=("Segoe UI", 9),
            fg=self.text_dim,
            bg=self.card_color,
            justify="left"
        )
        info_box.pack(anchor="w", pady=(0, 15))

        self.manager.update_widget_colors(self.parent)
