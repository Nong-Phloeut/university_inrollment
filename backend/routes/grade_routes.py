from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from controllers.grade_controller import get_all_grade, add_grade
from schemas.grade_schema import GradeCreate, UserRead
from typing import List

router = APIRouter(prefix="/grades", tags=["Grades"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[UserRead])
def list_grade(db: Session = Depends(get_db)):
    print("Fetching all grades")
    return get_all_grade(db)

@router.post("/", response_model=UserRead)
def create_new_grade(user: GradeCreate, db: Session = Depends(get_db)):
    return add_grade(db, user)
