"""Tab 2: Generate tracking by comparing required master and raw inputs."""

import customtkinter as ctk

from tabs.generate_tracking.logic import aggregate_unique, classify_new_old
from tabs.generate_tracking.excel_writer import write_output
from tabs.generate_tracking.excel_writer.formatting import apply_table_formatting
from tabs.generate_tracking.parser import parse_scan_file
from tabs.generate_tracking.excel_writer import (
    build_3uk_qualys_template_sheet_df,
    build_3uk_qualys_total_sheet_df,
    build_3uk_qualys_unique_sheet_df,
)
from utils.file_handler import list_excel_sheets, validate_file
from gui.qt_dialogs import DialogService
from gui.ui.themes import palette


class GenerateTrackingTab(ctk.CTkFrame):
    """Core workflow: parse -> compare -> aggregate -> write output."""
    def __init__(self, master, app_state, logger):
        super().__init__(master, fg_color="transparent")
        self.state = app_state
        self.logger = logger

        self.master_file = ctk.StringVar()
        self.master_sheet = ctk.StringVar()
        self.raw_file = ctk.StringVar()
        self.raw_sheet = ctk.StringVar()
        self.output_file = ctk.StringVar()
        self._entry_widgets = []
        self.dialogs = DialogService()
        self.colors = palette(self.state.get("theme_name", "Dark"))

        self._build_ui()
        self._bind_validation()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        combo_kwargs = {"corner_radius": 12, "height": 38, "fg_color": self.colors.get("input_bg", self.colors["panel"]), "border_color": self.colors.get("input_border", self.colors["border"]), "button_color": self.colors.get("button_blue", self.colors["primary"])}
        self.master_combo = ctk.CTkComboBox(self, values=[""], variable=self.master_sheet, **combo_kwargs)
        self.raw_combo = ctk.CTkComboBox(self, values=[""], variable=self.raw_sheet, **combo_kwargs)
        backend_text = f"Dialog backend: {self.dialogs.backend_name} (PySide/PyQt when available)"
        ctk.CTkLabel(self, text=backend_text, text_color=self.colors.get("light_blue", self.colors["primary"]), font=ctk.CTkFont(size=12)).grid(row=0, column=0, sticky="w", padx=16, pady=(6, 0))
        self._file_row(1, "📂 Master File (required)", self.master_file, self._browse_master)
        self.master_combo.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 10))
        self._file_row(3, "📊 Raw File", self.raw_file, self._browse_raw)
        self.raw_combo.grid(row=4, column=0, sticky="w", padx=16, pady=(0, 10))
        self._file_row(5, "📄 Output File", self.output_file, self._browse_output)
        self.run_btn = ctk.CTkButton(self, text="🛡  Run Assessment", command=self.run, height=42, corner_radius=12, fg_color=self.colors.get("run_button", self.colors.get("purple", self.colors["primary"])), hover_color=self.colors.get("purple_accent", self.colors.get("button_hover", self.colors["primary"])), font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"))
        self.run_btn.grid(row=6, column=0, sticky="e", padx=16, pady=14)
        self.form_status = ctk.CTkLabel(self, text="Fill required fields to enable Run", text_color=self.colors.get("warning", self.colors.get("orange", self.colors["primary"])), font=ctk.CTkFont(size=12, weight="bold"))
        self.form_status.grid(row=6, column=0, sticky="w", padx=16, pady=14)
        self.run_btn.configure(state="disabled")

    def _file_row(self, row, label, var, browse_command, save=False):
        card = ctk.CTkFrame(
            self,
            corner_radius=18,
            fg_color=self.colors.get("glass_bg", self.colors["panel"]),
            border_width=1,
            border_color=self.colors.get("glass_border", self.colors["border"]),
        )
        card.grid(row=row, column=0, sticky="ew", padx=16, pady=10)
        card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(card, text=label, text_color=self.colors["text"], font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold")).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 6))
        entry = ctk.CTkEntry(card, textvariable=var, corner_radius=12, height=38, fg_color=self.colors.get("input_bg", self.colors["panel"]), border_color=self.colors.get("input_border", self.colors["border"]))
        entry.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 14))
        self._entry_widgets.append(entry)
        ctk.CTkButton(card, text="📂  Browse", command=browse_command, width=140, height=38, corner_radius=12, fg_color=self.colors.get("button_blue", self.colors["primary"]), hover_color=self.colors.get("button_hover", self.colors["primary"])).grid(row=1, column=1, padx=(0, 16), pady=(0, 14))

    def _bind_validation(self):
        for var in (self.master_file, self.master_sheet, self.raw_file, self.raw_sheet, self.output_file):
            var.trace_add("write", lambda *_: self._validate_form())
        for entry in self._entry_widgets:
            entry.bind("<KeyRelease>", lambda _e: self._validate_form())
        self.master_combo.bind("<<ComboboxSelected>>", lambda _e: self._validate_form())
        self.raw_combo.bind("<<ComboboxSelected>>", lambda _e: self._validate_form())
        self._validate_form()

    def _validate_form(self):
        required_ok = bool(
            self.master_file.get().strip()
            and self.master_sheet.get().strip()
            and self.raw_file.get().strip()
            and self.raw_sheet.get().strip()
            and self.output_file.get().strip()
        )
        self.run_btn.configure(state="normal" if required_ok else "disabled")
        self.form_status.configure(
            text="Ready to run" if required_ok else "Select master, raw, sheets, and output to enable Run",
            text_color=self.colors.get("status_ready", self.colors.get("success", self.colors["primary"])) if required_ok else self.colors.get("warning", self.colors.get("orange", self.colors["primary"])),
        )
        return required_ok

    def _load_sheets(self, path, combo, var):
        sheets = list_excel_sheets(path)
        combo.configure(values=sheets or [""])
        if sheets:
            var.set(sheets[0])

    def _browse_master(self):
        path = self.dialogs.open_excel_file()
        if path:
            self.master_file.set(path)
            self._load_sheets(path, self.master_combo, self.master_sheet)

    def _browse_raw(self):
        path = self.dialogs.open_excel_file()
        if path:
            self.raw_file.set(path)
            self._load_sheets(path, self.raw_combo, self.raw_sheet)

    def _browse_output(self):
        path = self.dialogs.save_excel_file()
        if path:
            self.output_file.set(path)

    def _validate_inputs(self):
        if not self._validate_form():
            raise ValueError("Please select master file/sheet, raw file/sheet, and output file")
        validate_file(self.master_file.get())
        if not self.master_sheet.get():
            raise ValueError("Please select master sheet")
        validate_file(self.raw_file.get())
        if not self.raw_sheet.get():
            raise ValueError("Please select raw sheet")
        if not self.output_file.get():
            raise ValueError("Please select output file")

    def _parse_with_optional_severity_fallback(self, path: str, sheet: str, label: str):
        try:
            return parse_scan_file(path, sheet, self.state["selected_scanner"], self.state["selected_project"]).df
        except ValueError as exc:
            if "No rows left after severity filtering" not in str(exc):
                raise
            self.logger.warning(
                "%s has no rows after severity filtering; retrying without severity filter",
                label,
            )
            return parse_scan_file(
                path,
                sheet,
                self.state["selected_scanner"],
                self.state["selected_project"],
                require_rows_after_filter=False,
                apply_severity_filter=False,
            ).df


    def run(self):

        try:
            hooks = self.state.get("ui_hooks", {})
            hooks.get("set_run_state", lambda *_: None)("Running")
            hooks.get("set_stage", lambda *_: None)("Validate Inputs", 1)

            self.run_btn.configure(
                state="disabled"
            )

            self._validate_inputs()

            # -------------------------------------------------
            # PARSE RAW FILE
            # -------------------------------------------------

            hooks.get("set_stage", lambda *_: None)("Parse", 2)

            if (
                self.state["selected_project"].strip().casefold() == "3uk"
                and self.state["selected_scanner"].strip().casefold() == "qualys"
            ):
                raw_df = build_3uk_qualys_total_sheet_df(
                    self.raw_file.get(),
                    self.raw_sheet.get(),
                )

            else:

                raw_df = self._parse_with_optional_severity_fallback(
                    self.raw_file.get(),
                    self.raw_sheet.get(),
                    "Raw file",
                )

            # -------------------------------------------------
            # PARSE MASTER FILE
            # -------------------------------------------------

            if (
                self.state["selected_project"].strip().casefold() == "3uk"
                and self.state["selected_scanner"].strip().casefold() == "qualys"
            ):

                master_df = build_3uk_qualys_total_sheet_df(
                    self.master_file.get(),
                    self.master_sheet.get(),
                )

            else:

                master_df = self._parse_with_optional_severity_fallback(
                    self.master_file.get(),
                    self.master_sheet.get(),
                    "Master file",
                )
            # -------------------------------------------------
            # CLASSIFICATION
            # -------------------------------------------------
            hooks.get("set_stage", lambda *_: None)("Compare", 3)

            new_df, old_df = classify_new_old(
                raw_df,
                master_df,
            )
            if (
                self.state["selected_project"].strip().casefold() == "3uk"
                and self.state["selected_scanner"].strip().casefold() == "qualys"
            ):

                total_df = build_3uk_qualys_template_sheet_df(raw_df)
                new_df = build_3uk_qualys_template_sheet_df(new_df)
                old_df = build_3uk_qualys_template_sheet_df(old_df)
                unique_df = build_3uk_qualys_unique_sheet_df(raw_df)

            else:

                total_df = raw_df
                unique_df = aggregate_unique(raw_df)

            hooks.get("update_metrics", lambda **_: None)(
                total_vulns=len(raw_df),
                unique_vulns=len(unique_df),
            )


            # -------------------------------------------------
            # WRITE OUTPUT
            # -------------------------------------------------
            hooks.get("set_stage", lambda *_: None)("Write", 5)

            output = write_output(
                self.output_file.get(),
                new_df,
                old_df,
                unique_df,
                self.state["selected_project"],
                self.state["selected_scanner"],
                total_df=total_df,
            )

            # -------------------------------------------------
            # APPLY PROFESSIONAL FORMATTING
            # -------------------------------------------------

            from openpyxl import load_workbook

            from tabs.generate_tracking.excel_writer.formatting import apply_table_formatting

            wb = load_workbook(output)

            bordered_sheets = {
                "Total Vulnerabilities",
                "Unique Vulnerabilities",
                "New Vulnerabilities",
                "Old Vulnerabilities",
                "Total Data",
                "Unique Data",
            }
            for ws in wb.worksheets:
                apply_table_formatting(
                    ws,
                    include_borders=ws.title in bordered_sheets,
                )

            wb.save(output)

            wb.close()

            # -------------------------------------------------
            # SUCCESS LOGGING
            # -------------------------------------------------

            self.logger.info(
                "Tracking sheet created: %s",
                output,
            )

            self.state["last_output_file"] = output
            self.dialogs.show_info(
                "Success",
                f"Tracking sheet created:\n{output}",
            )
            hooks.get("set_run_state", lambda *_: None)("Success")

        except Exception as exc:

            self.logger.exception(
                "Update Tracking Sheet failed"
            )

            self.dialogs.show_error(
                "Error",
                str(exc),
            )
            hooks.get("set_run_state", lambda *_: None)("Failed")

        finally:

            self._validate_form()



    def reset(self):
        for var in (self.master_file, self.master_sheet, self.raw_file, self.raw_sheet, self.output_file):
            var.set("")
        self.master_combo.configure(values=[""])
        self.raw_combo.configure(values=[""])
        self._validate_form()
