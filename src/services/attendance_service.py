"""Attendance service for logging, duplicate prevention, and CSV operations."""
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from config.settings import settings
from src.core.db import db
from src.core.logger import logger

class AttendanceService:
    @classmethod
    def mark_attendance(cls, student_id: str, roll_no: str, name: str, department: str) -> bool:
        """Record attendance with daily duplicate protection."""
        now = datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        time_str = now.strftime("%H:%M:%S")

        # Check if already marked present today
        existing = db.fetch_one(
            "SELECT id FROM attendance WHERE student_id = %s AND log_date = %s",
            (student_id, date_str)
        )
        if existing:
            return False # Already recorded today

        # 1. Save to Database
        query = """
        INSERT INTO attendance (student_id, roll_no, name, department, log_time, log_date, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'Present')
        """
        db.execute(query, (student_id, roll_no, name, department, time_str, date_str))

        # 2. Mirror to daily CSV audit log
        cls._append_to_daily_csv(student_id, roll_no, name, department, time_str, date_str)
        return True

    @classmethod
    def _append_to_daily_csv(cls, student_id: str, roll_no: str, name: str, department: str, time_str: str, date_str: str):
        """Append record to daily CSV backup."""
        try:
            iso_date = datetime.now().strftime("%Y-%m-%d")
            csv_file = settings.ATTENDANCE_DIR / f"attendance_{iso_date}.csv"
            is_new = not csv_file.exists()

            with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if is_new:
                    writer.writerow(["StudentID", "RollNo", "Name", "Department", "Time", "Date", "Status"])
                writer.writerow([student_id, roll_no, name, department, time_str, date_str, "Present"])
        except Exception as e:
            logger.error(f"Failed to append to daily CSV: {e}")

    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        """Fetch all attendance records ordered by latest first."""
        return db.fetch_all("SELECT * FROM attendance ORDER BY id DESC")

    @classmethod
    def search(cls, field: str, value: str) -> List[Dict[str, Any]]:
        """Search attendance records."""
        allowed_fields = {"student_id", "roll_no", "name", "department", "log_date", "status"}
        if field not in allowed_fields:
            field = "student_id"
        query = f"SELECT * FROM attendance WHERE {field} LIKE %s ORDER BY id DESC"
        return db.fetch_all(query, (f"%{value}%",))

    @classmethod
    def delete(cls, attendance_id: int) -> bool:
        """Delete an attendance record."""
        db.execute("DELETE FROM attendance WHERE id = %s", (attendance_id,))
        return True

    @classmethod
    def export_to_csv(cls, target_path: Path, records: Optional[List[Dict[str, Any]]] = None) -> bool:
        """Export attendance records to a CSV file."""
        if records is None:
            records = cls.get_all()

        try:
            with open(target_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["AttendanceID", "StudentID", "RollNo", "Name", "Department", "Time", "Date", "Status"])
                for r in records:
                    writer.writerow([
                        r.get("id"),
                        r.get("student_id"),
                        r.get("roll_no"),
                        r.get("name"),
                        r.get("department"),
                        r.get("log_time"),
                        r.get("log_date"),
                        r.get("status")
                    ])
            return True
        except Exception as e:
            logger.error(f"Failed to export CSV to {target_path}: {e}")
            raise e

attendance_service = AttendanceService()
