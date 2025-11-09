# run.py
"""Entrypoint for running Genesis Student Manager locally (development)."""

from app import create_app
from app.config import Config

def main():
    app = create_app(Config())
    app.run(host="0.0.0.0", port=5000, debug=app.config.get("DEBUG", False))

if __name__ == "__main__":
    main()
