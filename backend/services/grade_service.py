from sqlalchemy.orm import Session
from models import Grade
from schemas.grade_schema import GradeCreate

def fetch_all_grades(db: Session):
    return db.query(Grade).all()

def create_grade(db: Session, user_data: GradeCreate):
    grade = Grade(
        grade=user_data.grade,
        graded_by=user_data.graded_by,
        graded_at=user_data.graded_at,
        enrollment_id=user_data.enrollment_id,
        comments=user_data.comments,
    )
    db.add(grade)
    db.commit()
    db.refresh(grade)
    return grade
