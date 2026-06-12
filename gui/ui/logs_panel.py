from __future__ import annotations
import customtkinter as ctk


class LogsPanel(ctk.CTkFrame):
    def __init__(self, master, palette: dict, open_output_command=None):
        super().__init__(
            master,
            corner_radius=20,
            fg_color=palette.get("glass_bg", palette["panel"]),
            border_width=1,
            border_color=palette.get("glass_border", palette.get("card_border", palette["border"])),
        )
        self.palette = palette
        self.search_var = ctk.StringVar()
        self.open_output_command = open_output_command
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=16, pady=(12, 6))
        ctk.CTkLabel(
            top,
            text="● Live Logs",
            text_color=palette.get("status_ready", palette.get("green", "#22C55E")),
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
        ).pack(side="left")
        ctk.CTkLabel(top, text="INFO SUCCESS WARNING ERROR", text_color=palette.get("muted", palette["text"]), font=ctk.CTkFont(size=11)).pack(side="right")
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(fill="x", padx=16, pady=(2, 8))
        ctk.CTkEntry(
            controls,
            textvariable=self.search_var,
            placeholder_text="Search logs...",
            fg_color=palette.get("input_bg", palette["panel"]),
            border_color=palette.get("input_border", palette["border"]),
            corner_radius=12,
            height=38,
        ).pack(side="left", fill="x", expand=True, padx=(0, 8))
        ctk.CTkButton(
            controls,
            text="📂  Open Output",
            width=170,
            height=38,
            corner_radius=12,
            fg_color=palette.get("button_blue", palette["primary"]),
            hover_color=palette.get("button_hover", palette["primary"]),
            command=self._open_output_file,
        ).pack(side="left", padx=3)
        self.text = ctk.CTkTextbox(
            self,
            height=128,
            font=("Consolas", 11),
            fg_color=palette.get("log_bg", palette["panel"]),
            text_color=palette["text"],
            border_color=palette.get("divider", palette.get("border", "#334155")),
            border_width=1,
            corner_radius=14,
        )
        self.text.pack(fill="both", expand=True, padx=16, pady=(0, 14))

    def append(self, msg: str):
        badge = "INFO"
        upper = msg.upper()
        if "ERROR" in upper or "FAILED" in upper:
            badge = "ERROR"
        elif "WARNING" in upper or "WARN" in upper:
            badge = "WARNING"
        elif "SUCCESS" in upper or "COMPLETED" in upper:
            badge = "SUCCESS"
        self.text.insert("end", f"[{badge}] {msg}\n")
        self.text.see("end")

    def _open_output_file(self):
        if self.open_output_command:
            self.open_output_command()
