from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHBoxLayout,
    QHeaderView, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt
from controllers.course_enrollment_controller import CourseEnrollmentController
from dialogs.add_enrollment_dialog import AddEnrollmentDialog


class EnrollmentView(QWidget):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        self.enrollment_controller =  CourseEnrollmentController()
        self.init_ui()
        self.load_enrollments_to_table()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 5, 5, 10)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # --- Title ---
        title_label = QLabel("Enrollment Management")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #2C3E50;")
        main_layout.addWidget(title_label)

        main_layout.addSpacing(25) # More space after title

        # --- Controls (Button) ---
        controls_layout = QHBoxLayout()
        self.add_enrollment_btn = QPushButton("Add New Enrollment")
        self.add_enrollment_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745; /* Green color */
                color: white;
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin-right: 10px; /* Space from the edge if needed */
            }
            QPushButton:hover {
                background-color: #218838; /* Darker green on hover */
            }
            QPushButton:pressed {
                background-color: #1e7e34; /* Even darker on pressed */
            }
        """)
        self.add_enrollment_btn.setFixedSize(220, 45) # Slightly larger button
        self.add_enrollment_btn.clicked.connect(self.open_add_enrollment_dialog)
        controls_layout.addWidget(self.add_enrollment_btn)
        controls_layout.addStretch() # Pushes the button to the left
        main_layout.addLayout(controls_layout)

        main_layout.addSpacing(20) # Space between button and table

        # --- Enrollment Table ---
        self.enrollment_table = QTableWidget()
        # Updated column count to include Grade and Enrollment Date
        self.enrollment_table.setColumnCount(6)
        self.enrollment_table.setHorizontalHeaderLabels(["Student Name", "Course Title", "Term", "Grade", "Enrolled Date","Status"])

        self.enrollment_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.enrollment_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.enrollment_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        header_style = """
            ::section {
                background-color: #F8F9FA; /* Light gray background */
                color: #343A40; /* Dark text */
                font-weight: bold;
                padding: 8px;
                border-bottom: 2px solid #DEE2E6; /* Subtle border */
                font-size: 14px;
            }
        """
        self.enrollment_table.horizontalHeader().setStyleSheet(header_style)
        self.enrollment_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.enrollment_table.verticalHeader().setVisible(False) # Hide row numbers

        # Table styling
        self.enrollment_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #D1D9E1;
                border-radius: 5px;
                font-size: 14px;
                selection-background-color: #B0E0E6; /* Light blue selection */
                selection-color: #333333;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #B0E0E6;
                color: #333333;
            }
        """)

        main_layout.addWidget(self.enrollment_table)
        main_layout.addStretch()

        self.setStyleSheet("background-color: #F4F6F9;") # Light background for the view

    def load_enrollments_to_table(self):
        """Loads all enrollment records from the database into the table."""
        self.enrollment_table.setRowCount(0)
        try:
            # Assuming get_enrollments now returns the detailed data from your query
            enrollments = self.enrollment_controller.get_all_enrollments()
            for enrollment in enrollments:
                row = self.enrollment_table.rowCount()
                self.enrollment_table.insertRow(row)

                # Extracting specific fields based on your provided SQL query output
                student_name = enrollment.get('student_name', 'N/A')
                course_title = enrollment.get('course_title', 'N/A')
                term = str(enrollment.get('semester', 'N/A'))
                grade = str(enrollment.get('grade', 'N/A')) # Grade can be NULL or a value
                # Format the enrolled_at date nicely
                enrolled_at = enrollment.get('enrolled_at')
                enrolled_date = enrolled_at.strftime("%Y-%m-%d %H:%M") if enrolled_at else 'N/A'
                status = str(enrollment.get('status', 'N/A')) 


                self.enrollment_table.setItem(row, 0, QTableWidgetItem(student_name))
                self.enrollment_table.setItem(row, 1, QTableWidgetItem(course_title))
                self.enrollment_table.setItem(row, 2, QTableWidgetItem(term))
                self.enrollment_table.setItem(row, 3, QTableWidgetItem(grade))
                self.enrollment_table.setItem(row, 4, QTableWidgetItem(enrolled_date))
                self.enrollment_table.setItem(row, 5, QTableWidgetItem(status))
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Could not load enrollments:\n{e}")

    def open_add_enrollment_dialog(self):
        dialog = AddEnrollmentDialog()
        if dialog.exec():
            data = dialog.get_enrollment_data()
            try:
                self.enrollment_controller.create_enrollment(
                    data["student_id"],
                    data["course_id"],
                    data["semester"],
                    data["academic_year"],
                    data["status"],
                    data["enrollment_date"],
                    data["grade"]
                )
                self.load_enrollments_to_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add enrollment:\n{e}")


                        