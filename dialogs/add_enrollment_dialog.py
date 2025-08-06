from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
    QWidget, QComboBox, QDateEdit
)
from PyQt6.QtCore import Qt, QDate
from models.student_model import StudentModel
from models.course_model import CourseModel


class AddEnrollmentDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Enrollment")
        self.setFixedSize(400, 400)
        self.setModal(True)

        self.course_model = CourseModel()
        self.student_model = StudentModel()
        self.enrollment_data = {}

        # Fetch students and courses
        self.students = self.student_model.get_all_students()
        self.courses = self.course_model.get_all_courses()

        self.init_ui()
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border: 1px solid #cccccc;
                border-radius: 8px;
            }
            QLabel {
                font-size: 14px;
                color: #333333;
                padding-bottom: 5px;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton {
                padding: 10px 15px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            #saveButton {
                background-color: #007bff;
                color: white;
            }
            #saveButton:hover {
                background-color: #0056b3;
            }
            #cancelButton {
                background-color: #6c757d;
                color: white;
            }
            #cancelButton:hover {
                background-color: #5a6268;
            }
        """)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # --- Student Select ---
        self.student_select = QComboBox()
        self.student_select.addItem("-- Select Student --", None)
        for student in self.students:
            full_name = f"{student['first_name']} {student['last_name']}"
            self.student_select.addItem(full_name, student["id"])
        main_layout.addLayout(self._create_input_row("Student:", self.student_select))

        # --- Course Select ---
        self.course_select = QComboBox()
        self.course_select.addItem("-- Select Course --", None)
        for course in self.courses:
            self.course_select.addItem(course["title"], course["id"])
        main_layout.addLayout(self._create_input_row("Course:", self.course_select))

        # --- Term Select ---
        self.semester_input = QComboBox()
        self.semester_input.addItems(["semester 1", "semester 2"])
        main_layout.addLayout(self._create_input_row("Semester:", self.semester_input))

        self.grade_input = QComboBox()
        self.grade_input.addItems(["A", "A-",
            "B+", "B", "B-",
            "C+", "C", "C-",
            "D+", "D", "D-",
            "F",
            "P",  # Pass
            "W",  # Withdrawn
            "I",  # Incomplete
        ])
        main_layout.addLayout(self._create_input_row("Grade:", self.grade_input))

        # --- Academic Year ---
        self.academic_year_input = QLineEdit()
        self.academic_year_input.setPlaceholderText("e.g. 2025-2026")
        main_layout.addLayout(self._create_input_row("Academic Year:", self.academic_year_input))

        # --- Status Select ---
        self.status_input = QComboBox()
        self.status_input.addItems(["active", "completed", "dropped"])
        main_layout.addLayout(self._create_input_row("Status:", self.status_input))

        # --- Enrollment Date ---
        self.enrollment_date_input = QDateEdit()
        self.enrollment_date_input.setDisplayFormat("yyyy-MM-dd")
        self.enrollment_date_input.setDate(QDate.currentDate())
        self.enrollment_date_input.setCalendarPopup(True)
        main_layout.addLayout(self._create_input_row("Enrollment Date:", self.enrollment_date_input))

        # --- Buttons ---
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.save_button = QPushButton("Save")
        self.save_button.setObjectName("saveButton")
        self.save_button.clicked.connect(self._on_save_clicked)
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(button_layout)

    def _create_input_row(self, label_text: str, input_widget: QWidget):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setFixedWidth(120)
        layout.addWidget(label)
        layout.addWidget(input_widget)
        return layout

    def _on_save_clicked(self):
        student_id = self.student_select.currentData()
        course_id = self.course_select.currentData()
        semester = self.semester_input.currentText()
        academic_year = self.academic_year_input.text().strip()
        status = self.status_input.currentText()
        enrollment_date = self.enrollment_date_input.date().toString("yyyy-MM-dd")
        grade = self.grade_input.currentText()

        if not student_id or not course_id:
            QMessageBox.warning(self, "Input Error", "Please select both a student and a course.")
            return

        if not academic_year:
            QMessageBox.warning(self, "Input Error", "Please enter the academic year.")
            return

        self.enrollment_data = {
            "student_id": student_id,
            "course_id": course_id,
            "semester": semester,
            "academic_year": academic_year,
            "status": status,
            "enrollment_date": enrollment_date,
            "grade": grade
        }
        self.accept()

    def get_enrollment_data(self):
        return self.enrollment_data
