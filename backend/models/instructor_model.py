from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import Base

class Instructor(Base):
    __tablename__ = "instructors"

    id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    employee_number = Column(String(50), nullable=False, unique=True)
    job_title = Column(String(100))
    status = Column(
        String(50),
        server_default="Active",
        CheckConstraint("status IN ('Active', 'On Leave', 'Retired')")
    )
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="instructor")
    courses = relationship("Course", back_populates="instructor")
