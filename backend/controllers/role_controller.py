from models.role_model import RoleModel

class RoleController:
    def __init__(self):
        self.role_model = RoleModel()

    def get_all_roles(self):
        return self.role_model.get_all_roles()

    def get_role_by_id(self, role_id):
        return self.role_model.get_role_by_id(role_id)

    def create_role(self, name):
        return self.role_model.create_role(name)

    def update_role(self, role_id, name):
        return self.role_model.update_role(role_id, name)

    def delete_role(self, role_id):
        return self.role_model.delete_role(role_id)
