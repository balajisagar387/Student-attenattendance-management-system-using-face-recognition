"""Student domain service for CRUD operations and directory management."""
from typing import Dict, Any, List, Optional
from src.core.db import db
from src.core.logger import logger
from src.services.face_recognizer import face_recognizer_service

class StudentService:
    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        """Fetch all registered student records."""
        return db.fetch_all("SELECT * FROM students ORDER BY student_id ASC")

    @classmethod
    def get_by_id(cls, student_id: str) -> Optional[Dict[str, Any]]:
        """Fetch student by unique ID."""
        return db.fetch_one("SELECT * FROM students WHERE student_id = %s", (student_id,))

    @classmethod
    def create(cls, data: Dict[str, Any], embedding: Optional[bytes] = None) -> bool:
        """Create a new student record."""
        query = """
        INSERT INTO students (
            student_id, department, course, year, semester,
            name, division, roll_no, gender, dob, email,
            phone, address, teacher, photo_path, face_embedding
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data["student_id"],
            data.get("department", ""),
            data.get("course", ""),
            data.get("year", ""),
            data.get("semester", ""),
            data["name"],
            data.get("division", ""),
            data["roll_no"],
            data.get("gender", ""),
            data.get("dob", ""),
            data.get("email", ""),
            data.get("phone", ""),
            data.get("address", ""),
            data.get("teacher", ""),
            data.get("photo_path", ""),
            embedding
        )
        db.execute(query, params)
        face_recognizer_service.reload_enrolled_cache()
        return True

    @classmethod
    def update(cls, student_id: str, data: Dict[str, Any], embedding: Optional[bytes] = None) -> bool:
        """Update existing student details."""
        if embedding is not None:
            query = """
            UPDATE students SET
                department = %s, course = %s, year = %s, semester = %s,
                name = %s, division = %s, roll_no = %s, gender = %s,
                dob = %s, email = %s, phone = %s, address = %s,
                teacher = %s, photo_path = %s, face_embedding = %s
            WHERE student_id = %s
            """
            params = (
                data.get("department", ""),
                data.get("course", ""),
                data.get("year", ""),
                data.get("semester", ""),
                data["name"],
                data.get("division", ""),
                data["roll_no"],
                data.get("gender", ""),
                data.get("dob", ""),
                data.get("email", ""),
                data.get("phone", ""),
                data.get("address", ""),
                data.get("teacher", ""),
                data.get("photo_path", ""),
                embedding,
                student_id
            )
        else:
            query = """
            UPDATE students SET
                department = %s, course = %s, year = %s, semester = %s,
                name = %s, division = %s, roll_no = %s, gender = %s,
                dob = %s, email = %s, phone = %s, address = %s,
                teacher = %s
            WHERE student_id = %s
            """
            params = (
                data.get("department", ""),
                data.get("course", ""),
                data.get("year", ""),
                data.get("semester", ""),
                data["name"],
                data.get("division", ""),
                data["roll_no"],
                data.get("gender", ""),
                data.get("dob", ""),
                data.get("email", ""),
                data.get("phone", ""),
                data.get("address", ""),
                data.get("teacher", ""),
                student_id
            )

        db.execute(query, params)
        face_recognizer_service.reload_enrolled_cache()
        return True

    @classmethod
    def delete(cls, student_id: str) -> bool:
        """Delete student and their enrolled photo."""
        student = cls.get_by_id(student_id)
        if student and student.get("photo_path"):
            try:
                import os
                from config.settings import settings
                photo_file = settings.BASE_DIR / student["photo_path"]
                if photo_file.exists():
                    os.remove(photo_file)
            except Exception as e:
                logger.warning(f"Could not remove student photo file: {e}")

        db.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        face_recognizer_service.reload_enrolled_cache()
        return True

    @classmethod
    def search(cls, field: str, value: str) -> List[Dict[str, Any]]:
        """Search students by specific field."""
        allowed_fields = {"student_id", "roll_no", "name", "department", "course"}
        if field not in allowed_fields:
            field = "name"
        query = f"SELECT * FROM students WHERE {field} LIKE %s"
        return db.fetch_all(query, (f"%{value}%",))

student_service = StudentService()
