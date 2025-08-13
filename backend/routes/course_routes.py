from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from controllers.course_controller import get_all_courses, add_course, fetc_course_by_id, update_course, delete_course
from schemas.course_schema import CourseCreate, UserRead
from typing import List

router = APIRouter(prefix="/courses", tags=["Courses"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[UserRead])
def list_course(db: Session = Depends(get_db)):
    return get_all_courses(db)

@router.post("/", response_model=UserRead)
def create_new_course(course: CourseCreate, db: Session = Depends(get_db)):
    return add_course(db, course)

@router.get("/{course_id}", response_model=UserRead)
def get_course(course_id: int, db: Session = Depends(get_db)):
    return fetc_course_by_id(db, course_id)

@router.put("/{course_id}", response_model=UserRead)
def update_course_info(course_id: int, course: CourseCreate, db: Session = Depends(get_db)):
    return update_course(db, course_id, course)

@router.delete("/{course_id}", response_model=UserRead)
def delete_course_info(course_id: int, db: Session = Depends(get_db)):
    return delete_course(db, course_id)
