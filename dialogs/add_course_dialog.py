from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit,
    QPushButton, QComboBox, QHBoxLayout, QMessageBox
)
from models.course_model import CourseModel
from models.instructor_model import InstructorModel


class AddCourseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Course")
        self.setFixedSize(400, 400)

        self.course_model = CourseModel()
        self.instructor_model = InstructorModel()
        self.instructor_map = {}

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.code_input = QLineEdit()
        layout.addWidget(QLabel("Course Code:"))
        layout.addWidget(self.code_input)

        self.title_input = QLineEdit()
        layout.addWidget(QLabel("Course Title:"))
        layout.addWidget(self.title_input)

        self.description_input = QTextEdit()
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_input)

        self.instructor_combo = QComboBox()
        layout.addWidget(QLabel("Instructor:"))
        layout.addWidget(self.instructor_combo)
        self.populate_instructors()

        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.save)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def populate_instructors(self):
        instructors = self.instructor_model.get_all_instructors()
        self.instructor_combo.clear()
        self.instructor_map.clear()

        if not instructors:
            self.instructor_combo.addItem("No Instructors Available")
            self.instructor_combo.setEnabled(False)
            return

        self.instructor_combo.setEnabled(True)
        self.instructor_combo.addItem("None", None)  # Optional

        for instructor in instructors:
            full_name = f"{instructor.get('first_name', '')} {instructor.get('last_name', '')}".strip()
            display_name = full_name if full_name else instructor.get("email", "Unknown Instructor")
            self.instructor_combo.addItem(display_name)
            self.instructor_map[display_name] = instructor['id']

    def get_course_data(self):
        code = self.code_input.text().strip()
        title = self.title_input.text().strip()
        description = self.description_input.toPlainText().strip()
        instructor_name = self.instructor_combo.currentText()
        instructor_id = self.instructor_map.get(instructor_name)

        if not code or not title:
            return None

        return {
            "code": code,
            "title": title,
            "description": description,
            "instructor_id": instructor_id
        }

    def save(self):
        data = self.get_course_data()
        if data:
            if self.course_model.create_course(**data):
                QMessageBox.information(self, "Success", "Course created successfully!")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Failed to create course.")
        else:
            QMessageBox.warning(self, "Input Error", "Code and Title are required.")
