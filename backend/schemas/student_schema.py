# schemas/user_schema.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

class StudentBase(BaseModel):
    student_number: str
    dob: datetime
    gender: str
    phone_number: str
    enrollment_date: datetime
    major: str
    status: str

class StudentCreate(StudentBase):
    password: str

class UserRead(StudentBase):
    id: int

    class Config:
        orm_mode = True