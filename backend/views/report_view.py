# views/report_view.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QLabel, QComboBox, QMessageBox, QTextEdit, QHeaderView,
    QFormLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class ReportView(QWidget): # Renamed from ReportManagementTab
    # Signals to communicate user actions to the controller
    generate_transcript_requested = pyqtSignal(int) # student_id
    generate_enrollment_report_requested = pyqtSignal(object, str) # course_id (or None), term

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20) # Add padding

        title_label = QLabel("Report Management")
        title_label.setFont(QFont("Inter", 24, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #333333;")
        layout.addWidget(title_label)
        layout.addSpacing(10)

        # Student Transcript Section
        transcript_group_box = QWidget()
        transcript_group_box.setObjectName("ReportSection") # For styling
        transcript_group_layout = QVBoxLayout()
        transcript_group_box.setLayout(transcript_group_layout)
        transcript_group_layout.addWidget(QLabel("<h3>Student Transcript</h3>"))

        transcript_form_layout = QHBoxLayout()
        self.transcript_student_combo = QComboBox()
        self.populate_transcript_student_combo()
        self.generate_transcript_button = QPushButton("Generate Transcript")
        self.generate_transcript_button.clicked.connect(self._emit_generate_transcript)

        transcript_form_layout.addWidget(QLabel("Select Student:"))
        transcript_form_layout.addWidget(self.transcript_student_combo)
        transcript_form_layout.addWidget(self.generate_transcript_button)
        transcript_group_layout.addLayout(transcript_form_layout)

        self.transcript_output = QTextEdit()
        self.transcript_output.setReadOnly(True)
        transcript_group_layout.addWidget(self.transcript_output)
        layout.addWidget(transcript_group_box)

        # Course Enrollments Report Section
        enrollment_report_group_box = QWidget()
        enrollment_report_group_box.setObjectName("ReportSection") # For styling
        enrollment_report_layout = QVBoxLayout()
        enrollment_report_group_box.setLayout(enrollment_report_layout)
        enrollment_report_layout.addWidget(QLabel("<h3>Course Enrollments Report</h3>"))

        enrollment_report_form_layout = QHBoxLayout()
        self.report_course_combo = QComboBox()
        self.populate_report_course_combo()
        self.report_term_input = QLineEdit()
        self.report_term_input.setPlaceholderText("Optional: Enter Term (e.g., Fall 2025)")
        self.generate_enrollment_report_button = QPushButton("Generate Report")
        self.generate_enrollment_report_button.clicked.connect(self._emit_generate_enrollment_report)

        enrollment_report_form_layout.addWidget(QLabel("Select Course:"))
        enrollment_report_form_layout.addWidget(self.report_course_combo)
        enrollment_report_form_layout.addWidget(QLabel("Term:"))
        enrollment_report_form_layout.addWidget(self.report_term_input)
        enrollment_report_form_layout.addWidget(self.generate_enrollment_report_button)
        enrollment_report_layout.addLayout(enrollment_report_form_layout)

        self.enrollment_report_output_table = QTableWidget()
        self.enrollment_report_output_table.setColumnCount(4)
        self.enrollment_report_output_table.setHorizontalHeaderLabels(['Student Name', 'Course Code', 'Term', 'Grade'])
        self.enrollment_report_output_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.enrollment_report_output_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # Make table read-only
        enrollment_report_layout.addWidget(self.enrollment_report_output_table)
        layout.addWidget(enrollment_report_group_box)

        self.setLayout(layout)

    def populate_transcript_student_combo(self):
        self.transcript_student_combo.clear()
        for user in self.controller.get_students():
            self.transcript_student_combo.addItem(user['name'], user['id'])

    def populate_report_course_combo(self):
        self.report_course_combo.clear()
        self.report_course_combo.addItem("All Courses", None) # Option to report on all courses
        for course in self.controller.get_all_courses():
            self.report_course_combo.addItem(f"{course['code']} - {course['title']}", course['id'])

    def _emit_generate_transcript(self):
        student_id = self.transcript_student_combo.currentData()
        self.generate_transcript_requested.emit(student_id)

    def _emit_generate_enrollment_report(self):
        course_id = self.report_course_combo.currentData()
        term = self.report_term_input.text().strip()
        self.generate_enrollment_report_requested.emit(course_id, term)

    def display_transcript(self, transcript_text):
        self.transcript_output.setText(transcript_text)

    def display_enrollment_report(self, enrollments_data, course_details_func, user_name_func):
        self.enrollment_report_output_table.setRowCount(len(enrollments_data))
        if not enrollments_data:
            # Clear table if no results
            self.enrollment_report_output_table.clearContents()
            self.enrollment_report_output_table.setRowCount(0)
            return

        for row_idx, enrollment in enumerate(enrollments_data):
            student_name = user_name_func(enrollment['student_id'])
            course = course_details_func(enrollment['course_id'])
            course_code = course['code'] if course else "Unknown"
            grade = enrollment['grade'] if enrollment['grade'] else "N/A"

            self.enrollment_report_output_table.setItem(row_idx, 0, QTableWidgetItem(student_name))
            self.enrollment_report_output_table.setItem(row_idx, 1, QTableWidgetItem(course_code))
            self.enrollment_report_output_table.setItem(row_idx, 2, QTableWidgetItem(enrollment['term']))
            self.enrollment_report_output_table.setItem(row_idx, 3, QTableWidgetItem(grade))

    def show_message(self, title, message, is_error=False):
        if is_error:
            QMessageBox.warning(self, title, message)
        else:
            QMessageBox.information(self, title, message)
