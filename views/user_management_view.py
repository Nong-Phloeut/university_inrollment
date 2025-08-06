from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QLineEdit
)
from PyQt6.QtCore import Qt, QSize
from functools import partial
from PyQt6.QtGui import QIcon

from dialogs.add_user_dialog import AddUserDialog
from models.user_model import UserModel

class UserManagementView(QWidget):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        self.user_model = UserModel()

        self.current_page = 1
        self.users_per_page = 10
        self.total_users = 0

        self.init_ui()
        self.load_users()

    def init_ui(self):
        content_v_layout = QVBoxLayout(self)
        content_v_layout.setContentsMargins(10, 5, 5, 10)
        content_v_layout.setSpacing(10)

        # Top bar
        top_bar_h_layout = QHBoxLayout()
        top_bar_h_layout.setSpacing(15)

        title = QLabel("User Management")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C3E50;")
        top_bar_h_layout.addWidget(title)
        top_bar_h_layout.addStretch()

        search_input = QLineEdit()
        search_input.setPlaceholderText("Search for users...")
        search_input.setFixedWidth(300)
        search_input.setStyleSheet("""
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
        top_bar_h_layout.addWidget(search_input)

        self.add_user_btn = QPushButton("New User")
        self.add_user_btn.clicked.connect(self.open_add_user_dialog)
        self.add_user_btn.setFixedSize(QSize(120, 40))
        self.add_user_btn.setStyleSheet("""
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
        top_bar_h_layout.addWidget(self.add_user_btn)

        content_v_layout.addLayout(top_bar_h_layout)

        # User table
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(6)
        self.user_table.setHorizontalHeaderLabels(["USER ID", "FIRST NAME", "LAST NAME", "EMAIL", "ROLE", "ACTION"])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.user_table.verticalHeader().setVisible(False)
        self.user_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.user_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.user_table.verticalHeader().setDefaultSectionSize(40)

        self.user_table.setStyleSheet("""
            QTableWidget {
                border-radius: 5px;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #DEECF7;
                color: #2C3E50;
            }
            QHeaderView::section {
                background-color: #ECF0F1;
                color: #2C3E50;
                padding: 8px;
                border: 1px solid #BDC3C7;
                font-weight: bold;
            }
        """)

        # Wrap the table in a widget with no extra spacing
        table_wrapper = QWidget()
        table_layout = QVBoxLayout(table_wrapper)
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(0)
        table_layout.addWidget(self.user_table)
        content_v_layout.addWidget(table_wrapper)

        # Pagination
        pagination_layout = QHBoxLayout()
        pagination_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.showing_label = QLabel(f"Showing {self.users_per_page}")
        self.showing_label.setStyleSheet("color: #555; font-size: 14px;")
        pagination_layout.addWidget(self.showing_label)
        pagination_layout.addSpacing(20)

        self.prev_btn = QPushButton("<")
        self.prev_btn.clicked.connect(self.prev_page)
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
        pagination_layout.addWidget(self.prev_btn)

        self.page_label = QLabel(f"{self.current_page}")
        self.page_label.setStyleSheet("font-weight: bold; font-size: 15px; color: #2C3E50;")
        pagination_layout.addWidget(self.page_label)

        self.next_btn = QPushButton(">")
        self.next_btn.clicked.connect(self.next_page)
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
        pagination_layout.addWidget(self.next_btn)

        content_v_layout.addLayout(pagination_layout)

    def load_users(self):
        all_users = self.user_model.get_all_users()
        self.total_users = len(all_users)

        start_index = (self.current_page - 1) * self.users_per_page
        end_index = start_index + self.users_per_page
        users_to_display = all_users[start_index:end_index]

        self.user_table.setRowCount(0)

        for row_num, user in enumerate(users_to_display):
            self.user_table.insertRow(row_num)

            self.user_table.setItem(row_num, 0, QTableWidgetItem(str(user['id'])))
            self.user_table.setItem(row_num, 1, QTableWidgetItem(user['first_name']))
            self.user_table.setItem(row_num, 2, QTableWidgetItem(user['last_name']))
            self.user_table.setItem(row_num, 3, QTableWidgetItem(user['email']))
            self.user_table.setItem(row_num, 4, QTableWidgetItem(user['role']))

            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(10)
            action_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Edit button
            edit_btn = QPushButton()
            edit_btn.setIcon(QIcon("assets/icons/edit_icon.png"))
            edit_btn.setIconSize(QSize(18, 18))
            edit_btn.setFixedSize(30, 30)
            edit_btn.setStyleSheet("border: none; background: transparent;")
            edit_btn.clicked.connect(partial(self.edit_user, user))

            # Delete button
            delete_btn = QPushButton()
            delete_btn.setIcon(QIcon("assets/icons/delete_icon.png"))
            delete_btn.setIconSize(QSize(18, 18))
            delete_btn.setFixedSize(30, 30)
            delete_btn.setStyleSheet("border: none; background: transparent;")
            delete_btn.clicked.connect(partial(self.delete_user, user))

            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            action_layout.addStretch()
            self.user_table.setCellWidget(row_num, 5, action_widget)

        self._update_pagination_buttons()
        self.page_label.setText(f"{self.current_page}")

    def _update_pagination_buttons(self):
        total_pages = (self.total_users + self.users_per_page - 1) // self.users_per_page
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < total_pages)

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_users()

    def next_page(self):
        total_pages = (self.total_users + self.users_per_page - 1) // self.users_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.load_users()

    def open_add_user_dialog(self):
        dialog = AddUserDialog(self)
        if dialog.exec():
            user_data = dialog.get_user_data()
            if user_data:
                self.user_model.create_user(**user_data)
                QMessageBox.information(self, "Success", "User created successfully!")
                self.load_users()

    def edit_user(self, user):
        QMessageBox.information(self, "Edit User", f"Editing user: {user['first_name']} {user['last_name']}")

    def delete_user(self, user):
        reply = QMessageBox.question(
            self, 'Delete User',
            f"Are you sure you want to delete user '{user['first_name']} {user['last_name']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.user_model.delete_user(user['id'])
            QMessageBox.information(self, "Deleted", "User deleted successfully!")
            self.load_users()
