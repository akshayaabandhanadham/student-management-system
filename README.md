# Genesis Student Manager

Genesis Student Manager is a lightweight, production-minded student management web application written in Python using Flask and SQLAlchemy. It provides full CRUD operations (Create, Read, Update, Delete) for student records and demonstrates a clear separation of concerns (database, repository, service, controllers) and simple UI templates.

## Features
- Create, list, view, edit and delete student records
- Input validation and unique constraint on enrollment number
- Simple HTML UI (Jinja2 templates) and minimal CSS
- JSON API endpoints for automation or integrations
- Unit/integration tests using `pytest`
- Designed for easy extension to PostgreSQL, REST auth, or containerization

## Prerequisites
- Python 3.10 or higher
- Git (optional)
- Virtual environment tool (recommended): `python -m venv` or `venv`

## Setup & Installation

```bash
# Clone the repository
git clone <repo-url> genesis-student-manager
cd genesis-student-manager

# Create and activate virtual environment (Unix)
python -m venv .venv
source .venv/bin/activate

# (Windows PowerShell)
# python -m venv .venv
# .venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the app (development)
python run.py
