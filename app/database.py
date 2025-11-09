
from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from typing import Optional

Base = declarative_base()
_DB_SESSION = None

def init_db(app):
    """
    Initialize database engine and create a scoped session factory available
    as current_app.db_session. Also creates tables if they do not exist.
    """
    global _DB_SESSION
    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], future=True)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    _DB_SESSION = scoped_session(session_factory)
    app.db_engine = engine
    app.db_session = _DB_SESSION

    # Import models here to ensure they are registered with Base.metadata
    from . import models  # noqa: F401

    # Create tables if missing
    Base.metadata.create_all(bind=engine)

def get_db_session():
    """Return the scoped session; raises if not initialized."""
    if _DB_SESSION is None:
        raise RuntimeError("Database not initialized. Call init_db(app) first.")
    return _DB_SESSION
