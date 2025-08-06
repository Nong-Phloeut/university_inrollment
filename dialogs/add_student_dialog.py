from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QDateEdit, QTextEdit
)
from PyQt6.QtCore import Qt, QDate


class AddStudentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Student")
        self.setFixedSize(500, 750)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # ----- USER INFORMATION -----
        self.first_name_input = QLineEdit()
        layout.addLayout(self._create_form_row("First Name:", self.first_name_input))

        self.last_name_input = QLineEdit()
        layout.addLayout(self._create_form_row("Last Name:", self.last_name_input))

        self.email_input = QLineEdit()
        layout.addLayout(self._create_form_row("Email:", self.email_input))

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addLayout(self._create_form_row("Password:", self.password_input))

        self.role_combo = QComboBox()
        self.role_combo.addItems(["Student"])  # Can be dynamic in future
        layout.addLayout(self._create_form_row("Role:", self.role_combo))

        # ----- STUDENT INFORMATION -----
        self.student_number_input = QLineEdit()
        layout.addLayout(self._create_form_row("Student Number:", self.student_number_input))

        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDate(QDate.currentDate())
        layout.addLayout(self._create_form_row("Date of Birth:", self.dob_input))

        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female", "Other"])
        layout.addLayout(self._create_form_row("Gender:", self.gender_combo))

        self.address_input = QTextEdit()
        self.address_input.setFixedHeight(60)
        layout.addLayout(self._create_form_row("Address:", self.address_input))

        self.phone_input = QLineEdit()
        layout.addLayout(self._create_form_row("Phone Number:", self.phone_input))

        self.enrollment_date_input = QDateEdit()
        self.enrollment_date_input.setCalendarPopup(True)
        self.enrollment_date_input.setDate(QDate.currentDate())
        layout.addLayout(self._create_form_row("Enrollment Date:", self.enrollment_date_input))

        self.major_input = QLineEdit()
        layout.addLayout(self._create_form_row("Major:", self.major_input))

        self.status_combo = QComboBox()
        self.status_combo.addItems(["Active", "On Leave", "Graduated", "Suspended"])
        layout.addLayout(self._create_form_row("Status:", self.status_combo))

        self.emergency_contact_name_input = QLineEdit()
        layout.addLayout(self._create_form_row("Emergency Contact Name:", self.emergency_contact_name_input))

        self.emergency_contact_phone_input = QLineEdit()
        layout.addLayout(self._create_form_row("Emergency Contact Phone:", self.emergency_contact_phone_input))

        # ----- BUTTONS -----
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(self.ok_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_btn)

        layout.addLayout(buttons_layout)

    def _create_form_row(self, label_text, widget):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setFixedWidth(160)
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(widget)
        return layout

    def get_student_data(self):
        return {
            # User fields
            "first_name": self.first_name_input.text().strip(),
            "last_name": self.last_name_input.text().strip(),
            "email": self.email_input.text().strip(),
            "password": self.password_input.text().strip(),
            "role_id": 3,  # Assuming 3 = Student. You can pass or fetch this dynamically.

            # Student fields
            "student_number": self.student_number_input.text().strip(),
            "dob": self.dob_input.date().toString("yyyy-MM-dd"),
            "gender": self.gender_combo.currentText(),
            "address": self.address_input.toPlainText().strip(),
            "phone_number": self.phone_input.text().strip(),
            "enrollment_date": self.enrollment_date_input.date().toString("yyyy-MM-dd"),
            "major": self.major_input.text().strip(),
            "status": self.status_combo.currentText(),
            "emergency_contact_name": self.emergency_contact_name_input.text().strip(),
            "emergency_contact_phone": self.emergency_contact_phone_input.text().strip(),
        }
