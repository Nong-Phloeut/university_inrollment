from sqlalchemy.orm import Session, joinedload
from models.course_enrollment_model import CourseEnrollment
from schemas.course_enrollments_schema import CourseEnrollmentCreate, CourseEnrollmentUpdate
from models.student_model import Student

def get_all_enrollments(db: Session):
    enrollments = (
        db.query(CourseEnrollment)
        .options(
            joinedload(CourseEnrollment.student).joinedload(Student.user),  # load student -> user
            joinedload(CourseEnrollment.course)  # load course
        )
        .all()
    )
    return enrollments


def get_enrollment_by_id(db: Session, enrollment_id: int):
    return db.query(CourseEnrollment).filter(CourseEnrollment.id == enrollment_id).first()


def create_enrollment(db: Session, enrollment_data: CourseEnrollmentCreate):
    new_enrollment = CourseEnrollment(**enrollment_data.dict())
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return new_enrollment


def update_enrollment(db: Session, enrollment_id: int, update_data: CourseEnrollmentUpdate):
    enrollment = get_enrollment_by_id(db, enrollment_id)
    if not enrollment:
        return None
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(enrollment, field, value)
    db.commit()
    db.refresh(enrollment)
    return enrollment


def delete_enrollment(db: Session, enrollment_id: int):
    enrollment = get_enrollment_by_id(db, enrollment_id)
    if not enrollment:
        return None
    db.delete(enrollment)
    db.commit()
    return enrollment
