# schemas/user_schema.py
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: str
    password: str
    role_id: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True