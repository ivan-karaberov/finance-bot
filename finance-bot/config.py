import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN", "")
TELEGRAM_ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID", "")

BASE_DIR = Path(__file__).resolve().parent
SQLITE_DB_FILE = BASE_DIR / "db.sqlite3"
INITIALIZATION_DB_FILE = BASE_DIR / "db.sql"
TEMPLATES_DIR = BASE_DIR / "templates"

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIMEZONE = "Europe/Moscow"
