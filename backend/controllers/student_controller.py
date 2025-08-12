from sqlalchemy.orm import Session
from services.student_service import fetch_all_students

def get_all_students(db: Session):
    return fetch_all_students(db)


    # def get_student_by_id(self, student_id):
    #     return self.student_model.get_student_by_id(student_id)

    # def create_student(self, first_name, last_name, email, password, role_id, student_number, **kwargs):
    #     return self.student_model.create_student(
    #         first_name, last_name, email, password, role_id, student_number, **kwargs
    #     )

    # def update_student(self, student_id, **kwargs):
    #     return self.student_model.update_student(student_id, **kwargs)

    # def delete_student(self, student_id):
    #     return self.student_model.delete_student(student_id)
