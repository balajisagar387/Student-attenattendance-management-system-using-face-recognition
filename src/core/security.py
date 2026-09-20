"""Security utilities for salted cryptographic password hashing and verification."""
import hashlib
import os
import secrets

class SecurityManager:
    ALGORITHM = "sha256"
    ITERATIONS = 100_000

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Hash a password using PBKDF2-HMAC-SHA256 with a unique 16-byte salt."""
        salt = secrets.token_hex(16)
        key = hashlib.pbkdf2_hmac(
            cls.ALGORITHM,
            password.encode("utf-8"),
            salt.encode("utf-8"),
            cls.ITERATIONS
        )
        return f"{cls.ALGORITHM}${cls.ITERATIONS}${salt}${key.hex()}"

    @classmethod
    def verify_password(cls, plain_password: str, hashed: str) -> bool:
        """Verify a plain password against stored salted hash."""
        if not hashed or "$" not in hashed:
            # Fallback check for legacy plaintext if any exists during migration
            return plain_password == hashed

        try:
            algorithm, iterations_str, salt, stored_key = hashed.split("$")
            iterations = int(iterations_str)
            key = hashlib.pbkdf2_hmac(
                algorithm,
                plain_password.encode("utf-8"),
                salt.encode("utf-8"),
                iterations
            )
            return secrets.compare_digest(key.hex(), stored_key)
        except Exception:
            return False

security = SecurityManager()
