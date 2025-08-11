from core.database import get_connection

class CourseModel:
    def get_all_courses(self):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        c.id, c.code, c.title, c.description, c.credits,
                        c.term, c.year,
                        c.instructor_id,
                        CONCAT(u.first_name, ' ', u.last_name) AS instructor_name
                    FROM courses c
                    LEFT JOIN users u ON c.instructor_id = u.id
                    ORDER BY c.id
                 """)
                return cursor.fetchall()

    def get_course_by_id(self, course_id):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT id, code, title, description, credits, instructor_id, term, year
                    FROM courses WHERE id = %s
                """, (course_id,))
                return cursor.fetchone()

    def create_course(self, code, title, description=None, credits=3, instructor_id=None, term=None, year=None):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO courses (code, title, description, credits, instructor_id, term, year)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (code, title, description, credits, instructor_id, term, year))
                course_id = cursor.fetchone()["id"]
                conn.commit()
                return course_id

    def update_course(self, course_id, **kwargs):
        allowed_fields = ['code', 'title', 'description', 'credits', 'instructor_id', 'term', 'year', 'updated_at']
        fields = []
        values = []
        for k, v in kwargs.items():
            if k in allowed_fields:
                fields.append(f"{k} = %s")
                values.append(v)
        if not fields:
            return
        values.append(course_id)
        sql = f"UPDATE courses SET {', '.join(fields)} WHERE id = %s"
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, values)
                conn.commit()

    def delete_course(self, course_id):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM courses WHERE id = %s", (course_id,))
                conn.commit()
