from __future__ import annotations
import customtkinter as ctk


class WorkflowStepper(ctk.CTkFrame):
    STEPS = ["Inputs", "Parse", "Compare", "Enrich", "Write"]

    def __init__(self, master, palette: dict):
        super().__init__(master, corner_radius=12, fg_color=palette["panel"], border_width=1, border_color=palette["border"])
        self.palette = palette
        self.labels = []
        for i, step in enumerate(self.STEPS):
            lbl = ctk.CTkLabel(self, text=f"○ {step}")
            lbl.grid(row=0, column=i * 2, padx=(8, 2), pady=8, sticky="w")
            self.labels.append(lbl)
            if i < len(self.STEPS) - 1:
                ctk.CTkLabel(self, text="────", text_color="#475569").grid(row=0, column=i * 2 + 1, sticky="ew")

    def set_active(self, step_name: str):
        try:
            active_idx = self.STEPS.index(step_name)
        except ValueError:
            active_idx = -1
        for i, lbl in enumerate(self.labels):
            if i < active_idx:
                lbl.configure(text=f"✔ {self.STEPS[i]}", text_color="#00c896")
            elif i == active_idx:
                lbl.configure(text=f"◉ {self.STEPS[i]}", text_color="#3b82f6")
            else:
                lbl.configure(text=f"○ {self.STEPS[i]}", text_color="#9ca3af")
