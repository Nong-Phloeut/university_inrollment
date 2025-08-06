from models.dashboard_model import DashboardModel

class DashboardController:
    def __init__(self):
        self.model = DashboardModel()

    def get_user_count_by_role(self, role_name: str) -> int:
        return self.model.get_user_count_by_role(role_name)

    def get_courses_count(self) -> int:
        return self.model.get_courses_count()

    def get_enrollments_count(self) -> int:
        return self.model.get_enrollments_count()
