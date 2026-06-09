from __future__ import annotations
import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    ITEMS = [
        ("🏠", "Dashboard"),
        ("📄", "Make Report"),
        ("📊", "Generate Tracking"),
        ("🛡", "Add VAMS Data"),
        ("📈", "Show Summary"),
        ("🧾", "Logs"),
        ("⚙️", "Settings"),
    ]

    def __init__(self, master, palette: dict, on_select):
        super().__init__(master, corner_radius=12, fg_color=palette["panel"], border_width=1, border_color=palette["border"])
        self.on_select = on_select
        self.buttons = {}
        for i, (icon, label) in enumerate(self.ITEMS):
            btn = ctk.CTkButton(self, text=f"{icon}  {label}", fg_color="transparent", hover_color=palette["secondary"], anchor="w", command=lambda name=label: self._select(name))
            btn.grid(row=i, column=0, sticky="ew", padx=8, pady=4)
            self.buttons[label] = btn
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(len(self.ITEMS), weight=1)

    def _select(self, name: str):
        for label, btn in self.buttons.items():
            btn.configure(fg_color=("#3b82f6" if label == name else "transparent"))
        self.on_select(name)
