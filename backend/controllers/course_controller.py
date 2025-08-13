from sqlalchemy.orm import Session
from services.course_service import fetch_all_courses, create_course, get_course_by_id, edit_course, delete_course_by_Id
from schemas.course_schema import CourseCreate, UserRead, CourseUpdate


def get_all_courses(db: Session):
    return fetch_all_courses(db)

def add_course(db: Session, user_data: CourseCreate):
    return create_course(db, user_data)

def fetc_course_by_id(db: Session, course_id: int):
    return get_course_by_id(db, course_id)

def update_course(db: Session, course_id: int, update_data: CourseUpdate):
    """Update an existing course by ID"""
    return edit_course(db, course_id, update_data)

def delete_course(db: Session, course_id: int):
    """Delete a course by ID"""
    return delete_course_by_Id(db, course_id)