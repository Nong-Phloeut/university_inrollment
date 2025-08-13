from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from typing import List

from schemas.course_enrollments_schema import (
    CourseEnrollmentCreate,
    CourseEnrollmentUpdate,
    CourseEnrollmentResponse,
)
import services.course_enrollments as service

router = APIRouter(prefix="/enrollments", tags=["Course Enrollments"])


@router.get("/", response_model=List[dict])
def fetch_enrollments(db: Session = Depends(get_db)):
    enrollments = service.get_all_enrollments(db)
    response = []

    for e in enrollments:
        student_name = (
            f"{e.student.user.first_name} {e.student.user.last_name}"
            if e.student and e.student.user else None
        )
        course_title = e.course.title if e.course else None

        response.append({
            "id": e.id,
            "student_id": e.student_id,
            "student_name": student_name,
            "course_id": e.course_id,
            "course_title": course_title,
            "semester": e.semester,
            "academic_year": e.academic_year,
            "status": e.status,
            "enrolled_at": e.enrolled_at
        })

    return response

@router.get("/{enrollment_id}", response_model=CourseEnrollmentResponse)
def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = service.get_enrollment_by_id(db, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment


@router.post("/", response_model=CourseEnrollmentResponse)
def create_enrollment(enrollment: CourseEnrollmentCreate, db: Session = Depends(get_db)):
    return service.create_enrollment(db, enrollment)


@router.put("/{enrollment_id}", response_model=CourseEnrollmentResponse)
def update_enrollment(enrollment_id: int, update_data: CourseEnrollmentUpdate, db: Session = Depends(get_db)):
    updated = service.update_enrollment(db, enrollment_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return updated


@router.delete("/{enrollment_id}", response_model=CourseEnrollmentResponse)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    deleted = service.delete_enrollment(db, enrollment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return deleted
