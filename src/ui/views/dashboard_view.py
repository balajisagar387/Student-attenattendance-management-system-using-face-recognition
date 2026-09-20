"""Modern Dashboard View with navigation cards and live statistics."""
import time
from datetime import datetime
import tkinter as tk
from typing import Callable, Dict, Any
from config.settings import settings
from src.core.db import db
from src.ui.styles import *

class DashboardView(tk.Frame):
    def __init__(self, master, current_user: Dict[str, Any], navigate_to: Callable[[str], None], logout_callback: Callable[[], None]):
        super().__init__(master, bg=BG_DARK)
        self.master = master
        self.current_user = current_user
        self.navigate_to = navigate_to
        self.logout_callback = logout_callback
        self.clock_id = None
        self.build_ui()

    def build_ui(self):
        # 1. Top Header Bar
        header = tk.Frame(self, bg=BG_CARD, height=70, padx=25)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        # Title & User
        title_box = tk.Frame(header, bg=BG_CARD)
        title_box.pack(side=tk.LEFT, fill=tk.Y, pady=12)

        app_title = tk.Label(title_box, text=settings.APP_NAME, font=FONT_SUBTITLE, fg=TEXT_PRIMARY, bg=BG_CARD)
        app_title.pack(anchor="w")

        user_name = f"{self.current_user.get('first_name', '')} {self.current_user.get('last_name', '')}".strip() or "Administrator"
        user_lbl = tk.Label(title_box, text=f"Logged in as: {user_name}", font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_CARD)
        user_lbl.pack(anchor="w")

        # Right side: Clock & Logout
        right_box = tk.Frame(header, bg=BG_CARD)
        right_box.pack(side=tk.RIGHT, fill=tk.Y, pady=15)

        self.clock_lbl = tk.Label(right_box, text="", font=FONT_BODY_BOLD, fg=THEME_SUCCESS, bg=BG_CARD)
        self.clock_lbl.pack(side=tk.LEFT, padx=(0, 20))
        self.update_clock()

        logout_btn = tk.Button(right_box, text="Log Out", font=FONT_SMALL, bg=THEME_DANGER, fg=TEXT_PRIMARY,
                               bd=0, cursor="hand2", padx=12, pady=4, command=self.logout_callback)
        logout_btn.pack(side=tk.RIGHT)

        # 2. Main Action Cards Container
        content = tk.Frame(self, bg=BG_DARK, padx=40, pady=40)
        content.pack(fill=tk.BOTH, expand=True)

        cards_data = [
            ("Student Directory", "Enroll students, view academic profiles, and capture guided face photos.",
             THEME_PRIMARY, lambda: self.navigate_to("students")),
            ("Live Attendance Scanner", "Launch camera for real-time 60 FPS face recognition & attendance logging.",
             THEME_SUCCESS, lambda: self.navigate_to("scanner")),
            ("Attendance Records", "Browse logs, filter by date or department, and export reports to CSV/Excel.",
             THEME_WARNING, lambda: self.navigate_to("attendance")),
            ("System SOPs & Help", "View architecture docs, troubleshooting SOPs, and developer guidelines.",
             "#6c5ce7", lambda: self.navigate_to("help")),
        ]

        # 2x2 Grid
        content.columnconfigure(0, weight=1, uniform="col")
        content.columnconfigure(1, weight=1, uniform="col")
        content.rowconfigure(0, weight=1, uniform="row")
        content.rowconfigure(1, weight=1, uniform="row")

        for idx, (title, desc, color, action) in enumerate(cards_data):
            row = idx // 2
            col = idx % 2
            self.create_card(content, row, col, title, desc, color, action)

        # 3. Footer Statistics Bar
        footer = tk.Frame(self, bg=BG_CARD, height=40, padx=25)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)

        stats_text = self.get_quick_stats()
        stats_lbl = tk.Label(footer, text=stats_text, font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_CARD)
        stats_lbl.pack(side=tk.LEFT, pady=10)

        docs_tip = tk.Label(footer, text="Documentation & SOPs: docs/ folder", font=FONT_SMALL, fg=THEME_PRIMARY, bg=BG_CARD)
        docs_tip.pack(side=tk.RIGHT, pady=10)

    def create_card(self, parent, row, col, title, desc, color, action):
        card = tk.Frame(parent, bg=BG_CARD, bd=1, relief=tk.SOLID, padx=25, pady=25)
        card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

        indicator = tk.Frame(card, bg=color, height=4)
        indicator.pack(fill=tk.X, side=tk.TOP, pady=(0, 15))

        tk.Label(card, text=title, font=FONT_SUBTITLE, fg=TEXT_PRIMARY, bg=BG_CARD, anchor="w").pack(fill=tk.X)
        tk.Label(card, text=desc, font=FONT_BODY, fg=TEXT_MUTED, bg=BG_CARD, wraplength=320, justify=tk.LEFT, anchor="w").pack(fill=tk.X, pady=(10, 20))

        btn = tk.Button(card, text=f"Open {title} ->", font=FONT_BODY_BOLD, bg=color, fg=TEXT_PRIMARY,
                        bd=0, cursor="hand2", pady=8, command=action)
        btn.pack(fill=tk.X, side=tk.BOTTOM)

    def update_clock(self):
        now_str = datetime.now().strftime("%I:%M:%S %p | %A, %b %d, %Y")
        if self.winfo_exists():
            self.clock_lbl.config(text=now_str)
            self.clock_id = self.after(1000, self.update_clock)

    def get_quick_stats(self) -> str:
        try:
            total_students = db.fetch_one("SELECT COUNT(*) as count FROM students")
            s_count = total_students["count"] if total_students else 0
            today_str = datetime.now().strftime("%d/%m/%Y")
            today_att = db.fetch_one("SELECT COUNT(*) as count FROM attendance WHERE log_date = %s", (today_str,))
            a_count = today_att["count"] if today_att else 0
            return f"System Online  |  Enrolled Students: {s_count}  |  Today's Attendance Count: {a_count}  |  Storage: {settings.DB_TYPE.upper()}"
        except Exception:
            return "System Ready"
