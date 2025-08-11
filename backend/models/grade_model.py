from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import Base

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    enrollment_id = Column(Integer, ForeignKey("course_enrollments.id", ondelete="CASCADE"), nullable=False)
    grade = Column(String(5))
    comments = Column(Text)
    graded_by = Column(Integer, ForeignKey("users.id"))
    graded_at = Column(TIMESTAMP, server_default=func.now())

    enrollment = relationship("CourseEnrollment", back_populates="grade")
