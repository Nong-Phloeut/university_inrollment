-- 1. Insert roles with explicit IDs
INSERT INTO roles (id, name) VALUES
(1, 'Admin'),
(2, 'Instructor'),
(3, 'Student')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- 2. Insert users with explicit IDs and matching role_ids
INSERT INTO users (id, first_name, last_name, email, password, role_id) VALUES
(1, 'System', 'Admin', 'admin@example.com', 'hashed_admin_password', 1),
(2, 'John', 'Doe', 'john.doe@example.com', 'hashed_password', 2),
(3, 'Jane', 'Student', 'jane.student@example.com', 'hashed_password', 3)
ON DUPLICATE KEY UPDATE email=VALUES(email);

-- 3. Insert instructors linked to users
INSERT INTO instructors (id, employee_number, job_title, status) VALUES
(2, 'T20240001', 'Professor', 'Active')
ON DUPLICATE KEY UPDATE employee_number=VALUES(employee_number);

-- 4. Insert students linked to users
INSERT INTO students (id, student_number, dob, gender, phone_number, enrollment_date, major, status) VALUES
(3, 'S20240001', '2002-09-15', 'Female', '0987654321', '2024-06-01', 'Computer Science', 'Active')
ON DUPLICATE KEY UPDATE student_number=VALUES(student_number);

-- 5. Insert courses with valid instructor_id
INSERT INTO courses (id, code, title, instructor_id, term, year) VALUES
(1, 'CS101', 'Intro to Programming', 2, 'Fall', 2024)
ON DUPLICATE KEY UPDATE code=VALUES(code);

-- 6. Insert course enrollments with all required fields
INSERT INTO course_enrollments (id, student_id, course_id, semester, academic_year, status) VALUES
(1, 3, 1, 'Fall', '2024-2025', 'active')
ON DUPLICATE KEY UPDATE student_id=VALUES(student_id);

-- 7. Insert grades linked to enrollments
INSERT INTO grades (id, enrollment_id, grade, comments, graded_by) VALUES
(1, 1, 'A', 'Excellent performance.', 2)
ON DUPLICATE KEY UPDATE grade=VALUES(grade);
