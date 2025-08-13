# from models.grade_model import Grade

# class GradeController:
#     def __init__(self):
#         self.grade_model = Grade()

#     def get_all_grades(self):
#         return self.grade_model.get_all_grades()

#     def get_grade_by_id(self, grade_id):
#         return self.grade_model.get_grade_by_id(grade_id)

#     def create_grade(self, enrollment_id, grade, comments=None):
#         return self.grade_model.create_grade(enrollment_id, grade, comments)

#     def update_grade(self, grade_id, **kwargs):
#         return self.grade_model.update_grade(grade_id, **kwargs)

#     def delete_grade(self, grade_id):
#         return self.grade_model.delete_grade(grade_id)

from sqlalchemy.orm import Session
from services.grade_service import fetch_all_grades, create_grade
from schemas.grade_schema import GradeCreate, UserRead


def get_all_grade(db: Session):
    print("Fetching all grades")
    return fetch_all_grades(db)

def add_grade(db: Session, user_data: GradeCreate):
    return create_grade(db, user_data)
