"""Unified Database Manager supporting SQLite (embedded default) and MySQL."""
import sqlite3
from typing import Any, List, Optional, Tuple, Dict
from config.settings import settings
from src.core.logger import logger

class DatabaseManager:
    def __init__(self):
        self.db_type = settings.DB_TYPE
        self.init_schema()

    def get_connection(self):
        """Yield a database connection based on active configuration."""
        if self.db_type == "mysql":
            try:
                import mysql.connector
                conn = mysql.connector.connect(
                    host=settings.MYSQL_HOST,
                    port=settings.MYSQL_PORT,
                    user=settings.MYSQL_USER,
                    password=settings.MYSQL_PASSWORD,
                    database=settings.MYSQL_DATABASE
                )
                return conn
            except Exception as e:
                logger.error(f"MySQL connection failed: {e}. Falling back to SQLite.")
                self.db_type = "sqlite"

        # Default SQLite
        conn = sqlite3.connect(str(settings.SQLITE_PATH), timeout=20.0)
        conn.row_factory = sqlite3.Row
        return conn

    def _convert_query(self, query: str) -> str:
        """Ensure parameter placeholder compatibility (%s for MySQL, ? for SQLite)."""
        if self.db_type == "sqlite":
            return query.replace("%s", "?")
        return query

    def execute(self, query: str, params: Tuple = ()) -> int:
        """Execute an INSERT, UPDATE, or DELETE query and return affected rows."""
        conn = self.get_connection()
        converted_query = self._convert_query(query)
        try:
            cursor = conn.cursor()
            cursor.execute(converted_query, params)
            conn.commit()
            last_id = cursor.lastrowid
            cursor.close()
            return last_id or 1
        except Exception as e:
            logger.error(f"DB Execute Error on '{query}': {e}")
            conn.rollback()
            raise e
        finally:
            conn.close()

    def fetch_one(self, query: str, params: Tuple = ()) -> Optional[Dict[str, Any]]:
        """Fetch a single record as a dictionary."""
        conn = self.get_connection()
        converted_query = self._convert_query(query)
        try:
            cursor = conn.cursor()
            cursor.execute(converted_query, params)
            row = cursor.fetchone()
            if not row:
                return None
            if hasattr(cursor, "column_names"): # MySQL
                columns = cursor.column_names
                return dict(zip(columns, row))
            # SQLite
            return dict(row)
        finally:
            conn.close()

    def fetch_all(self, query: str, params: Tuple = ()) -> List[Dict[str, Any]]:
        """Fetch all records matching query as dictionaries."""
        conn = self.get_connection()
        converted_query = self._convert_query(query)
        try:
            cursor = conn.cursor()
            cursor.execute(converted_query, params)
            rows = cursor.fetchall()
            if not rows:
                return []
            if hasattr(cursor, "column_names"): # MySQL
                columns = cursor.column_names
                return [dict(zip(columns, r)) for r in rows]
            # SQLite
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def init_schema(self):
        """Create tables if they do not exist."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Schema commands (compatible across SQLite and MySQL)
        if self.db_type == "sqlite":
            queries = [
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT NOT NULL,
                    security_question TEXT NOT NULL,
                    security_answer_hash TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS students (
                    student_id TEXT PRIMARY KEY,
                    department TEXT NOT NULL,
                    course TEXT NOT NULL,
                    year TEXT NOT NULL,
                    semester TEXT NOT NULL,
                    name TEXT NOT NULL,
                    division TEXT,
                    roll_no TEXT NOT NULL,
                    gender TEXT,
                    dob TEXT,
                    email TEXT,
                    phone TEXT,
                    address TEXT,
                    teacher TEXT,
                    photo_path TEXT,
                    face_embedding BLOB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    roll_no TEXT NOT NULL,
                    name TEXT NOT NULL,
                    department TEXT NOT NULL,
                    log_time TEXT NOT NULL,
                    log_date TEXT NOT NULL,
                    status TEXT DEFAULT 'Present',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            ]
        else: # MySQL
            queries = [
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    phone VARCHAR(20) NOT NULL,
                    security_question VARCHAR(200) NOT NULL,
                    security_answer_hash VARCHAR(256) NOT NULL,
                    password_hash VARCHAR(256) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """,
                """
                CREATE TABLE IF NOT EXISTS students (
                    student_id VARCHAR(50) PRIMARY KEY,
                    department VARCHAR(100) NOT NULL,
                    course VARCHAR(50) NOT NULL,
                    year VARCHAR(20) NOT NULL,
                    semester VARCHAR(20) NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    division VARCHAR(20),
                    roll_no VARCHAR(50) NOT NULL,
                    gender VARCHAR(20),
                    dob VARCHAR(30),
                    email VARCHAR(100),
                    phone VARCHAR(20),
                    address TEXT,
                    teacher VARCHAR(100),
                    photo_path VARCHAR(255),
                    face_embedding LONGBLOB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """,
                """
                CREATE TABLE IF NOT EXISTS attendance (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id VARCHAR(50) NOT NULL,
                    roll_no VARCHAR(50) NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    department VARCHAR(100) NOT NULL,
                    log_time VARCHAR(20) NOT NULL,
                    log_date VARCHAR(20) NOT NULL,
                    status VARCHAR(20) DEFAULT 'Present',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """
            ]

        try:
            for q in queries:
                cursor.execute(q)
            conn.commit()
            logger.info("Database schema initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize database schema: {e}")
        finally:
            cursor.close()
            conn.close()

db = DatabaseManager()
