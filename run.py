#!/usr/bin/env python3
"""
Student Attendance Management System
Main Entrypoint Script
"""
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.logger import logger
from src.ui.app import AttendanceApp

def main():
    try:
        app = AttendanceApp()
        app.run()
    except Exception as e:
        logger.critical(f"Unhandled application exception: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
