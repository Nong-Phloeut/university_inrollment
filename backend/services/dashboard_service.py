from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime
from typing import Dict

import models.student_model as student_model
import models.instructor_model as instructor_model
import models.course_model as course_model
import models.course_enrollment_model as course_enrollment_model
import models.user_model as user_model  # ✅ Needed for User join

def get_dashboard_data_service(db: Session) -> Dict:
    # Summary counts
    total_students = db.query(student_model.Student).count()
    total_instructors = db.query(instructor_model.Instructor).count()
    total_courses = db.query(course_model.Course).count()
    pending_approvals = 0  # TODO: replace with actual query

    # Recent enrollments (limit 5)
    recent_enrollments = (
        db.query(
            course_enrollment_model.CourseEnrollment.id.label("id"),
            course_enrollment_model.CourseEnrollment.enrolled_at.label("date"),
            func.concat(user_model.User.first_name, " ", user_model.User.last_name).label("student"),
            func.concat(course_model.Course.code, ": ", course_model.Course.title).label("course")
        )
        .join(student_model.Student, course_enrollment_model.CourseEnrollment.student_id == student_model.Student.id)
        .join(user_model.User, student_model.Student.id == user_model.User.id)
        .join(course_model.Course, course_enrollment_model.CourseEnrollment.course_id == course_model.Course.id)
        .order_by(desc(course_enrollment_model.CourseEnrollment.enrolled_at))
        .limit(5)
        .all()
    )

    # Convert to JSON-friendly format
    recent_enrollments_list = [
        {
            "id": e.id,
            "date": e.date.strftime("%Y-%m-%d") if isinstance(e.date, datetime) else None,
            "student": e.student,
            "course": e.course
        }
        for e in recent_enrollments
    ]

    return {
        "total_students": total_students,
        "total_instructors": total_instructors,
        "total_courses": total_courses,
        "pending_approvals": pending_approvals,
        "recent_enrollments": recent_enrollments_list
    }
