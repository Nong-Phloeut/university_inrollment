from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from controllers.user_controller import get_all_users, add_user
from schemas.user_schema import UserCreate, UserRead
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[UserRead])
def list_users(db: Session = Depends(get_db)):
    return get_all_users(db)

@router.post("/", response_model=UserRead)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return add_user(db, user)
