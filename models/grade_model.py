from core.database import get_connection

class GradeModel:
    def get_all_grades(self):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT g.id, g.enrollment_id, g.grade, g.comments, g.graded_at,
                           ce.student_id, ce.course_id
                    FROM grades g
                    JOIN course_enrollments ce ON g.enrollment_id = ce.id
                    ORDER BY g.id
                """)
                return cursor.fetchall()

    def get_grade_by_id(self, grade_id):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT g.id, g.enrollment_id, g.grade, g.comments, g.graded_at,
                           ce.student_id, ce.course_id
                    FROM grades g
                    JOIN course_enrollments ce ON g.enrollment_id = ce.id
                    WHERE g.id = %s
                """, (grade_id,))
                return cursor.fetchone()

    def create_grade(self, enrollment_id, grade, comments=None):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO grades (enrollment_id, grade, comments)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """, (enrollment_id, grade, comments))
                grade_id = cursor.fetchone()["id"]
                conn.commit()
                return grade_id

    def update_grade(self, grade_id, grade=None, comments=None):
        fields = []
        values = []
        if grade is not None:
            fields.append("grade = %s")
            values.append(grade)
        if comments is not None:
            fields.append("comments = %s")
            values.append(comments)

        if not fields:
            return

        values.append(grade_id)
        sql = f"UPDATE grades SET {', '.join(fields)} WHERE id = %s"

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, values)
                conn.commit()

    def delete_grade(self, grade_id):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM grades WHERE id = %s", (grade_id,))
                conn.commit()
