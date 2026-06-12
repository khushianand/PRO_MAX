from __future__ import annotations
import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    ITEMS = [
        ("⌂", "Dashboard"),
        ("▣", "Make Report"),
        ("▧", "Generate Tracking"),
        ("🛡", "Add VAMS Data"),
        ("↗", "Show Summary"),
        ("☷", "Logs"),
        ("⚙", "Settings"),
    ]

    def __init__(self, master, palette: dict, on_select):
        super().__init__(
            master,
            corner_radius=20,
            fg_color=palette.get("sidebar_bg", palette["panel"]),
            border_width=1,
            border_color=palette.get("glass_border", palette.get("card_border", palette["border"])),
            width=220,
        )
        self.palette = palette
        self.on_select = on_select
        self.buttons = {}
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False)

        ctk.CTkLabel(
            self,
            text="VMAT",
            text_color=palette["primary"],
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(18, 8))
        ctk.CTkFrame(
            self,
            height=1,
            fg_color=palette.get("glass_highlight", palette.get("divider", palette["border"])),
        ).grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 10))

        for i, (icon, label) in enumerate(self.ITEMS, start=2):
            btn = ctk.CTkButton(
                self,
                text=f"{icon}  {label}",
                fg_color="transparent",
                hover_color=palette.get("nav_hover", palette["secondary"]),
                text_color=palette["text"],
                anchor="w",
                corner_radius=12,
                height=42,
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                command=lambda name=label: self._select(name),
            )
            btn.grid(row=i, column=0, sticky="ew", padx=12, pady=4)
            self.buttons[label] = btn

        self.grid_rowconfigure(len(self.ITEMS) + 2, weight=1)
        ctk.CTkLabel(
            self,
            text="Stronger today,\nSafer tomorrow.",
            text_color=palette.get("muted", palette["text"]),
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            justify="center",
        ).grid(row=len(self.ITEMS) + 3, column=0, sticky="s", padx=16, pady=(16, 20))

    def _select(self, name: str):
        active_text = self.palette.get("dark_active_text", "#FFFFFF") if self.palette.get("sidebar_active") == "#2D5FAE" else self.palette.get("primary", self.palette["text"])
        for label, btn in self.buttons.items():
            active = label == name
            btn.configure(
                fg_color=(self.palette.get("sidebar_active", self.palette["secondary"]) if active else "transparent"),
                text_color=(active_text if active else self.palette["text"]),
            )
        self.on_select(name)
