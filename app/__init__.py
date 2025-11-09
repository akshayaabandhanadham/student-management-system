# app/__init__.py
"""
Application factory for Genesis Student Manager.
Creates and configures the Flask app and registers blueprints.
"""

from flask import Flask
from .config import Config
from .database import init_db
from .controllers import register_routes

def create_app(config_object: Config = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_object or Config())

    # Initialize extensions / database
    init_db(app)

    # Register controllers (routes)
    register_routes(app)

    # Simple health endpoint
    @app.route("/healthz")
    def healthz():
        return {"status": "ok"}, 200

    return app
