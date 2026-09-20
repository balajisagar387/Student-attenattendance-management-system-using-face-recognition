"""Modern Student Management and Academic Directory View."""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional, Dict, Any
from pathlib import Path
from config.constants import *
from config.settings import settings
from src.services.student_service import student_service
from src.utils.validators import validators
from src.utils.image_utils import image_utils
from src.ui.styles import *
from src.ui.views.enrollment_view import EnrollmentView

class StudentView(tk.Frame):
    def __init__(self, master, navigate_to: Callable[[str], None]):
        super().__init__(master, bg=BG_DARK)
        self.master = master
        self.navigate_to = navigate_to
        self.current_photo_path = None
        self.form_entries = {}
        self.build_ui()
        self.load_students_table()

    def build_ui(self):
        # 1. Header Bar
        header = tk.Frame(self, bg=BG_CARD, height=60, padx=25)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        title = tk.Label(header, text="Student Directory & Profile Management", font=FONT_SUBTITLE, fg=TEXT_PRIMARY, bg=BG_CARD)
        title.pack(side=tk.LEFT, pady=15)

        back_btn = tk.Button(header, text="<- Back to Dashboard", font=FONT_BODY, bg=THEME_PRIMARY, fg=TEXT_PRIMARY,
                             bd=0, cursor="hand2", padx=15, pady=4, command=lambda: self.navigate_to("dashboard"))
        back_btn.pack(side=tk.RIGHT, pady=15)

        # 2. Main Body: Split View (Left: Form, Right: Directory Table)
        body = tk.Frame(self, bg=BG_DARK, padx=20, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        # Left Column: Form Card
        left_card = tk.Frame(body, bg=BG_CARD, bd=1, relief=tk.SOLID, padx=20, pady=20, width=480)
        left_card.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        left_card.pack_propagate(False)

        self.build_student_form(left_card)

        # Right Column: Directory Table & Search
        right_card = tk.Frame(body, bg=BG_CARD, bd=1, relief=tk.SOLID, padx=20, pady=20)
        right_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.build_directory_table(right_card)

    def build_student_form(self, parent):
        tk.Label(parent, text="Student Academic Profile", font=FONT_BODY_BOLD, fg=THEME_PRIMARY, bg=BG_CARD).pack(anchor="w", pady=(0, 10))

        # Photo Preview Row
        photo_box = tk.Frame(parent, bg=BG_CARD_LIGHT, height=120, bd=1, relief=tk.SOLID)
        photo_box.pack(fill=tk.X, pady=(0, 10))

        self.photo_lbl = tk.Label(photo_box, text="No Photo Enrolled", font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_CARD_LIGHT)
        self.photo_lbl.pack(side=tk.LEFT, padx=15, pady=10)

        photo_actions = tk.Frame(photo_box, bg=BG_CARD_LIGHT)
        photo_actions.pack(side=tk.RIGHT, padx=15, pady=15)

        enroll_btn = tk.Button(photo_actions, text="Capture Photo (Guided) ->", font=FONT_SMALL, bg=THEME_SUCCESS, fg=TEXT_PRIMARY,
                               bd=0, cursor="hand2", padx=10, pady=6, command=self.open_enrollment_window)
        enroll_btn.pack(fill=tk.X)

        self.photo_status_lbl = tk.Label(photo_actions, text="Status: Unregistered", font=FONT_SMALL, fg=THEME_WARNING, bg=BG_CARD_LIGHT)
        self.photo_status_lbl.pack(pady=(5, 0))

        # Academic Fields
        form_scroll = tk.Frame(parent, bg=BG_CARD)
        form_scroll.pack(fill=tk.BOTH, expand=True)

        fields = [
            ("Student ID (Unique)", "student_id", "entry"),
            ("Full Name", "name", "entry"),
            ("Roll Number", "roll_no", "entry"),
            ("Department", "department", "combo", DEPARTMENTS),
            ("Course", "course", "combo", COURSES),
            ("Academic Year", "year", "combo", ACADEMIC_YEARS),
            ("Semester", "semester", "combo", SEMESTERS),
            ("Class Division", "division", "combo", DIVISIONS),
            ("Gender", "gender", "combo", GENDERS),
            ("Email Address", "email", "entry"),
            ("Contact Phone (10 digits)", "phone", "entry"),
            ("Mentor / Teacher", "teacher", "entry"),
        ]

        # 2-column compact grid
        for i, item in enumerate(fields):
            label_text, key, ftype = item[0], item[1], item[2]
            r = i // 2
            c = (i % 2) * 2

            tk.Label(form_scroll, text=label_text, font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_CARD).grid(row=r*2, column=c, sticky="w", padx=4, pady=(4, 0))
            if ftype == "entry":
                e = tk.Entry(form_scroll, font=FONT_SMALL, bg=BG_CARD_LIGHT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, bd=1, relief=tk.FLAT)
                e.grid(row=r*2+1, column=c, sticky="ew", padx=4, pady=(2, 6), ipady=3)
                self.form_entries[key] = e
            elif ftype == "combo":
                values = item[3]
                cb = ttk.Combobox(form_scroll, values=values, state="readonly", font=FONT_SMALL)
                cb.current(0)
                cb.grid(row=r*2+1, column=c, sticky="ew", padx=4, pady=(2, 6), ipady=1)
                self.form_entries[key] = cb

        form_scroll.columnconfigure(0, weight=1)
        form_scroll.columnconfigure(2, weight=1)

        # Action Buttons
        btn_bar = tk.Frame(parent, bg=BG_CARD)
        btn_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))

        tk.Button(btn_bar, text="Save / Add", font=FONT_BODY_BOLD, bg=THEME_SUCCESS, fg=TEXT_PRIMARY,
                  bd=0, cursor="hand2", padx=12, pady=6, command=self.save_student).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        tk.Button(btn_bar, text="Update", font=FONT_BODY_BOLD, bg=THEME_PRIMARY, fg=TEXT_PRIMARY,
                  bd=0, cursor="hand2", padx=12, pady=6, command=self.update_student).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        tk.Button(btn_bar, text="Delete", font=FONT_BODY_BOLD, bg=THEME_DANGER, fg=TEXT_PRIMARY,
                  bd=0, cursor="hand2", padx=12, pady=6, command=self.delete_student).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        tk.Button(btn_bar, text="Clear", font=FONT_BODY, bg=BG_CARD_LIGHT, fg=TEXT_PRIMARY,
                  bd=0, cursor="hand2", padx=10, pady=6, command=self.clear_form).pack(side=tk.LEFT, padx=2)

    def build_directory_table(self, parent):
        # Search controls
        search_bar = tk.Frame(parent, bg=BG_CARD)
        search_bar.pack(fill=tk.X, pady=(0, 15))

        tk.Label(search_bar, text="Search By:", font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_CARD).pack(side=tk.LEFT, padx=(0, 8))
        self.search_combo = ttk.Combobox(search_bar, values=["student_id", "roll_no", "name", "department"], state="readonly", width=14)
        self.search_combo.current(2)
        self.search_combo.pack(side=tk.LEFT, padx=(0, 8))

        self.search_entry = tk.Entry(search_bar, font=FONT_BODY, bg=BG_CARD_LIGHT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, bd=1, relief=tk.FLAT)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=3)

        tk.Button(search_bar, text="Search", font=FONT_SMALL, bg=THEME_PRIMARY, fg=TEXT_PRIMARY,
                  bd=0, cursor="hand2", padx=12, pady=4, command=self.execute_search).pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(search_bar, text="Show All", font=FONT_SMALL, bg=BG_CARD_LIGHT, fg=TEXT_PRIMARY,
                  bd=0, cursor="hand2", padx=10, pady=4, command=self.load_students_table).pack(side=tk.LEFT)

        # Table Container
        table_frame = tk.Frame(parent, bg=BG_CARD)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("student_id", "name", "roll_no", "department", "course", "year", "phone", "photo")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.heading("student_id", text="Student ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("roll_no", text="Roll No")
        self.tree.heading("department", text="Department")
        self.tree.heading("course", text="Course")
        self.tree.heading("year", text="Year")
        self.tree.heading("phone", text="Phone")
        self.tree.heading("photo", text="Photo")

        self.tree.column("student_id", width=90)
        self.tree.column("name", width=140)
        self.tree.column("roll_no", width=80)
        self.tree.column("department", width=140)
        self.tree.column("course", width=70)
        self.tree.column("year", width=70)
        self.tree.column("phone", width=90)
        self.tree.column("photo", width=70)

        # Scrollbars
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind("<ButtonRelease-1>", self.on_table_select)

    def load_students_table(self, records=None):
        self.tree.delete(*self.tree.get_children())
        if records is None:
            records = student_service.get_all()

        for r in records:
            has_photo = "Yes" if r.get("photo_path") else "No"
            self.tree.insert("", tk.END, values=(
                r.get("student_id"),
                r.get("name"),
                r.get("roll_no"),
                r.get("department"),
                r.get("course"),
                r.get("year"),
                r.get("phone"),
                has_photo
            ))

    def on_table_select(self, event=None):
        selected = self.tree.focus()
        if not selected:
            return
        vals = self.tree.item(selected, "values")
        if not vals:
            return
        student_id = vals[0]
        student = student_service.get_by_id(student_id)
        if not student:
            return

        # Populate form
        for key, widget in self.form_entries.items():
            val = student.get(key, "")
            if isinstance(widget, ttk.Combobox):
                if val in widget["values"]:
                    widget.set(val)
            else:
                widget.delete(0, tk.END)
                widget.insert(0, str(val or ""))

        # Preview photo
        self.current_photo_path = student.get("photo_path")
        if self.current_photo_path:
            full_path = settings.BASE_DIR / self.current_photo_path
            img = image_utils.load_and_resize(full_path, (90, 90))
            if img:
                self.photo_lbl.config(image=img, text="")
                self.photo_lbl.image = img
                self.photo_status_lbl.config(text="✓ Enrolled (Single Photo)", fg=THEME_SUCCESS)
                return

        self.photo_lbl.config(image="", text="No Photo Enrolled")
        self.photo_lbl.image = None
        self.photo_status_lbl.config(text="⚠ Photo Missing", fg=THEME_WARNING)

    def open_enrollment_window(self):
        s_id = self.form_entries["student_id"].get().strip()
        s_name = self.form_entries["name"].get().strip()
        if not s_id or not s_name:
            messagebox.showerror("Error", "Please enter Student ID and Name before taking photo.", parent=self.master)
            return

        EnrollmentView(self.master, s_id, s_name, self.on_photo_enrolled_callback)

    def on_photo_enrolled_callback(self, photo_path: str):
        self.current_photo_path = photo_path
        full_path = settings.BASE_DIR / photo_path
        img = image_utils.load_and_resize(full_path, (90, 90))
        if img:
            self.photo_lbl.config(image=img, text="")
            self.photo_lbl.image = img
            self.photo_status_lbl.config(text="✓ Enrolled (Single Photo)", fg=THEME_SUCCESS)
        self.load_students_table()

    def get_form_data(self) -> Dict[str, Any]:
        data = {k: v.get().strip() if hasattr(v, "get") else "" for k, v in self.form_entries.items()}
        data["photo_path"] = self.current_photo_path or ""
        return data

    def save_student(self):
        data = self.get_form_data()
        ok, err = validators.validate_id(data["student_id"], "Student ID")
        if not ok:
            messagebox.showerror("Validation Error", err, parent=self.master)
            return
        ok, err = validators.validate_name(data["name"], "Student Name")
        if not ok:
            messagebox.showerror("Validation Error", err, parent=self.master)
            return
        ok, err = validators.validate_id(data["roll_no"], "Roll Number")
        if not ok:
            messagebox.showerror("Validation Error", err, parent=self.master)
            return

        try:
            student_service.create(data)
            messagebox.showinfo("Success", f"Student {data['name']} added successfully!", parent=self.master)
            self.load_students_table()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save student: {e}", parent=self.master)

    def update_student(self):
        data = self.get_form_data()
        s_id = data["student_id"]
        if not s_id:
            messagebox.showerror("Error", "Select a student to update.", parent=self.master)
            return
        try:
            student_service.update(s_id, data)
            messagebox.showinfo("Success", "Student details updated successfully!", parent=self.master)
            self.load_students_table()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to update: {e}", parent=self.master)

    def delete_student(self):
        s_id = self.form_entries["student_id"].get().strip()
        if not s_id:
            messagebox.showerror("Error", "Select a student to delete.", parent=self.master)
            return
        if messagebox.askyesno("Confirm Delete", f"Delete student record {s_id}?", parent=self.master):
            try:
                student_service.delete(s_id)
                messagebox.showinfo("Deleted", "Student record deleted successfully.", parent=self.master)
                self.clear_form()
                self.load_students_table()
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete: {e}", parent=self.master)

    def clear_form(self):
        for widget in self.form_entries.values():
            if isinstance(widget, ttk.Combobox):
                widget.current(0)
            else:
                widget.delete(0, tk.END)
        self.current_photo_path = None
        self.photo_lbl.config(image="", text="No Photo Enrolled")
        self.photo_lbl.image = None
        self.photo_status_lbl.config(text="Status: Unregistered", fg=TEXT_MUTED)

    def execute_search(self):
        field = self.search_combo.get()
        query = self.search_entry.get().strip()
        if not query:
            self.load_students_table()
            return
        results = student_service.search(field, query)
        self.load_students_table(results)
