from functools import partial
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QLineEdit
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

from dialogs.add_user_dialog import AddUserDialog
from controllers.instructor_controller import InstructorController  # Use InstructorController


class InstructorManagementView(QWidget):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        self.instructor_controller = InstructorController()

        self.current_page = 1
        self.instructors_per_page = 10
        self.total_instructors = 0

        self.init_ui()
        self.load_instructors()

    def init_ui(self):
        content_v_layout = QVBoxLayout(self)
        content_v_layout.setContentsMargins(10, 5, 5, 10)
        content_v_layout.setSpacing(20)

        # Top bar layout
        top_bar_h_layout = QHBoxLayout()
        top_bar_h_layout.setSpacing(15)

        title = QLabel("Instructor Management")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        top_bar_h_layout.addWidget(title)
        top_bar_h_layout.addStretch()

        # Search bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search for instructors")
        self.search_input.setFixedWidth(250)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        self.search_input.textChanged.connect(self.on_search_text_changed)
        top_bar_h_layout.addWidget(self.search_input)

        # Add button
        self.add_instructor_btn = QPushButton("New Instructor")
        self.add_instructor_btn.clicked.connect(self.open_add_instructor_dialog)
        self.add_instructor_btn.setStyleSheet("""
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
        self.add_instructor_btn.setFixedSize(QSize(140, 36))
        top_bar_h_layout.addWidget(self.add_instructor_btn)

        content_v_layout.addLayout(top_bar_h_layout)

        # Table setup
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(6)
        self.user_table.setHorizontalHeaderLabels(["EMAIL", "FIRST NAME", "LAST NAME", "EMPLOYEE NO.", "STATUS", "ACTION"])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.user_table.verticalHeader().setVisible(False)
        self.user_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.user_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        content_v_layout.addWidget(self.user_table)

        # Pagination bar
        pagination_layout = QHBoxLayout()
        pagination_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.prev_btn = QPushButton("<")
        self.prev_btn.setFixedSize(30, 30)
        self.prev_btn.setStyleSheet(self._get_pagination_button_style())
        self.prev_btn.clicked.connect(self.prev_page)
        pagination_layout.addWidget(self.prev_btn)

        self.page_label = QLabel(str(self.current_page))
        self.page_label.setStyleSheet("font-weight: bold; font-size: 14px; margin: 0 5px;")
        pagination_layout.addWidget(self.page_label)

        self.next_btn = QPushButton(">")
        self.next_btn.setFixedSize(30, 30)
        self.next_btn.setStyleSheet(self._get_pagination_button_style())
        self.next_btn.clicked.connect(self.next_page)
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

    def load_instructors(self):
        search_text = self.search_input.text().lower().strip()
        all_instructors = self.instructor_controller.get_all_instructors()

        if search_text:
            all_instructors = [
                user for user in all_instructors
                if search_text in user.get("email", "").lower()
                or search_text in user.get("first_name", "").lower()
                or search_text in user.get("last_name", "").lower()
            ]

        self.total_instructors = len(all_instructors)

        start_index = (self.current_page - 1) * self.instructors_per_page
        end_index = start_index + self.instructors_per_page
        instructors_to_display = all_instructors[start_index:end_index]

        self.user_table.setRowCount(0)

        for row_num, user in enumerate(instructors_to_display):
            self.user_table.insertRow(row_num)
            self.user_table.setItem(row_num, 0, QTableWidgetItem(user.get("email", "")))
            self.user_table.setItem(row_num, 1, QTableWidgetItem(user.get("first_name", "")))
            self.user_table.setItem(row_num, 2, QTableWidgetItem(user.get("last_name", "")))
            self.user_table.setItem(row_num, 3, QTableWidgetItem(user.get("employee_number", "")))

            status = user.get("status", "Inactive")
            status_item = QTableWidgetItem(status)
            status_item.setForeground(Qt.GlobalColor.darkGreen if status.lower() == "active" else Qt.GlobalColor.red)
            self.user_table.setItem(row_num, 4, status_item)

            # Action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(5)

            edit_btn = QPushButton("✎")
            edit_btn.setFixedSize(24, 24)
            edit_btn.setStyleSheet("border: none; background: transparent; font-size: 16px; color: #555;")
            edit_btn.clicked.connect(partial(self.edit_instructor, user))

            delete_btn = QPushButton("🗑")
            delete_btn.setFixedSize(24, 24)
            delete_btn.setStyleSheet("border: none; background: transparent; font-size: 16px; color: #555;")
            delete_btn.clicked.connect(partial(self.delete_instructor, user))

            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            action_layout.addStretch()

            self.user_table.setCellWidget(row_num, 5, action_widget)

        self._update_pagination_buttons()
        self.page_label.setText(str(self.current_page))

    def _update_pagination_buttons(self):
        total_pages = (self.total_instructors + self.instructors_per_page - 1) // self.instructors_per_page
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < total_pages)

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_instructors()

    def next_page(self):
        total_pages = (self.total_instructors + self.instructors_per_page - 1) // self.instructors_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.load_instructors()

    def open_add_instructor_dialog(self):
        dialog = AddUserDialog(self)
        if dialog.exec():
            instructor_data = dialog.get_user_data()
            if instructor_data:
                self.instructor_controller.instructor_model.create_instructor(**instructor_data)
                QMessageBox.information(self, "Success", "Instructor created successfully!")
                self.current_page = 1
                self.load_instructors()

    def edit_instructor(self, instructor):
        QMessageBox.information(self, "Edit Instructor", f"Editing: {instructor.get('email', '')}")
        # TODO: Implement edit dialog logic

    def delete_instructor(self, instructor):
        reply = QMessageBox.question(
            self,
            "Delete Instructor",
            f"Are you sure you want to delete instructor '{instructor.get('email', '')}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.instructor_controller.instructor_model.delete_instructor(instructor["id"])
            QMessageBox.information(self, "Deleted", "Instructor deleted successfully!")
            self.current_page = 1
            self.load_instructors()

    def on_search_text_changed(self):
        self.current_page = 1
        self.load_instructors()
