from core.database import get_connection

class DashboardModel:
    def get_user_count_by_role(self, role_name: str) -> int:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(u.id)
                    FROM users u
                    JOIN roles r ON u.role_id = r.id
                    WHERE r.name = %s
                """, (role_name,))
                return cursor.fetchone()

    def get_courses_count(self) -> int:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM courses")
                return cursor.fetchone()

    def get_enrollments_count(self) -> int:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM course_enrollments")
                return cursor.fetchone()
