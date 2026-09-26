"""Application configuration (ports, database credentials, upload rules)."""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    """Central configuration holder for the whole application."""

    SECRET_KEY = "alzikrayat-secret-key-change-me"
    PORT = 5000

    # "mysql" = production (PyMySQL, raw SQL) | "sqlite" = quick local run with no server
    DB_DRIVER = os.environ.get("DB_DRIVER", "sqlite")

    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = ""
    DB_NAME = "alzikrayat"
    SQLITE_PATH = os.path.join(BASE_DIR, "alzikrayat.db")

    UPLOAD_DIR = os.path.join(BASE_DIR, "app", "static", "uploads")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB per upload

    LAST_LOGIN_COOKIE = "lastLogin"
    LAST_LOGIN_COOKIE_DAYS = 7
