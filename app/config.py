
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv("GENESIS_SECRET", "change-me-in-prod")
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'data' / 'gs_manager.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
