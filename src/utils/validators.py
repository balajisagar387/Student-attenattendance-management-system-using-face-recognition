"""Input validation utilities."""
import re
from typing import Tuple

class Validator:
    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    PHONE_REGEX = re.compile(r"^\d{10}$")

    @classmethod
    def validate_name(cls, name: str, field_name: str = "Name") -> Tuple[bool, str]:
        if not name or not name.strip():
            return False, f"{field_name} cannot be empty."
        if any(char.isdigit() for char in name):
            return False, f"{field_name} must not contain numbers."
        if len(name.strip()) < 2:
            return False, f"{field_name} must be at least 2 characters."
        return True, ""

    @classmethod
    def validate_email(cls, email: str) -> Tuple[bool, str]:
        if not email or not email.strip():
            return False, "Email address is required."
        if not cls.EMAIL_REGEX.match(email.strip()):
            return False, "Please enter a valid email address (e.g. user@domain.com)."
        return True, ""

    @classmethod
    def validate_phone(cls, phone: str) -> Tuple[bool, str]:
        if not phone or not phone.strip():
            return False, "Phone number is required."
        clean_phone = re.sub(r"[\s\-\(\)]", "", phone)
        if not cls.PHONE_REGEX.match(clean_phone):
            return False, "Phone number must be exactly 10 digits."
        return True, ""

    @classmethod
    def validate_id(cls, identifier: str, field_name: str = "ID") -> Tuple[bool, str]:
        if not identifier or not identifier.strip():
            return False, f"{field_name} cannot be empty."
        if len(identifier.strip()) < 1:
            return False, f"{field_name} is too short."
        return True, ""

validators = Validator()
