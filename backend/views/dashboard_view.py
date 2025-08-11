from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from controllers.dashboard_controller import DashboardController

class DashboardView(QWidget):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        self.dashboard_controller =  DashboardController()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title
        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2C3E50;")
        main_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignLeft)

        # --- Summary Cards Layout ---
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        # Create cards for Users, Courses, Enrollments
        self.students_card = self.create_card("Students", self.get_students_count())
        self.instructors_card = self.create_card("Instructors", self.get_instructors_count())
        self.admins_card = self.create_card("Admins", self.get_admins_count())
        self.courses_card = self.create_card("Courses", self.get_courses_count())
        self.enrollments_card = self.create_card("Enrollments", self.get_enrollments_count())

        cards_layout.addWidget(self.students_card)
        cards_layout.addWidget(self.instructors_card)
        cards_layout.addWidget(self.admins_card)
        cards_layout.addWidget(self.courses_card)
        cards_layout.addWidget(self.enrollments_card)

        main_layout.addLayout(cards_layout)

        # --- Reports Section ---
        reports_label = QLabel("Reports")
        reports_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #2C3E50;")
        main_layout.addWidget(reports_label, alignment=Qt.AlignmentFlag.AlignLeft)

        reports_layout = QHBoxLayout()
        reports_layout.setSpacing(15)

        btn_transcripts = QPushButton("Generate Transcripts")
        btn_transcripts.clicked.connect(self.on_generate_transcripts)
        reports_layout.addWidget(btn_transcripts)

        btn_enrollments_report = QPushButton("Course Enrollments per Term")
        btn_enrollments_report.clicked.connect(self.on_generate_enrollment_report)
        reports_layout.addWidget(btn_enrollments_report)

        main_layout.addLayout(reports_layout)

        # --- Placeholder for Graphs ---
        graph_label = QLabel("Graphs and Analytics (coming soon)")
        graph_label.setStyleSheet("""
            font-size: 18px; 
            font-style: italic; 
            color: #888888; 
            border: 2px dashed #cccccc; 
            padding: 40px;
            text-align: center;
        """)
        graph_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(graph_label)

        main_layout.addStretch()

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #f0f4f8;")

    def create_card(self, title: str, count: int) -> QFrame:
        card = QFrame()
        card.setFixedSize(160, 100)
        card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #d0d7de;
                padding: 15px;
            }
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)

        count_label = QLabel(str(count))
        count_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        count_label.setStyleSheet("color: #2c3e50;")
        count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; color: #6c757d;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(count_label)
        layout.addWidget(title_label)

        # Save the count label so you can update later
        card.count_label = count_label  
        return card

    # Methods to get counts via the dashboard controller
    def get_students_count(self) -> int:
        return self.dashboard_controller.get_user_count_by_role("student")

    def get_instructors_count(self) -> int:
        return self.dashboard_controller.get_user_count_by_role("instructor")

    def get_admins_count(self) -> int:
        return self.dashboard_controller.get_user_count_by_role("admin")

    def get_courses_count(self) -> int:
        return self.dashboard_controller.get_courses_count()

    def get_enrollments_count(self) -> int:
        return self.dashboard_controller.get_enrollments_count()

    # Optional: call this to refresh all counts dynamically
    def refresh_counts(self):
        self.students_card.count_label.setText(str(self.get_students_count()))
        self.instructors_card.count_label.setText(str(self.get_instructors_count()))
        self.admins_card.count_label.setText(str(self.get_admins_count()))
        self.courses_card.count_label.setText(str(self.get_courses_count()))
        self.enrollments_card.count_label.setText(str(self.get_enrollments_count()))

    # Slots for report buttons
    def on_generate_transcripts(self):
        print("Generate Transcripts clicked")
        # Your code here to open report view or generate PDF etc.

    def on_generate_enrollment_report(self):
        print("Generate Enrollment Report clicked")
        # Your code here to open report view or generate Excel etc.
