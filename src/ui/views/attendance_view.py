"""Attendance Log, Auditing, and CSV Export View."""
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Callable, List, Dict, Any
from config.settings import settings
from config.constants import DEPARTMENTS
from src.services.attendance_service import attendance_service
from src.ui.styles import *

class AttendanceView(tk.Frame):
    def __init__(self, master, navigate_to: Callable[[str], None]):
        super().__init__(master, bg=BG_DARK)
        self.master = master
        self.navigate_to = navigate_to
        self.current_records: List[Dict[str, Any]] = []
        self.build_ui()
        self.load_records()

    def build_ui(self):
        # 1. Header Bar
        header = tk.Frame(self, bg=BG_CARD, height=60, padx=25)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        title = tk.Label(header, text="Attendance Records & Reporting", font=FONT_SUBTITLE, fg=TEXT_PRIMARY, bg=BG_CARD)
        title.pack(side=tk.LEFT, pady=15)

        back_btn = tk.Button(header, text="<- Back to Dashboard", font=FONT_BODY, bg=THEME_PRIMARY, fg=TEXT_PRIMARY,
                             bd=0, cursor="hand2", padx=15, pady=4, command=lambda: self.navigate_to("dashboard"))
        back_btn.pack(side=tk.RIGHT, pady=15)

        # 2. Main Body
        body = tk.Frame(self, bg=BG_DARK, padx=20, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        # Top Control Bar (Search + Actions)
        top_bar = tk.Frame(body, bg=BG_CARD, bd=1, relief=tk.SOLID, padx=15, pady=12)
        top_bar.pack(fill=tk.X, pady=(0, 15))

        tk.Label(top_bar, text="Search By:", font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_CARD).pack(side=tk.LEFT, padx=(0, 8))
        self.search_field = ttk.Combobox(top_bar, values=["name", "student_id", "roll_no", "department", "log_date"], state="readonly", width=14)
        self.search_field.current(0)
        self.search_field.pack(side=tk.LEFT, padx=(0, 8))

        self.search_entry = tk.Entry(top_bar, font=FONT_BODY, bg=BG_CARD_LIGHT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, bd=1, relief=tk.FLAT)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=3)

        tk.Button(top_bar, text="Search", font=FONT_SMALL, bg=THEME_PRIMARY, fg=TEXT_PRIMARY,
                  bd=0, cursor="hand2", padx=12, pady=4, command=self.execute_search).pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(top_bar, text="Reset / All", font=FONT_SMALL, bg=BG_CARD_LIGHT, fg=TEXT_PRIMARY,
                  bd=0, cursor="hand2", padx=10, pady=4, command=self.load_records).pack(side=tk.LEFT, padx=(0, 15))

        # Export & Delete Actions
        tk.Button(top_bar, text="Export to CSV", font=FONT_BODY_BOLD, bg=THEME_SUCCESS, fg=TEXT_PRIMARY,
                  bd=0, cursor="hand2", padx=14, pady=4, command=self.export_csv).pack(side=tk.RIGHT, padx=4)
        tk.Button(top_bar, text="Delete Selected", font=FONT_SMALL, bg=THEME_DANGER, fg=TEXT_PRIMARY,
                  bd=0, cursor="hand2", padx=10, pady=4, command=self.delete_selected).pack(side=tk.RIGHT, padx=4)

        # Table Container
        table_card = tk.Frame(body, bg=BG_CARD, bd=1, relief=tk.SOLID, padx=15, pady=15)
        table_card.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "student_id", "roll_no", "name", "department", "time", "date", "status")
        self.tree = ttk.Treeview(table_card, columns=columns, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("student_id", text="Student ID")
        self.tree.heading("roll_no", text="Roll No")
        self.tree.heading("name", text="Student Name")
        self.tree.heading("department", text="Department")
        self.tree.heading("time", text="Timestamp")
        self.tree.heading("date", text="Date")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=50)
        self.tree.column("student_id", width=100)
        self.tree.column("roll_no", width=80)
        self.tree.column("name", width=160)
        self.tree.column("department", width=180)
        self.tree.column("time", width=100)
        self.tree.column("date", width=100)
        self.tree.column("status", width=90)

        scroll_y = ttk.Scrollbar(table_card, orient=tk.VERTICAL, command=self.tree.yview)
        scroll_x = ttk.Scrollbar(table_card, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Bottom summary bar
        self.summary_lbl = tk.Label(body, text="Total Records: 0", font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_DARK)
        self.summary_lbl.pack(anchor="w", pady=(8, 0))

    def load_records(self, records=None):
        self.tree.delete(*self.tree.get_children())
        if records is None:
            records = attendance_service.get_all()

        self.current_records = records
        for r in records:
            self.tree.insert("", tk.END, values=(
                r.get("id"),
                r.get("student_id"),
                r.get("roll_no"),
                r.get("name"),
                r.get("department"),
                r.get("log_time"),
                r.get("log_date"),
                r.get("status")
            ))
        self.summary_lbl.config(text=f"Total Records Displayed: {len(records)}")

    def execute_search(self):
        field = self.search_field.get()
        query = self.search_entry.get().strip()
        if not query:
            self.load_records()
            return
        results = attendance_service.search(field, query)
        self.load_records(results)

    def delete_selected(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a record from the table to delete.", parent=self.master)
            return
        vals = self.tree.item(selected, "values")
        if not vals:
            return
        rec_id = int(vals[0])
        if messagebox.askyesno("Confirm Delete", f"Delete attendance log #{rec_id} for {vals[3]}?", parent=self.master):
            attendance_service.delete(rec_id)
            self.load_records()
            messagebox.showinfo("Success", "Attendance record deleted.", parent=self.master)

    def export_csv(self):
        if not self.current_records:
            messagebox.showerror("Export", "No records available to export.", parent=self.master)
            return

        date_str = datetime.now().strftime("%Y-%m-%d")
        default_name = f"attendance_export_{date_str}.csv"
        file_path = filedialog.asksaveasfilename(
            initialfile=default_name,
            defaultextension=".csv",
            filetypes=[("CSV Spreadsheet", "*.csv"), ("All Files", "*.*")],
            parent=self.master
        )
        if not file_path:
            return

        try:
            attendance_service.export_to_csv(Path(file_path), self.current_records)
            messagebox.showinfo("Export Successful", f"Saved {len(self.current_records)} records to:\n{file_path}", parent=self.master)
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not export file: {e}", parent=self.master)
