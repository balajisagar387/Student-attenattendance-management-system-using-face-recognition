"""User authentication and security administration service."""
from typing import Dict, Any, Optional, Tuple
from src.core.db import db
from src.core.security import security
from src.core.logger import logger

class AuthService:
    @classmethod
    def register_user(cls, data: Dict[str, str]) -> Tuple[bool, str]:
        """Register a new staff/admin user."""
        email = data["email"].strip().lower()

        # Check existing
        existing = db.fetch_one("SELECT id FROM users WHERE email = %s", (email,))
        if existing:
            return False, "An account with this email address already exists."

        pw_hash = security.hash_password(data["password"])
        ans_hash = security.hash_password(data["security_answer"].strip().lower())

        query = """
        INSERT INTO users (first_name, last_name, email, phone, security_question, security_answer_hash, password_hash)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data["first_name"].strip(),
            data["last_name"].strip(),
            email,
            data["phone"].strip(),
            data["security_question"],
            ans_hash,
            pw_hash
        )
        db.execute(query, params)
        logger.info(f"User registered successfully: {email}")
        return True, "Registration successful."

    @classmethod
    def authenticate(cls, email: str, password: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        """Authenticate user credentials."""
        user = db.fetch_one("SELECT * FROM users WHERE email = %s", (email.strip().lower(),))
        if not user:
            return False, None, "Invalid email address or password."

        stored_hash = user.get("password_hash", "")
        if not security.verify_password(password, stored_hash):
            return False, None, "Invalid email address or password."

        return True, user, "Login successful."

    @classmethod
    def get_security_question(cls, email: str) -> Tuple[bool, Optional[str]]:
        """Retrieve security question for email."""
        user = db.fetch_one("SELECT security_question FROM users WHERE email = %s", (email.strip().lower(),))
        if not user:
            return False, None
        return True, user.get("security_question")

    @classmethod
    def reset_password(cls, email: str, answer: str, new_password: str) -> Tuple[bool, str]:
        """Reset password via verified security answer."""
        user = db.fetch_one("SELECT * FROM users WHERE email = %s", (email.strip().lower(),))
        if not user:
            return False, "User not found."

        stored_ans_hash = user.get("security_answer_hash", "")
        if not security.verify_password(answer.strip().lower(), stored_ans_hash):
            return False, "Incorrect security answer provided."

        new_hash = security.hash_password(new_password)
        db.execute("UPDATE users SET password_hash = %s WHERE email = %s", (new_hash, email.strip().lower()))
        logger.info(f"Password reset completed for: {email}")
        return True, "Password has been reset successfully."

auth_service = AuthService()
