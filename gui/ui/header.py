from __future__ import annotations

import customtkinter as ctk


class HeaderPanel(ctk.CTkFrame):
    """Enterprise-grade hero header with clean layered styling."""

    def __init__(self, master, palette: dict, get_theme_name):
        super().__init__(
            master,
            corner_radius=20,
            fg_color=palette["panel"],
            border_width=1,
            border_color=palette.get("card_border", palette["border"]),
        )
        self.get_theme_name = get_theme_name
        self.status_var = ctk.StringVar(value="Ready")
        self.theme_var = ctk.StringVar(value=self.get_theme_name())

        self.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(
            self,
            text="🛡",
            width=64,
            height=64,
            corner_radius=32,
            fg_color=palette.get("blue_glow", palette["primary"]),
            text_color=palette["primary"],
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
        ).grid(row=0, column=0, rowspan=2, sticky="w", padx=(24, 16), pady=20)
        ctk.CTkLabel(
            self,
            text="Vulnerability Management Automation Tool",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color=palette["text"],
        ).grid(row=0, column=1, sticky="w", pady=(20, 0))
        ctk.CTkLabel(
            self,
            text="Automate vulnerability assessment & reporting with enterprise-grade clarity",
            text_color=palette.get("secondary_text", palette["muted"]),
            font=ctk.CTkFont(family="Segoe UI", size=13),
        ).grid(row=1, column=1, sticky="w", pady=(0, 20))
        decoration = ctk.CTkFrame(self, fg_color="transparent")
        decoration.grid(row=0, column=2, rowspan=2, sticky="e", padx=(0, 14))
        ctk.CTkLabel(
            decoration,
            text="••••••\n••••••\n••••••",
            text_color=palette.get("divider", palette["border"]),
            justify="right",
        ).pack(anchor="e")
        ctk.CTkFrame(
            decoration,
            width=86,
            height=8,
            corner_radius=4,
            fg_color=palette.get("mesh_blue", palette["primary"]),
        ).pack(anchor="e", pady=(8, 0))
        ctk.CTkFrame(
            decoration,
            width=56,
            height=8,
            corner_radius=4,
            fg_color=palette.get("mesh_purple", palette.get("purple", palette["primary"])),
        ).pack(anchor="e", pady=(6, 0))
        self.meta = ctk.CTkLabel(
            self,
            textvariable=self._meta_text(),
            text_color=palette["text"],
            fg_color=palette.get("card_alt", palette["panel"]),
            corner_radius=12,
            padx=16,
            pady=10,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
        )
        self.meta.grid(row=0, column=3, rowspan=2, sticky="e", padx=(0, 24))

    def _meta_text(self):
        var = ctk.StringVar()

        def refresh(*_):
            var.set(f"Theme: {self.theme_var.get()}   |   Run Status: ● {self.status_var.get()}")

        self.theme_var.trace_add("write", refresh)
        self.status_var.trace_add("write", refresh)
        refresh()
        return var
