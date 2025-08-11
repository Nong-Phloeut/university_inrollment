# models/transcript_model.py
from core.database import get_connection

class TranscriptModel:
    def get_all_transcripts(self):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        CONCAT(u.first_name, ' ', u.last_name) AS student_name,
                        c.code AS course_code,
                        ce.semester,
                        g.grade
                    FROM course_enrollments ce
                    JOIN students s ON ce.student_id = s.id
                    JOIN users u ON s.id = u.id
                    JOIN courses c ON ce.course_id = c.id
                    LEFT JOIN grades g ON g.enrollment_id = ce.id
                    ORDER BY student_name, ce.semester
                """)
                return cursor.fetchall()
