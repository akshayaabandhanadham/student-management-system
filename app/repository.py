

from typing import List, Optional
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session
from .models import Student

class StudentRepository:
    """Repository for Student model."""

    def __init__(self, session: Session):
        self.session = session

    def list_all(self) -> List[Student]:
        """Return all students ordered by id descending."""
        return self.session.query(Student).order_by(Student.id.desc()).all()

    def get_by_id(self, student_id: int) -> Optional[Student]:
        """Return a student by id or None."""
        return self.session.query(Student).filter(Student.id == student_id).one_or_none()

    def get_by_enrollment(self, enrollment_no: str) -> Optional[Student]:
        """Return a student by enrollment number or None."""
        return (
            self.session.query(Student)
            .filter(Student.enrollment_no == enrollment_no)
            .one_or_none()
        )

    def create(self, **kwargs) -> Student:
        """Create and persist a Student. Raises IntegrityError if duplicate enrollment_no."""
        student = Student(**kwargs)
        self.session.add(student)
        try:
            self.session.commit()
            self.session.refresh(student)
            return student
        except IntegrityError:
            self.session.rollback()
            raise

    def update(self, student: Student, **kwargs) -> Student:
        """Update fields on an existing student and commit."""
        for k, v in kwargs.items():
            if hasattr(student, k):
                setattr(student, k, v)
        try:
            self.session.commit()
            self.session.refresh(student)
            return student
        except IntegrityError:
            self.session.rollback()
            raise

    def delete(self, student: Student) -> None:
        """Delete the student record."""
        self.session.delete(student)
        self.session.commit()
