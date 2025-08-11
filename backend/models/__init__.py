from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .role_model import Role
from .user_model import User
from .student_model import Student
from .instructor_model import Instructor
from .course_model import Course
from .course_enrollment_model import CourseEnrollment
from .grade_model import Grade
