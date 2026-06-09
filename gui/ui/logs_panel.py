from __future__ import annotations
import customtkinter as ctk


class LogsPanel(ctk.CTkFrame):
    def __init__(self, master, palette: dict, open_output_command=None):
        super().__init__(master, corner_radius=12, fg_color=palette["panel"], border_width=1, border_color=palette["border"])
        self.search_var = ctk.StringVar()
        self.open_output_command = open_output_command
        ctk.CTkLabel(self, text="● Live Logs", text_color="#22c55e").pack(anchor="w", padx=10, pady=(6, 0))
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(fill="x", padx=10, pady=(4, 4))
        ctk.CTkEntry(controls, textvariable=self.search_var, placeholder_text="Search logs...").pack(side="left", fill="x", expand=True, padx=(0, 8))
        ctk.CTkButton(
            controls,
            text="📂 Open Output File",
            width=150,
            command=self._open_output_file,
        ).pack(side="left", padx=3)
        self.text = ctk.CTkTextbox(self, height=120, font=("Consolas", 11), fg_color="#0b1020")
        self.text.pack(fill="both", expand=True, padx=10, pady=(0, 8))

    def append(self, msg: str):
        self.text.insert("end", msg + "\n")
        self.text.see("end")

    def _open_output_file(self):
        if self.open_output_command:
            self.open_output_command()
