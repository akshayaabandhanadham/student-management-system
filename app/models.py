

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from .database import Base

class Student(Base):
    """
    Student model represents a student record.
    Fields:
      - id: primary key
      - enrollment_no: unique enrollment number string
      - first_name, last_name, email, course
      - created_at, updated_at: timestamps
    """
    __tablename__ = "students"
    __table_args__ = (UniqueConstraint("enrollment_no", name="uq_enrollment_no"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    enrollment_no = Column(String(64), nullable=False, unique=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=True)
    email = Column(String(120), nullable=True)
    course = Column(String(120), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Student id={self.id} enroll={self.enrollment_no} name={self.first_name} {self.last_name}>"
