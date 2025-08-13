from pydantic import BaseModel
from typing import List, Optional

class RecentEnrollment(BaseModel):
    id: int
    date: Optional[str]
    student: str
    course: str

    class Config:
        orm_mode = True

class DashboardResponse(BaseModel):
    total_students: int
    total_instructors: int
    total_courses: int
    pending_approvals: int
    recent_enrollments: List[RecentEnrollment]
