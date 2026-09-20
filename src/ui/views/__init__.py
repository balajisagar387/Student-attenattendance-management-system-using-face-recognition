"""Views package."""
from src.ui.views.login_view import LoginView
from src.ui.views.dashboard_view import DashboardView
from src.ui.views.student_view import StudentView
from src.ui.views.enrollment_view import EnrollmentView
from src.ui.views.scanner_view import ScannerView
from src.ui.views.attendance_view import AttendanceView
from src.ui.views.help_view import HelpView

__all__ = [
    "LoginView",
    "DashboardView",
    "StudentView",
    "EnrollmentView",
    "ScannerView",
    "AttendanceView",
    "HelpView"
]
