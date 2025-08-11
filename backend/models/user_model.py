from core.database import get_connection
from psycopg2.extras import RealDictCursor

class UserModel:
    def get_all_users(self):
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT users.id, users.first_name, users.last_name, users.email, roles.name AS role
                    FROM users
                    JOIN roles ON users.role_id = roles.id
                    ORDER BY users.id
                """)
                return cursor.fetchall()

    def get_user_by_id(self, user_id):
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT users.id, users.first_name, users.last_name, users.email, roles.name AS role
                    FROM users
                    JOIN roles ON users.role_id = roles.id
                    WHERE users.id = %s
                """, (user_id,))
                return cursor.fetchone()

    def create_user(self, first_name, last_name, email, password, role_id):
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO users (first_name, last_name, email, password, role_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (first_name, last_name, email, password, role_id))
                row = cursor.fetchone()
                if not row or "id" not in row:
                    raise Exception("Failed to retrieve user ID after insert.")
                conn.commit()
                return row["id"]

    def update_user(self, user_id, first_name=None, last_name=None, email=None, password=None, role_id=None):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                fields = []
                values = []
                if first_name is not None:
                    fields.append("first_name = %s")
                    values.append(first_name)
                if last_name is not None:
                    fields.append("last_name = %s")
                    values.append(last_name)
                if email is not None:
                    fields.append("email = %s")
                    values.append(email)
                if password is not None:
                    fields.append("password = %s")
                    values.append(password)
                if role_id is not None:
                    fields.append("role_id = %s")
                    values.append(role_id)

                if not fields:
                    return  # Nothing to update

                values.append(user_id)
                sql = f"UPDATE users SET {', '.join(fields)} WHERE id = %s"
                cursor.execute(sql, values)
                conn.commit()

    def delete_user(self, user_id):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                conn.commit()

    def get_instructors_only(self):
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT id, first_name, last_name
                    FROM users
                    WHERE role_id = (
                        SELECT id FROM roles WHERE name = 'Instructor'
                    )
                """)
                return cursor.fetchall()
