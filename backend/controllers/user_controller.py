from models.user_model import UserModel

class UserController:
    def __init__(self):
        self.user_model = UserModel()

    def get_all_users(self):
        return self.user_model.get_all_users()

    def get_user_by_id(self, user_id):
        return self.user_model.get_user_by_id(user_id)

    def create_user(self, first_name, last_name, email, password, role_id):
        return self.user_model.create_user(first_name, last_name, email, password, role_id)

    def update_user(self, user_id, **kwargs):
        return self.user_model.update_user(user_id, **kwargs)

    def delete_user(self, user_id):
        return self.user_model.delete_user(user_id)
