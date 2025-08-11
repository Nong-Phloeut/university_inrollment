from core.database import get_connection

class CourseEnrollmentModel:
    def get_all_enrollments(self):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        ce.id,
                        ce.student_id,
                        ce.course_id,
                        ce.semester,
                        ce.academic_year,
                        ce.status,
                        ce.enrolled_at,
                        c.code,
                        c.title AS course_title,
                        CONCAT(u.first_name, ' ', u.last_name) AS student_name,
                        g.grade
                    FROM course_enrollments ce
                    JOIN students s ON ce.student_id = s.id
                    JOIN users u ON s.id = u.id
                    JOIN courses c ON ce.course_id = c.id
                    LEFT JOIN grades g ON g.enrollment_id = ce.id
                    ORDER BY ce.id
                """)
                return cursor.fetchall()

    def get_enrollment_by_id(self, enrollment_id):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        ce.id,
                        ce.student_id,
                        ce.course_id,
                        ce.semester,
                        ce.academic_year,
                        ce.status,
                        ce.enrolled_at,
                        u.first_name,
                        u.last_name,
                        c.code,
                        c.title AS course_title,
                    FROM course_enrollments ce
                    JOIN students s ON ce.student_id = s.id
                    JOIN users u ON s.id = u.id
                    JOIN courses c ON ce.course_id = c.id
                    WHERE ce.id = %s
                """, (enrollment_id,))
                return cursor.fetchone()

    def create_enrollment(self, student_id, course_id, semester, academic_year, status, enrolled_at, grade=None):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO course_enrollments (
                        student_id, course_id, semester, academic_year, status, enrolled_at
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (student_id, course_id, semester, academic_year, status, enrolled_at))
                enrollment_id = cursor.fetchone()["id"]

                if grade:
                    cursor.execute("""
                        INSERT INTO grades (enrollment_id, grade)
                        VALUES (%s, %s)
                    """, (enrollment_id, grade))
                conn.commit()
                return enrollment_id


    def delete_enrollment(self, enrollment_id):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM course_enrollments WHERE id = %s", (enrollment_id,))
                conn.commit()
