from core.database import get_connection

class StudentModel:
    def get_all_students(self):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT u.id, u.first_name, u.last_name, u.email, s.student_number, s.dob, s.gender, s.address,
                           s.phone_number, s.enrollment_date, s.major, s.status, s.emergency_contact_name, s.emergency_contact_phone
                    FROM students s
                    JOIN users u ON s.id = u.id
                    ORDER BY u.id
                """)
                return cursor.fetchall()

    def get_student_by_id(self, student_id):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT u.id, u.first_name, u.last_name, u.email, s.student_number, s.dob, s.gender, s.address,
                           s.phone_number, s.enrollment_date, s.major, s.status, s.emergency_contact_name, s.emergency_contact_phone
                    FROM students s
                    JOIN users u ON s.id = u.id
                    WHERE s.id = %s
                """, (student_id,))
                return cursor.fetchone()
            
    def create_student(self, first_name, last_name, email, password, role_id, student_number, **kwargs):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # 1. Create user
                cursor.execute("""
                    INSERT INTO users (first_name, last_name, email, password, role_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (first_name, last_name, email, password, role_id))
                
                user_row = cursor.fetchone()
                if not user_row:
                    raise Exception("Failed to insert user.")
                user_id = user_row["id"]

                # 2. Create student linked to the user
                cursor.execute("""
                    INSERT INTO students (
                        id, student_number, dob, gender, address,
                        phone_number, enrollment_date, major, status,
                        emergency_contact_name, emergency_contact_phone
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    user_id,
                    student_number,
                    kwargs.get("dob"),
                    kwargs.get("gender"),
                    kwargs.get("address"),
                    kwargs.get("phone_number"),
                    kwargs.get("enrollment_date"),
                    kwargs.get("major"),
                    kwargs.get("status", "Active"),
                    kwargs.get("emergency_contact_name"),
                    kwargs.get("emergency_contact_phone")
                ))

                conn.commit()
                return user_id

    def update_student(self, student_id, **kwargs):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Update users table
                cursor.execute("""
                    UPDATE users SET
                        first_name = %s,
                        last_name = %s,
                        email = %s
                    WHERE id = %s
                """, (
                    kwargs.get("first_name"),
                    kwargs.get("last_name"),
                    kwargs.get("email"),
                    student_id
                ))

                # Update students table
                cursor.execute("""
                    UPDATE students SET
                        student_number = %s,
                        dob = %s,
                        gender = %s,
                        address = %s,
                        phone_number = %s,
                        enrollment_date = %s,
                        major = %s,
                        status = %s,
                        emergency_contact_name = %s,
                        emergency_contact_phone = %s
                    WHERE id = %s
                """, (
                    kwargs.get("student_number"),
                    kwargs.get("dob"),
                    kwargs.get("gender"),
                    kwargs.get("address"),
                    kwargs.get("phone_number"),
                    kwargs.get("enrollment_date"),
                    kwargs.get("major"),
                    kwargs.get("status"),
                    kwargs.get("emergency_contact_name"),
                    kwargs.get("emergency_contact_phone"),
                    student_id
                ))

                conn.commit()
                return True

    def delete_student(self, student_id):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Delete from students first (foreign key dependency)
                cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
                cursor.execute("DELETE FROM users WHERE id = %s", (student_id,))
                conn.commit()
                return True

