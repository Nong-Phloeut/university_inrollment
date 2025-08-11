from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import Base

class CourseEnrollment(Base):
    __tablename__ = "course_enrollments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    semester = Column(String(20), nullable=False)
    academic_year = Column(String(9), nullable=False)
    status = Column(String(20), default="active")
    enrolled_at = Column(TIMESTAMP, server_default=func.now())

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    grade = relationship("Grade", uselist=False, back_populates="enrollment")

    __table_args__ = (
        CheckConstraint("status IN ('active', 'completed', 'dropped')", name="status_check"),
    )
