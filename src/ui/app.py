"""Main Desktop Application Controller and View Router."""
import tkinter as tk
from typing import Optional, Dict, Any
from config.settings import settings
from src.core.logger import logger
from src.ui.styles import *
from src.ui.views import (
    LoginView,
    DashboardView,
    StudentView,
    ScannerView,
    AttendanceView,
    HelpView
)

class AttendanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(settings.APP_NAME)
        self.geometry("1280x780")
        self.minsize(1050, 680)
        self.configure(bg=BG_DARK)

        self.current_user: Optional[Dict[str, Any]] = None
        self.current_view: Optional[tk.Frame] = None

        # Container for swappable views
        self.container = tk.Frame(self, bg=BG_DARK)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.show_login()

    def clear_current_view(self):
        """Destroy existing view before loading a new one."""
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None

    def show_login(self):
        """Render the login screen."""
        self.clear_current_view()
        self.current_user = None
        self.current_view = LoginView(self.container, self.on_login_success)
        self.current_view.pack(fill=tk.BOTH, expand=True)

    def on_login_success(self, user_record: Dict[str, Any]):
        """Handle successful authentication."""
        self.current_user = user_record
        self.show_dashboard()

    def show_dashboard(self):
        """Render the main dashboard."""
        self.clear_current_view()
        self.current_view = DashboardView(
            self.container,
            self.current_user or {},
            self.navigate_to,
            self.show_login
        )
        self.current_view.pack(fill=tk.BOTH, expand=True)

    def navigate_to(self, view_name: str):
        """Route to specific modular view."""
        self.clear_current_view()

        if view_name == "dashboard":
            self.show_dashboard()
        elif view_name == "students":
            self.current_view = StudentView(self.container, self.navigate_to)
            self.current_view.pack(fill=tk.BOTH, expand=True)
        elif view_name == "scanner":
            self.current_view = ScannerView(self.container, self.navigate_to)
            self.current_view.pack(fill=tk.BOTH, expand=True)
        elif view_name == "attendance":
            self.current_view = AttendanceView(self.container, self.navigate_to)
            self.current_view.pack(fill=tk.BOTH, expand=True)
        elif view_name == "help":
            self.current_view = HelpView(self.container, self.navigate_to)
            self.current_view.pack(fill=tk.BOTH, expand=True)
        else:
            self.show_dashboard()

    def run(self):
        """Start the Tkinter event loop."""
        logger.info("Starting Attendance Management Desktop Application...")
        self.mainloop()
