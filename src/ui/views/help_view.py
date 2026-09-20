"""System Documentation & Developer Support View."""
import os
import tkinter as tk
from typing import Callable
from config.settings import settings
from src.ui.styles import *

class HelpView(tk.Frame):
    def __init__(self, master, navigate_to: Callable[[str], None]):
        super().__init__(master, bg=BG_DARK)
        self.master = master
        self.navigate_to = navigate_to
        self.build_ui()

    def build_ui(self):
        # 1. Header Bar
        header = tk.Frame(self, bg=BG_CARD, height=60, padx=25)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        title = tk.Label(header, text="System Standard Operating Procedures & Help", font=FONT_SUBTITLE, fg=TEXT_PRIMARY, bg=BG_CARD)
        title.pack(side=tk.LEFT, pady=15)

        back_btn = tk.Button(header, text="<- Back to Dashboard", font=FONT_BODY, bg=THEME_PRIMARY, fg=TEXT_PRIMARY,
                             bd=0, cursor="hand2", padx=15, pady=4, command=lambda: self.navigate_to("dashboard"))
        back_btn.pack(side=tk.RIGHT, pady=15)

        # 2. Main Content
        body = tk.Frame(self, bg=BG_DARK, padx=30, pady=30)
        body.pack(fill=tk.BOTH, expand=True)

        card = tk.Frame(body, bg=BG_CARD, bd=1, relief=tk.SOLID, padx=30, pady=30)
        card.pack(fill=tk.BOTH, expand=True)

        tk.Label(card, text="Standard Operating Procedures (docs/ directory)", font=FONT_SUBTITLE, fg=THEME_SUCCESS, bg=BG_CARD, anchor="w").pack(fill=tk.X)

        sops = [
            ("SOP-01: System Architecture & Design", "01_SYSTEM_ARCHITECTURE.md", "High-level overview of UI, services, and models."),
            ("SOP-02: Installation & Environment Setup", "02_INSTALLATION_AND_SETUP.md", "Step-by-step installation for Windows, macOS, and Linux."),
            ("SOP-03: Database Management", "03_DATABASE_MANAGEMENT.md", "Switching between SQLite and MySQL, schema, and backups."),
            ("SOP-04: Security & User Access", "04_SECURITY_AND_USER_ACCESS.md", "User registration, password hashing, and recovery."),
            ("SOP-05: Student Enrollment Guidelines", "05_STUDENT_ENROLLMENT_GUIDELINES.md", "Pose guidance, single photo criteria, and best practices."),
            ("SOP-06: Attendance Scanner Operations", "06_ATTENDANCE_SCANNER_OPERATIONS.md", "Operating the live camera recognition scanner."),
            ("SOP-07: Reporting & Data Export", "07_REPORTING_AND_DATA_EXPORT.md", "Auditing attendance logs and exporting to CSV."),
            ("SOP-08: Troubleshooting & FAQ", "08_TROUBLESHOOTING_AND_FAQ.md", "Diagnosing camera, database, and lighting issues."),
        ]

        sop_list_frame = tk.Frame(card, bg=BG_CARD)
        sop_list_frame.pack(fill=tk.BOTH, expand=True, pady=15)

        for title_text, filename, desc in sops:
            row = tk.Frame(sop_list_frame, bg=BG_CARD_LIGHT, padx=12, pady=8, bd=1, relief=tk.SOLID)
            row.pack(fill=tk.X, pady=4)

            tk.Label(row, text=title_text, font=FONT_BODY_BOLD, fg=TEXT_PRIMARY, bg=BG_CARD_LIGHT).pack(side=tk.LEFT)
            tk.Label(row, text=f"- {desc}", font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_CARD_LIGHT).pack(side=tk.LEFT, padx=10)

        # Developer info footer
        footer = tk.Frame(card, bg=BG_CARD)
        footer.pack(fill=tk.X, side=tk.BOTTOM, pady=(15, 0))

        tk.Label(footer, text="Modernized Attendance Management Platform v2.0", font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_CARD).pack(side=tk.LEFT)
        tk.Label(footer, text="Lead Developers: Balaji Birajdar, Aradhya Telkhade, Abhishek Patil", font=FONT_SMALL, fg=THEME_PRIMARY, bg=BG_CARD).pack(side=tk.RIGHT)
