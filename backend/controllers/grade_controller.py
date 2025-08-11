from models.grade_model import GradeModel

class GradeController:
    def __init__(self):
        self.grade_model = GradeModel()

    def get_all_grades(self):
        return self.grade_model.get_all_grades()

    def get_grade_by_id(self, grade_id):
        return self.grade_model.get_grade_by_id(grade_id)

    def create_grade(self, enrollment_id, grade, comments=None):
        return self.grade_model.create_grade(enrollment_id, grade, comments)

    def update_grade(self, grade_id, **kwargs):
        return self.grade_model.update_grade(grade_id, **kwargs)

    def delete_grade(self, grade_id):
        return self.grade_model.delete_grade(grade_id)
