from sqlalchemy.orm import Session, joinedload
from models.student_model import Student
from models.course_enrollment_model import CourseEnrollment
from models.grade_model import Grade

def compute_gpa(grades):
    """Simple GPA mapping"""
    grade_map = {"A":4.0, "B":3.0, "C":2.0, "D":1.0, "F":0.0}
    total_points = 0
    count = 0
    for g in grades:
        if g in grade_map:
            total_points += grade_map[g]
            count += 1
    return round(total_points / count, 2) if count else 0

def get_student_transcript(db: Session, student_id: int):
    """Fetch single student transcript with courses and grades"""
    enrollments = (
        db.query(CourseEnrollment)
        .filter(CourseEnrollment.student_id == student_id)
        .options(
            joinedload(CourseEnrollment.course),          # load course
            joinedload(CourseEnrollment.grade),           # load grade
            joinedload(CourseEnrollment.student).joinedload(Student.user)  # load user
        )
        .all()
    )
    if not enrollments:
        return None

    courses_data = []
    total_score = 0
    course_count = 0
    grade_letters = []

    for e in enrollments:
        grade = e.grade
        score = grade.score if grade and hasattr(grade, "score") else 0
        total_score += score
        course_count += 1
        grade_letters.append(grade.grade if grade and grade.grade else None)

        courses_data.append({
            "id": e.course.id if e.course else None,
            "title": e.course.title if e.course else None,
            "score": score,
            "grade": grade.grade if grade else None,
            "remarks": grade.comments if grade else None
        })

    average_score = total_score / course_count if course_count else 0
    gpa = compute_gpa(grade_letters)

    student_name = (
        f"{enrollments[0].student.user.first_name} {enrollments[0].student.user.last_name}"
        if enrollments[0].student and enrollments[0].student.user else None
    )

    return {
        "studentId": student_id,
        "studentName": student_name,
        "totalScore": total_score,
        "averageScore": average_score,
        "gpa": gpa,
        "courses": courses_data
    }


def get_all_transcripts(db: Session):
    """Fetch transcript summary for all students"""
    students = db.query(Student).options(joinedload(Student.user)).all()
    result = []

    for student in students:
        enrollments = (
            db.query(CourseEnrollment)
            .filter(CourseEnrollment.student_id == student.id)
            .options(joinedload(CourseEnrollment.grade))
            .all()
        )
        total_score = sum(e.grade.score if e.grade and hasattr(e.grade, "score") else 0 for e in enrollments)
        course_count = len(enrollments)
        average_score = total_score / course_count if course_count else 0
        gpa = compute_gpa([e.grade.grade if e.grade else None for e in enrollments])

        result.append({
            "studentId": student.id,
            "studentName": f"{student.user.first_name} {student.user.last_name}" if student.user else None,
            "totalScore": total_score,
            "averageScore": average_score,
            "gpa": gpa
        })

    return result
