from core.database import get_connection

class RoleModel:
    def get_all_roles(self):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, name FROM roles")
                return cursor.fetchall()

    def insert_role(self, role_name):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(
                        "INSERT INTO roles (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
                        (role_name,)
                    )
                    conn.commit()
                    return True
                except Exception as e:
                    conn.rollback()
                    print(f"Error inserting role: {e}")
                    return False

    def delete_role(self, role_id):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute("DELETE FROM roles WHERE id = %s", (role_id,))
                    conn.commit()
                    return True
                except Exception as e:
                    conn.rollback()
                    print(f"Error deleting role: {e}")
                    return False

    def update_role(self, role_id, new_name):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(
                        "UPDATE roles SET name = %s WHERE id = %s",
                        (new_name, role_id)
                    )
                    conn.commit()
                    return True
                except Exception as e:
                    conn.rollback()
                    print(f"Error updating role: {e}")
                    return False
