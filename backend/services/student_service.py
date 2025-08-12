from sqlalchemy.orm import Session
from models import Student
from schemas.student_schema import StudentCreate

def fetch_all_students(db: Session):
    return db.query(Student).all()

def create_user(db: Session, user_data: StudentCreate):
    user = Student(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password=user_data.password,  # ? Hash in real apps
        role_id=user_data.role_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
