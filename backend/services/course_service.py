from sqlalchemy.orm import Session
from models import Course
from schemas.course_schema import CourseCreate, CourseUpdate  # You might need to create CourseUpdate schema
from datetime import datetime

def fetch_all_courses(db: Session):
    return db.query(Course).all()

def create_course(db: Session, user_data: CourseCreate):
    course = Course(
        code=user_data.code,
        title=user_data.title,
        instructor_id=user_data.instructor_id,
        term=user_data.term,
        year=user_data.year,
        created_at=user_data.created_at,
        updated_at=user_data.updated_at,
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

def get_course_by_id(db: Session, course_id: int):
    """Fetch a course by its ID"""
    return db.query(Course).filter(Course.id == course_id).first()

def edit_course(db: Session, course_id: int, update_data: CourseUpdate):
    """Update an existing course by ID"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        return None  # Or raise an exception

    # Update only provided fields
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(course, key, value)

    course.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(course)
    return course

def delete_course(db: Session, course_id: int):
    """Delete a course by ID"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        return None  # Or raise an exception

    db.delete(course)
    db.commit()
    return course
