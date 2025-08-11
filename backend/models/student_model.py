from sqlalchemy import Column, Integer, String, Date, ForeignKey, CheckConstraint, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    student_number = Column(String(50), nullable=False, unique=True)
    dob = Column(Date)
    gender = Column(String(10), nullable=True)
    phone_number = Column(String(20))
    enrollment_date = Column(Date)
    major = Column(String(100))
    status = Column(String(50), server_default="Active")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="student")
    enrollments = relationship("CourseEnrollment", back_populates="student")

    __table_args__ = (
        CheckConstraint("gender IN ('Male', 'Female', 'Other')", name="chk_gender_valid"),
        CheckConstraint("status IN ('Active', 'On Leave', 'Graduated', 'Suspended')", name="chk_status_valid"),
    )
