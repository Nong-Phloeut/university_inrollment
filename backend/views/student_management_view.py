from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QLineEdit, QSizePolicy
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

from dialogs.add_student_dialog import AddStudentDialog
from models.student_model import StudentModel


class StudentManagementView(QWidget):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        self.student_model = StudentModel()

        self.current_page = 1
        self.students_per_page = 10
        self.total_students = 0

        self.init_ui()
        self.load_students()

    def init_ui(self):
        content_v_layout = QVBoxLayout(self)
        content_v_layout.setContentsMargins(10, 5, 5, 10)
        content_v_layout.setSpacing(20)

        # Top bar
        top_bar_h_layout = QHBoxLayout()
        top_bar_h_layout.setSpacing(15)

        title = QLabel("Student Management")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        top_bar_h_layout.addWidget(title)
        top_bar_h_layout.addStretch()

        self.add_student_btn = QPushButton("New Student")
        self.add_student_btn.clicked.connect(self.open_add_student_dialog)
        self.add_student_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.add_student_btn.setFixedSize(QSize(110, 36))
        top_bar_h_layout.addWidget(self.add_student_btn)

        content_v_layout.addLayout(top_bar_h_layout)

        # Student Table
        self.student_table = QTableWidget()
        self.student_table.setColumnCount(6)
        self.student_table.setHorizontalHeaderLabels([
            "STUDENT ID", "FIRST NAME", "LAST NAME", "CLASSROOM", "STATUS", "ACTION"
        ])
        self.student_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.student_table.verticalHeader().setVisible(False)
        self.student_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.student_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.student_table.verticalHeader().setDefaultSectionSize(40)

        self.student_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                gridline-color: #e0e0e0;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 10px;
                border-bottom: 1px solid #e0e0e0;
                font-weight: bold;
                color: #555;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #e6f7ff;
                color: black;
            }
        """)
        content_v_layout.addWidget(self.student_table)

        # Pagination
        pagination_layout = QHBoxLayout()
        pagination_layout.setContentsMargins(0, 10, 0, 0)
        pagination_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.showing_label = QLabel(f"Showing {self.students_per_page} \u25BC")
        self.showing_label.setStyleSheet("font-size: 13px; color: #555;")
        pagination_layout.addWidget(self.showing_label)
        pagination_layout.addSpacing(20)

        self.prev_btn = QPushButton("<")
        self.prev_btn.clicked.connect(self.prev_page)
        self.prev_btn.setFixedSize(30, 30)
        self.prev_btn.setStyleSheet(self._get_pagination_button_style())
        pagination_layout.addWidget(self.prev_btn)

        self.page_label = QLabel(f"{self.current_page}")
        self.page_label.setStyleSheet("font-weight: bold; font-size: 14px; margin: 0 5px;")
        pagination_layout.addWidget(self.page_label)

        self.next_btn = QPushButton(">")
        self.next_btn.clicked.connect(self.next_page)
        self.next_btn.setFixedSize(30, 30)
        self.next_btn.setStyleSheet(self._get_pagination_button_style())
        pagination_layout.addWidget(self.next_btn)

        content_v_layout.addLayout(pagination_layout)

    def _get_pagination_button_style(self):
        return """
            QPushButton {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px 8px;
                font-size: 14px;
                color: #555;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
            QPushButton:disabled {
                background-color: #f8f9fa;
                color: #bbb;
                border: 1px solid #eee;
            }
        """

    def load_students(self):
        all_students = self.student_model.get_all_students()
        self.total_students = len(all_students)

        start_index = (self.current_page - 1) * self.students_per_page
        end_index = start_index + self.students_per_page
        students_to_display = all_students[start_index:end_index]

        self.student_table.setRowCount(0)
        for row_num, student in enumerate(students_to_display):
            self.student_table.insertRow(row_num)

            self.student_table.setItem(row_num, 0, QTableWidgetItem(str(student["student_number"])))
            self.student_table.setItem(row_num, 1, QTableWidgetItem(student["first_name"]))
            self.student_table.setItem(row_num, 2, QTableWidgetItem(student["last_name"]))
            self.student_table.setItem(row_num, 3, QTableWidgetItem(student.get("classroom", "N/A")))

            # Status column
            status_item = QTableWidgetItem(student.get("status", "Unknown"))
            if student.get("status", "").lower() == "active":
                status_item.setForeground(Qt.GlobalColor.darkGreen)
            else:
                status_item.setForeground(Qt.GlobalColor.red)
            self.student_table.setItem(row_num, 4, status_item)

            # Action buttons with icons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(5)
            action_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            edit_btn = QPushButton()
            edit_btn.setIcon(QIcon("assets/icons/edit_icon.png"))
            edit_btn.setIconSize(QSize(18, 18))
            edit_btn.setFixedSize(28, 28)
            edit_btn.setStyleSheet("border: none; background: transparent;")
            edit_btn.clicked.connect(lambda _, s=student: self.edit_student(s))

            delete_btn = QPushButton()
            delete_btn.setIcon(QIcon("assets/icons/delete_icon.png"))
            delete_btn.setIconSize(QSize(18, 18))
            delete_btn.setFixedSize(28, 28)
            delete_btn.setStyleSheet("border: none; background: transparent;")
            delete_btn.clicked.connect(lambda _, s=student: self.delete_student(s))

            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            action_layout.addStretch()
            self.student_table.setCellWidget(row_num, 5, action_widget)

        self._update_pagination_buttons()
        self.page_label.setText(f"{self.current_page}")

    def _update_pagination_buttons(self):
        total_pages = (self.total_students + self.students_per_page - 1) // self.students_per_page
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < total_pages)

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_students()

    def next_page(self):
        total_pages = (self.total_students + self.students_per_page - 1) // self.students_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.load_students()

    def open_add_student_dialog(self):
        dialog = AddStudentDialog(self)
        if dialog.exec():
            student_data = dialog.get_student_data()
            if student_data:
                self.student_model.create_student(**student_data)
                QMessageBox.information(self, "Success", "Student created successfully!")
                self.current_page = 1
                self.load_students()

    def edit_student(self, student):
        QMessageBox.information(self, "Edit Student", f"Editing student ID: {student['student_id']}")
        # You can open a dialog here to modify and save student info

    def delete_student(self, student):
        reply = QMessageBox.question(
            self,
            'Delete Student',
            f"Are you sure you want to delete student ID '{student['student_id']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.student_model.delete_student(student["student_id"])
            QMessageBox.information(self, "Deleted", "Student deleted successfully!")
            self.current_page = 1
            self.load_students()
