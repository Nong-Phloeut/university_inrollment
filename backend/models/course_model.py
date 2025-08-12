from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(20), nullable=False, unique=True)  # e.g., MATH101
    title = Column(String(255), nullable=False)
    instructor_id = Column(Integer, ForeignKey("instructors.id", ondelete="SET NULL"))
    term = Column(String(50))
    year = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    instructor = relationship("Instructor", back_populates="courses")
    enrollments = relationship("CourseEnrollment", back_populates="course")
