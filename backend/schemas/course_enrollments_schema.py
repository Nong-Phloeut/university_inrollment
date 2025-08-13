from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CourseEnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    semester: str
    academic_year: str
    status: Optional[str] = "active"


class CourseEnrollmentCreate(CourseEnrollmentBase):
    pass


class CourseEnrollmentUpdate(BaseModel):
    semester: Optional[str]
    academic_year: Optional[str]
    status: Optional[str]


class CourseEnrollmentResponse(CourseEnrollmentBase):
    id: int
    enrolled_at: datetime

    class Config:
        orm_mode = True
