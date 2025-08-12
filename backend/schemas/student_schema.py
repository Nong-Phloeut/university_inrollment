# schemas/user_schema.py
from pydantic import BaseModel, EmailStr

class StudentBase(BaseModel):
    student_number: str
    dob: str
    gender: str
    phone_number: str
    enrollment_date: int
    major: int
    status: int

class StudentCreate(StudentBase):
    password: str

class UserRead(StudentBase):
    id: int

    class Config:
        orm_mode = True