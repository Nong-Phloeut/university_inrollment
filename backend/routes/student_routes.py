from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from controllers.student_controller import get_all_students
from schemas.student_schema import StudentCreate, UserRead
from typing import List

router = APIRouter(prefix="/students", tags=["Students"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[UserRead])
def list_students(db: Session = Depends(get_db)):
    return get_all_students(db)

# @router.post("/", response_model=UserRead)
# def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
#     return add_user(db, user)
