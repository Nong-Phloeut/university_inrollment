from core.database import get_connection

class InstructorModel:
    def get_all_instructors(self):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT u.id, u.first_name, u.last_name, u.email, 
                           i.employee_number, i.department, i.phone_number, 
                           i.hire_date, i.job_title, i.status
                    FROM instructors i
                    JOIN users u ON i.id = u.id
                    ORDER BY u.id
                """)
                return cursor.fetchall()

    def get_instructor_by_id(self, instructor_id):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT u.id, u.first_name, u.last_name, u.email, 
                           i.employee_number, i.department, i.phone_number, 
                           i.hire_date, i.job_title, i.status
                    FROM instructors i
                    JOIN users u ON i.id = u.id
                    WHERE i.id = %s
                """, (instructor_id,))
                return cursor.fetchone()

    def create_instructor(self, first_name, last_name, email, password, role_id, employee_number,
                          department=None, phone_number=None, hire_date=None, job_title=None, status='Active'):
        from models.user_model import UserModel
        user_model = UserModel()

        # First create user and get the user ID
        user_id = user_model.create_user(
            first_name, last_name, email, password, role_id
        )

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO instructors (
                        id, employee_number, department, phone_number, 
                        hire_date, job_title, status
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    user_id, employee_number, department, phone_number,
                    hire_date, job_title, status
                ))
                conn.commit()
                return user_id

    def update_instructor(self, instructor_id, **kwargs):
        allowed_fields = [
            'employee_number', 'department', 'phone_number',
            'hire_date', 'job_title', 'status'
        ]
        fields = []
        values = []

        for key, value in kwargs.items():
            if key in allowed_fields:
                fields.append(f"{key} = %s")
                values.append(value)

        if not fields:
            return  # Nothing to update

        values.append(instructor_id)
        sql = f"UPDATE instructors SET {', '.join(fields)} WHERE id = %s"

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, values)
                conn.commit()

    def delete_instructor(self, instructor_id):
        from models.user_model import UserModel
        user_model = UserModel()
        # Since instructors.id references users.id ON DELETE CASCADE,
        # we only need to delete from users
        user_model.delete_user(instructor_id)
