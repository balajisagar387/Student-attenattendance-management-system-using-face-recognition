"""Central application settings with environment variable support."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env if present
load_dotenv(BASE_DIR / ".env")

class Settings:
    # Application Metadata
    APP_NAME: str = os.getenv("APP_NAME", "Face Attendance Management System")
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

    # Directory Paths
    BASE_DIR: Path = BASE_DIR
    BASE_PATH: Path = BASE_DIR
    DATA_DIR: Path = BASE_DIR / "data"
    STUDENTS_DIR: Path = BASE_DIR / "data" / "students"
    ATTENDANCE_DIR: Path = BASE_DIR / "data" / "attendance"
    ASSETS_DIR: Path = BASE_DIR / "college_images"  # Preserving existing image assets
    DOCS_DIR: Path = BASE_DIR / "docs"

    # Database Settings
    DB_TYPE: str = os.getenv("DB_TYPE", "sqlite").lower()
    SQLITE_PATH: Path = BASE_DIR / os.getenv("SQLITE_PATH", "data/attendance_system.db")

    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "student_management")

    # Camera & Vision Thresholds
    CAMERA_INDEX: int = int(os.getenv("CAMERA_INDEX", "0"))
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.60"))
    DETECTION_CONFIDENCE: float = float(os.getenv("DETECTION_CONFIDENCE", "0.50"))

    # Pose Guidance Limits (Degrees)
    MAX_YAW_ANGLE: float = 16.0     # Horizontal look angle limit
    MAX_PITCH_ANGLE: float = 16.0   # Vertical tilt limit
    MAX_ROLL_ANGLE: float = 14.0    # Sideways slant limit
    MIN_FACE_SCALE: float = 0.18    # Minimum face size (allows comfortable zoomed-out distance)
    MAX_FACE_SCALE: float = 0.75    # Maximum face size
    MIN_LAPLACIAN_VAR: float = 25.0 # Blurriness threshold suited for laptop webcams

    # UI Theme
    UI_THEME: str = os.getenv("UI_THEME", "Dark")
    UI_COLOR_THEME: str = os.getenv("UI_COLOR_THEME", "blue")

    def __init__(self):
        # Ensure directories exist
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.STUDENTS_DIR.mkdir(parents=True, exist_ok=True)
        self.ATTENDANCE_DIR.mkdir(parents=True, exist_ok=True)

settings = Settings()
