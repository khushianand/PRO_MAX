from __future__ import annotations

import customtkinter as ctk


class HeaderPanel(ctk.CTkFrame):
    def __init__(self, master, palette: dict, get_theme_name):
        super().__init__(master, corner_radius=12, fg_color=palette["panel"], border_width=1, border_color=palette["border"])
        self.get_theme_name = get_theme_name
        self.status_var = ctk.StringVar(value="Ready")
        self.theme_var = ctk.StringVar(value=self.get_theme_name())

        self.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self, text="🛡 Vulnerability Management Automation Suite", font=ctk.CTkFont(size=18, weight="bold"), text_color=palette["text"]).grid(row=0, column=0, sticky="w", padx=12, pady=(8, 0))
        ctk.CTkLabel(self, text="Enterprise Vulnerability Processing Platform  •  v2.0", text_color=palette["secondary"]).grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))
        self.meta = ctk.CTkLabel(self, textvariable=self._meta_text(), text_color=palette["text"])
        self.meta.grid(row=0, column=1, rowspan=2, sticky="e", padx=12)

    def _meta_text(self):
        var = ctk.StringVar()
        def refresh(*_):
            var.set(f"Theme: {self.theme_var.get()}   |   Run Status: {self.status_var.get()}")
        self.theme_var.trace_add("write", refresh)
        self.status_var.trace_add("write", refresh)
        refresh()
        return var
