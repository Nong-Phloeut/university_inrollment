# schemas/user_schema.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class CourseBase(BaseModel):
    code: str
    title: str
    instructor_id : int
    term: str
    year: int
    created_at: datetime
    updated_at: datetime

class CourseCreate(CourseBase):
    """Schema for creating a new course"""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class UserRead(CourseBase):
    id: int

    class Config:
        orm_mode = True
        
        
class CourseUpdate(BaseModel):
    code: Optional[str] = None
    title: Optional[str] = None
    instructor_id: Optional[int] = None
    term: Optional[str] = None
    year: Optional[int] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
