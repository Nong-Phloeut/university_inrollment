from models.course_model import CourseModel

class CourseController:
    def __init__(self):
        self.course_model = CourseModel()

    def get_all_courses(self):
        return self.course_model.get_all_courses()

    def get_course_by_id(self, course_id):
        return self.course_model.get_course_by_id(course_id)

    def create_course(self, code, title, **kwargs):
        return self.course_model.create_course(code, title, **kwargs)

    def update_course(self, course_id, **kwargs):
        return self.course_model.update_course(course_id, **kwargs)

    def delete_course(self, course_id):
        return self.course_model.delete_course(course_id)
