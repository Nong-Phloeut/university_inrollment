from models.instructor_model import InstructorModel

class InstructorController:
    def __init__(self):
        self.instructor_model = InstructorModel()

    def get_all_instructors(self):
        return self.instructor_model.get_all_instructors()

    def get_instructor_by_id(self, instructor_id):
        return self.instructor_model.get_instructor_by_id(instructor_id)

    def create_instructor(self, first_name, last_name, email, password, role_id, employee_number, **kwargs):
        return self.instructor_model.create_instructor(
            first_name, last_name, email, password, role_id, employee_number, **kwargs
        )

    def update_instructor(self, instructor_id, **kwargs):
        return self.instructor_model.update_instructor(instructor_id, **kwargs)

    def delete_instructor(self, instructor_id):
        return self.instructor_model.delete_instructor(instructor_id)
