# schemas/user_schema.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

class GradeBase(BaseModel):
    grade: str
    graded_by: int
    graded_at: datetime
    enrollment_id: int
    comments: str

class GradeCreate(GradeBase):
    password: str

class UserRead(GradeBase):
    id: int

    class Config:
        orm_mode = True