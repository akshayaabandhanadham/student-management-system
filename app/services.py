

from typing import Dict, Tuple, List
from sqlalchemy.exc import IntegrityError
from .repository import StudentRepository
from .schemas import validate_student_payload
from .models import Student

class StudentService:
    """Service containing student-related business logic."""

    def __init__(self, repo: StudentRepository):
        self.repo = repo

    def list_students(self) -> List[Student]:
        """Return all students."""
        return self.repo.list_all()

    def get_student(self, student_id: int) -> Student:
        """Get a student or raise ValueError if not found."""
        student = self.repo.get_by_id(student_id)
        if student is None:
            raise ValueError(f"Student id={student_id} not found.")
        return student

    def create_student(self, payload: Dict) -> Student:
        """Validate payload and create a student. Raises ValueError or IntegrityError."""
        ok, err = validate_student_payload(payload)
        if not ok:
            raise ValueError(err)

        try:
            return self.repo.create(
                enrollment_no=payload["enrollment_no"].strip(),
                first_name=payload["first_name"].strip(),
                last_name=(payload.get("last_name") or "").strip(),
                email=(payload.get("email") or "").strip(),
                course=(payload.get("course") or "").strip(),
            )
        except IntegrityError as e:
            # Re-raise with friendly message
            raise IntegrityError(
                statement=e.statement, params=e.params, orig=Exception("Enrollment number must be unique.")
            )

    def update_student(self, student_id: int, payload: Dict) -> Student:
        """Update an existing student after validation."""
        # Simpler validation: ensure required fields if provided are correct types
        ok, err = validate_student_payload({**payload, "enrollment_no": payload.get("enrollment_no", "x"), "first_name": payload.get("first_name", "x")})  # type: ignore
        if not ok:
            # If user intends partial update, we allow missing fields — but keep basic checks
            # For clarity, only block on bad types
            if err and "required" in err:
                # allow partial updates, so ignore missing required fields
                pass
            else:
                raise ValueError(err)

        student = self.repo.get_by_id(student_id)
        if student is None:
            raise ValueError("Student not found.")
        update_fields = {}
        for field in ("enrollment_no", "first_name", "last_name", "email", "course"):
            if field in payload and payload[field] is not None:
                update_fields[field] = payload[field].strip() if isinstance(payload[field], str) else payload[field]
        try:
            return self.repo.update(student, **update_fields)
        except IntegrityError as e:
            raise IntegrityError(
                statement=e.statement, params=e.params, orig=Exception("Enrollment number must be unique.")
            )

    def delete_student(self, student_id: int) -> None:
        """Delete student by id."""
        student = self.repo.get_by_id(student_id)
        if student is None:
            raise ValueError("Student not found.")
        self.repo.delete(student)
