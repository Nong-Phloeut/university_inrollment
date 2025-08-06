from models.course_enrollment_model import CourseEnrollmentModel

class CourseEnrollmentController:
    def __init__(self):
        self.enrollment_model = CourseEnrollmentModel()

    def get_all_enrollments(self):
        return self.enrollment_model.get_all_enrollments()

    def get_enrollment_by_id(self, enrollment_id):
        return self.enrollment_model.get_enrollment_by_id(enrollment_id)

    def create_enrollment(self, student_id, course_id, semester, academic_year, status, enrolled_at, grade):
        return self.enrollment_model.create_enrollment(
            student_id, course_id, semester, academic_year, status, enrolled_at ,grade
        )

    def delete_enrollment(self, enrollment_id):
        return self.enrollment_model.delete_enrollment(enrollment_id)
