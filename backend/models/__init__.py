from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .role import Role
from .user import User
from .student import Student
from .instructor import Instructor
from .course import Course
from .course_enrollment import CourseEnrollment
from .grade import Grade
