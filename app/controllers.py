# app/controllers.py
"""Flask route handlers for the Student Manager."""

from flask import Flask, render_template, request, redirect, url_for, flash, current_app, jsonify
from .repository import StudentRepository
from .services import StudentService
from sqlalchemy.exc import IntegrityError

def register_routes(app: Flask) -> None:
    """Register all routes on the provided Flask app."""
    @app.before_request
    def attach_service():
        # Attach repository & service instances to flask.g for request scope
        if not hasattr(current_app, "db_session"):
            raise RuntimeError("Database not initialized.")
        session = current_app.db_session()
        repo = StudentRepository(session)
        # store in app context (not a perfect pattern but simple)
        request.student_service = StudentService(repo)

    @app.teardown_request
    def remove_session(exc):
        # Remove scoped session at request end
        if hasattr(current_app, "db_session"):
            current_app.db_session.remove()

    @app.route("/", methods=["GET"])
    def index():
        """List students."""
        service: StudentService = request.student_service
        students = service.list_students()
        return render_template("index.html", students=students)

    @app.route("/students/new", methods=["GET", "POST"])
    def create_student():
        """Create student via form or JSON."""
        service: StudentService = request.student_service
        if request.method == "POST":
            payload = request.form.to_dict() if request.form else request.get_json(force=False) or {}
            try:
                student = service.create_student(payload)
                flash("Student created successfully.", "success")
                return redirect(url_for("index"))
            except ValueError as ve:
                flash(str(ve), "danger")
            except IntegrityError:
                flash("Enrollment number already exists.", "danger")
        return render_template("student_form.html", action="Create", student=None)

    @app.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
    def edit_student(student_id: int):
        service: StudentService = request.student_service
        try:
            student = service.get_student(student_id)
        except ValueError:
            flash("Student not found.", "warning")
            return redirect(url_for("index"))

        if request.method == "POST":
            payload = request.form.to_dict() if request.form else request.get_json(force=False) or {}
            try:
                service.update_student(student_id, payload)
                flash("Student updated successfully.", "success")
                return redirect(url_for("index"))
            except ValueError as ve:
                flash(str(ve), "danger")
            except IntegrityError:
                flash("Enrollment number already exists.", "danger")
        return render_template("student_form.html", action="Edit", student=student)

    @app.route("/students/<int:student_id>", methods=["GET"])
    def student_detail(student_id: int):
        service: StudentService = request.student_service
        try:
            student = service.get_student(student_id)
        except ValueError:
            flash("Student not found.", "warning")
            return redirect(url_for("index"))
        return render_template("student_detail.html", student=student)

    @app.route("/students/<int:student_id>/delete", methods=["POST"])
    def delete_student(student_id: int):
        service: StudentService = request.student_service
        try:
            service.delete_student(student_id)
            flash("Student deleted.", "success")
        except ValueError:
            flash("Student not found.", "warning")
        return redirect(url_for("index"))

    # Minimal JSON API endpoints for integration or tests
    @app.route("/api/students", methods=["GET", "POST"])
    def api_students():
        service: StudentService = request.student_service
        if request.method == "GET":
            students = service.list_students()
            return jsonify([_student_to_dict(s) for s in students])
        data = request.get_json() or {}
        try:
            student = service.create_student(data)
            return jsonify(_student_to_dict(student)), 201
        except ValueError as ve:
            return {"error": str(ve)}, 400
        except IntegrityError:
            return {"error": "enrollment_no must be unique"}, 400

    @app.route("/api/students/<int:student_id>", methods=["GET", "PUT", "DELETE"])
    def api_student_detail(student_id: int):
        service: StudentService = request.student_service
        if request.method == "GET":
            try:
                student = service.get_student(student_id)
                return jsonify(_student_to_dict(student))
            except ValueError:
                return {"error": "not found"}, 404
        if request.method == "PUT":
            payload = request.get_json() or {}
            try:
                student = service.update_student(student_id, payload)
                return jsonify(_student_to_dict(student))
            except ValueError as ve:
                return {"error": str(ve)}, 400
            except IntegrityError:
                return {"error": "enrollment_no must be unique"}, 400
        # DELETE
        try:
            service.delete_student(student_id)
            return {}, 204
        except ValueError:
            return {"error": "not found"}, 404

def _student_to_dict(s):
    return {
        "id": s.id,
        "enrollment_no": s.enrollment_no,
        "first_name": s.first_name,
        "last_name": s.last_name,
        "email": s.email,
        "course": s.course,
        "created_at": s.created_at.isoformat() if s.created_at else None,
        "updated_at": s.updated_at.isoformat() if s.updated_at else None,
    }
