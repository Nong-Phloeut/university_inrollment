# schemas/user_schema.py
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    role_id: int

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    email: str
    password: str