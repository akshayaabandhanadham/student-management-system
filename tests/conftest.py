# tests/conftest.py
"""Pytest fixtures for the app."""

import os
import tempfile
import pytest
from app import create_app
from app.config import Config
from app.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

class TestConfig(Config):
    TESTING = True
    DEBUG = False
    # Use a temporary sqlite DB for tests
    SQLALCHEMY_DATABASE_URI = ""

@pytest.fixture(scope="session")
def tmp_db_file():
    fd, path = tempfile.mkstemp(prefix="test_gs_", suffix=".db")
    os.close(fd)
    yield path
    try:
        os.remove(path)
    except OSError:
        pass

@pytest.fixture()
def app(tmp_db_file):
    # Create a config with sqlite file path
    cfg = TestConfig()
    cfg.SQLALCHEMY_DATABASE_URI = f"sqlite:///{tmp_db_file}"
    app = create_app(cfg)
    # Ensure fresh DB
    Base.metadata.drop_all(bind=app.db_engine)
    Base.metadata.create_all(bind=app.db_engine)
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
