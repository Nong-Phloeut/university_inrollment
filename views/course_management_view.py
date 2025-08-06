from functools import partial
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QLineEdit
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

from dialogs.add_course_dialog import AddCourseDialog
from models.course_model import CourseModel


class CourseManagementView(QWidget):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        self.course_model = CourseModel()

        self.current_page = 1
        self.courses_per_page = 10
        self.total_courses = 0

        self.init_ui()
        self.load_courses()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(25)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)

        self.title_label = QLabel("Course Management")
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #2C3E50;")
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search courses by title or code...")
        self.search_input.setFixedWidth(300)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #BDC3C7;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #3498DB;
            }
        """)
        self.search_input.textChanged.connect(self.search_courses)
        header_layout.addWidget(self.search_input)

        self.add_btn = QPushButton("New Course")
        self.add_btn.setFixedSize(QSize(120, 40))
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #217DBB;
            }
        """)
        self.add_btn.clicked.connect(self.open_add_dialog)
        header_layout.addWidget(self.add_btn)

        self.main_layout.addLayout(header_layout)

        self.course_table = QTableWidget()
        self.course_table.setColumnCount(5)
        self.course_table.setHorizontalHeaderLabels(["ID", "TITLE", "CODE", "INSTRUCTOR", "ACTION"])
        self.course_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.course_table.verticalHeader().setVisible(False)
        self.course_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.course_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.course_table.verticalHeader().setDefaultSectionSize(60)
        self.course_table.setAlternatingRowColors(True)

        self.main_layout.addWidget(self.course_table)

        self.pagination_layout = QHBoxLayout()
        self.pagination_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.showing_label = QLabel(f"Showing {self.courses_per_page} courses")
        self.showing_label.setStyleSheet("color: #555; font-size: 14px;")
        self.pagination_layout.addWidget(self.showing_label)
        self.pagination_layout.addSpacing(20)

        self.prev_btn = QPushButton("<")
        self.prev_btn.setFixedSize(35, 35)
        self.prev_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #BDC3C7;
                border-radius: 5px;
                font-size: 16px;
                color: #3498DB;
            }
            QPushButton:hover {
                background-color: #ECF0F1;
            }
            QPushButton:disabled {
                color: #BDC3C7;
            }
        """)
        self.prev_btn.clicked.connect(self.prev_page)
        self.pagination_layout.addWidget(self.prev_btn)

        self.page_label = QLabel(f"{self.current_page}")
        self.page_label.setStyleSheet("font-weight: bold; font-size: 15px; color: #2C3E50;")
        self.pagination_layout.addWidget(self.page_label)

        self.next_btn = QPushButton(">")
        self.next_btn.setFixedSize(35, 35)
        self.next_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #BDC3C7;
                border-radius: 5px;
                font-size: 16px;
                color: #3498DB;
            }
            QPushButton:hover {
                background-color: #ECF0F1;
            }
            QPushButton:disabled {
                color: #BDC3C7;
            }
        """)
        self.next_btn.clicked.connect(self.next_page)
        self.pagination_layout.addWidget(self.next_btn)

        self.main_layout.addLayout(self.pagination_layout)

    def load_courses(self):
        query = self.search_input.text().lower()
        all_courses = self.course_model.get_all_courses()

        filtered = [
            course for course in all_courses
            if query in course.get("title", "").lower() or query in course.get("code", "").lower()
        ] if query else all_courses

        self.total_courses = len(filtered)
        start = (self.current_page - 1) * self.courses_per_page
        end = start + self.courses_per_page
        paginated_courses = filtered[start:end]

        self.course_table.setRowCount(0)

        for row_num, course in enumerate(paginated_courses):
            self.course_table.insertRow(row_num)
            self.course_table.setItem(row_num, 0, QTableWidgetItem(str(course.get('id', 'N/A'))))
            self.course_table.setItem(row_num, 1, QTableWidgetItem(course.get('title', 'No Title')))
            self.course_table.setItem(row_num, 2, QTableWidgetItem(course.get('code', 'No Code')))
            self.course_table.setItem(row_num, 3, QTableWidgetItem(course.get('instructor_name', 'N/A')))

            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(10)
            action_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            edit_btn = QPushButton()
            edit_btn.setIcon(QIcon("assets/icons/edit_icon.png"))
            edit_btn.setIconSize(QSize(18, 18))
            edit_btn.setFixedSize(30, 30)
            edit_btn.setStyleSheet("border: none; background: transparent;")
            edit_btn.clicked.connect(partial(self.open_edit_dialog, course))

            delete_btn = QPushButton()
            delete_btn.setIcon(QIcon("assets/icons/delete_icon.png"))
            delete_btn.setIconSize(QSize(18, 18))
            delete_btn.setFixedSize(30, 30)
            delete_btn.setStyleSheet("border: none; background: transparent;")
            delete_btn.clicked.connect(partial(self.delete_course, course))

            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            action_layout.addStretch()

            self.course_table.setCellWidget(row_num, 4, action_widget)

        self.update_pagination_controls()
        self.showing_label.setText(f"Showing {len(paginated_courses)} of {self.total_courses} courses")

    def update_pagination_controls(self):
        total_pages = max(1, (self.total_courses + self.courses_per_page - 1) // self.courses_per_page)
        self.page_label.setText(f"Page {self.current_page} of {total_pages}")
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < total_pages)

    def next_page(self):
        total_pages = max(1, (self.total_courses + self.courses_per_page - 1) // self.courses_per_page)
        if self.current_page < total_pages:
            self.current_page += 1
            self.load_courses()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_courses()

    def open_add_dialog(self):
        dialog = AddCourseDialog()
        if dialog.exec():
            self.current_page = 1
            self.load_courses()

    def search_courses(self):
        self.current_page = 1
        self.load_courses()

    def open_edit_dialog(self, course_data):
        QMessageBox.information(self, "Edit Course",
                                f"You clicked Edit for: {course_data.get('title', '')}\n"
                                "Implement your actual edit dialog here.")

    def delete_course(self, course_data):
        reply = QMessageBox.question(
            self,
            'Delete Course',
            f"Are you sure you want to delete '{course_data.get('title', '')}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            if "id" in course_data:
                self.course_model.delete_course(course_data["id"])
                QMessageBox.information(self, "Delete Successful",
                                        f"Course '{course_data.get('title', '')}' deleted successfully.")
                if len(self.course_model.get_all_courses()) % self.courses_per_page == 0 and self.current_page > 1:
                    self.current_page -= 1
                self.load_courses()
            else:
                QMessageBox.warning(self, "Error", "Cannot delete course: ID not found.")
