from __future__ import annotations
import customtkinter as ctk


class SummaryCards(ctk.CTkFrame):
    """Premium KPI cards with accent icons and lightweight sparkline patterns."""

    SPARKLINES = ["▁▃▅▆▇", "▂▆▅▇▆", "▁▄▇▅▇", "▃▅▂▆▇"]

    def __init__(self, master, palette: dict):
        super().__init__(master, fg_color="transparent")
        self.cards = {}
        self.tags = {}
        card_specs = [
            ("Vulnerabilities Processed", "🛡", "Total sheet count: {value}", palette["primary"]),
            ("Unique Vulnerabilities", "☑", "Unique sheet count: {value}", palette.get("success", palette["green"])),
            ("Processing Time", "◷", "Elapsed time: {value}", palette.get("purple", palette["secondary"])),
            ("Success Rate", "↗", "Completion: {value}", palette.get("orange", palette["secondary"])),
        ]
        for i, (name, icon, tag_template, accent) in enumerate(card_specs):
            card = ctk.CTkFrame(
                self,
                corner_radius=18,
                fg_color=palette["panel"],
                border_width=1,
                border_color=palette.get("card_border", palette["border"]),
            )
            card.grid(row=0, column=i, sticky="nsew", padx=8, pady=(4, 0))
            self.grid_columnconfigure(i, weight=1)
            value = ctk.StringVar(value="0")
            tag = ctk.StringVar(value=tag_template.format(value="0"))

            top = ctk.CTkFrame(card, fg_color="transparent")
            top.pack(fill="x", padx=16, pady=(16, 8))
            ctk.CTkLabel(
                top,
                text=icon,
                width=54,
                height=54,
                corner_radius=27,
                fg_color=accent,
                text_color=palette.get("dark_active_text", "#FFFFFF"),
                font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            ).pack(side="left", padx=(0, 12))
            text = ctk.CTkFrame(top, fg_color="transparent")
            text.pack(side="left", fill="both", expand=True)
            ctk.CTkLabel(
                text,
                text=name,
                text_color=palette["text"],
                font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            ).pack(anchor="w")
            ctk.CTkLabel(
                text,
                textvariable=value,
                font=ctk.CTkFont(family="Segoe UI", size=30, weight="bold"),
                text_color=accent,
            ).pack(anchor="w", pady=(2, 0))

            footer = ctk.CTkFrame(card, fg_color="transparent")
            footer.pack(fill="x", padx=16, pady=(0, 14))
            ctk.CTkLabel(
                footer,
                textvariable=tag,
                text_color=palette.get("secondary_text", palette["muted"]),
                font=ctk.CTkFont(family="Segoe UI", size=12),
            ).pack(side="left")
            ctk.CTkLabel(
                footer,
                text=self.SPARKLINES[i],
                text_color=accent,
                font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            ).pack(side="right")
            self.cards[name] = value
            self.tags[name] = (tag, tag_template)

    def update_metrics(self, **values):
        for k, v in values.items():
            if k in self.cards:
                value = str(v)
                self.cards[k].set(value)
                tag, template = self.tags[k]
                tag.set(template.format(value=value))
