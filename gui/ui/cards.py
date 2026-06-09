from __future__ import annotations
import customtkinter as ctk


class SummaryCards(ctk.CTkFrame):
    def __init__(self, master, palette: dict):
        super().__init__(master, fg_color="transparent")
        self.cards = {}
        self.tags = {}
        card_specs = [
            ("Vulnerabilities Processed", "🛡", "Total sheet count: {value}"),
            ("Unique Vulnerabilities", "🧩", "Unique sheet count: {value}"),
            ("Processing Time", "⏱", "Elapsed time: {value}"),
            ("Success Rate", "📈", "Completion: {value}"),
        ]
        for i, (name, icon, tag_template) in enumerate(card_specs):
            card = ctk.CTkFrame(self, corner_radius=12, fg_color=palette["panel"], border_width=1, border_color=palette["border"])
            card.grid(row=0, column=i, sticky="nsew", padx=6, pady=2)
            self.grid_columnconfigure(i, weight=1)
            value = ctk.StringVar(value="0")
            tag = ctk.StringVar(value=tag_template.format(value="0"))
            ctk.CTkLabel(card, text=f"{icon} {name}", text_color=palette["text"]).pack(anchor="w", padx=10, pady=(6, 1))
            ctk.CTkLabel(card, textvariable=value, font=ctk.CTkFont(size=30, weight="bold"), text_color=palette["primary"]).pack(anchor="w", padx=10, pady=(0, 1))
            ctk.CTkLabel(card, textvariable=tag, text_color=palette["secondary"]).pack(anchor="w", padx=10, pady=(0, 6))
            self.cards[name] = value
            self.tags[name] = (tag, tag_template)

    def update_metrics(self, **values):
        for k, v in values.items():
            if k in self.cards:
                value = str(v)
                self.cards[k].set(value)
                tag, template = self.tags[k]
                tag.set(template.format(value=value))
