from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt, QSize
from models.role_model import RoleModel


class AddUserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New User")
        self.setFixedSize(450, 480)  # Increased size for better spacing
        self.user_data = {}

        self.role_model = RoleModel()

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        title_label = QLabel("Create New User")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #34495E;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        main_layout.addSpacing(20)

        # Helper to create a labeled input with spacing
        def create_styled_input(placeholder, label_text="", echo_mode=QLineEdit.EchoMode.Normal):
            layout = QVBoxLayout()
            layout.setSpacing(6)

            label = QLabel(label_text)
            label.setStyleSheet("font-size: 14px; color: #555;")

            line_edit = QLineEdit()
            line_edit.setPlaceholderText(placeholder)
            line_edit.setEchoMode(echo_mode)
            line_edit.setMinimumHeight(35)
            line_edit.setStyleSheet("""
                QLineEdit {
                    padding: 8px 12px;
                    border: 1px solid #BDC3C7;
                    border-radius: 5px;
                    font-size: 14px;
                    background-color: #FFFFFF;
                }
                QLineEdit:focus {
                    border: 1px solid #3498DB;
                }
            """)

            layout.addWidget(label)
            layout.addWidget(line_edit)
            return layout, line_edit

        # First Name
        first_name_layout, self.first_name_input = create_styled_input("Enter first name", "First Name:")
        main_layout.addLayout(first_name_layout)

        # Last Name
        last_name_layout, self.last_name_input = create_styled_input("Enter last name", "Last Name:")
        main_layout.addLayout(last_name_layout)

        # Email
        email_layout, self.email_input = create_styled_input("Enter email address", "Email:")
        main_layout.addLayout(email_layout)

        # Password
        password_layout, self.password_input = create_styled_input("Enter password", "Password:", QLineEdit.EchoMode.Password)
        main_layout.addLayout(password_layout)

        # Role
        role_layout = QVBoxLayout()
        role_layout.setSpacing(6)

        role_label = QLabel("Role:")
        role_label.setStyleSheet("font-size: 14px; color: #555;")

        self.role_select = QComboBox()
        self.role_select.setMinimumHeight(35)
        self.role_select.setStyleSheet("""
            QComboBox {
                padding: 8px 12px;
                border: 1px solid #BDC3C7;
                border-radius: 5px;
                font-size: 14px;
                background-color: #FFFFFF;
                selection-background-color: #3498DB;
                selection-color: white;
            }
            QComboBox::drop-down {
                border: 0px;
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: url(assets/icons/down_arrow.png);
                width: 14px;
                height: 14px;
            }
            QComboBox:focus {
                border: 1px solid #3498DB;
            }
        """)
        self.populate_roles()

        role_layout.addWidget(role_label)
        role_layout.addWidget(self.role_select)
        main_layout.addLayout(role_layout)

        main_layout.addStretch()

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedSize(QSize(100, 40))
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #ECF0F1;
                color: #2C3E50;
                border: 1px solid #BDC3C7;
                border-radius: 5px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D5DBDB;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Save User")
        save_btn.setFixedSize(QSize(120, 40))
        save_btn.setStyleSheet("""
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
        save_btn.clicked.connect(self.save_user)
        btn_layout.addWidget(save_btn)

        main_layout.addSpacing(15)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    def populate_roles(self):
        roles = self.role_model.get_all_roles()
        self.roles_map = {}

        if not roles:
            self.role_select.addItem("No Roles Available")
            self.role_select.setEnabled(False)
            return

        for role in roles:
            self.role_select.addItem(role["name"])
            self.roles_map[role["name"]] = role["id"]

    def save_user(self):
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        role_name = self.role_select.currentText()
        role_id = self.roles_map.get(role_name)

        if not first_name or not last_name or not email or not password:
            QMessageBox.warning(self, "Missing Information", "All fields are required. Please fill them out.")
            return

        if "@" not in email or "." not in email:
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Password Too Short", "Password must be at least 6 characters long.")
            return

        if not role_id:
            QMessageBox.warning(self, "Role Missing", "No role selected or available. Please ensure roles are loaded.")
            return

        self.user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "role_id": role_id
        }
        self.accept()

    def get_user_data(self):
        return self.user_data
