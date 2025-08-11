from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon 
from PyQt6.QtGui import QPixmap
import os


class SidebarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(220)
        self.setStyleSheet("background-color: #F9F9FB;")  # Match light sidebar

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 25, 20, 25)
        self.main_layout.setSpacing(4)

        # === App Title ===
        logo_label = QLabel()
        logo_pixmap = QPixmap("assets/logo/school.png")  # Use your actual logo path

        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaledToWidth(140, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
        else:
            logo_label.setText("Logo not found")

        logo_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(logo_label)

        self.main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # --- Navigation Buttons ---
        self.dashboard_btn = self._create_nav_button("Dashboard", "dashboard_btn", "assets/icons/dashboard.png")
        self.user_btn = self._create_nav_button("User Management", "user_btn", "assets/icons/users.png")
        self.students_btn = self._create_nav_button("Student Management", "students_btn", "assets/icons/users.png")
        self.instructors_btn = self._create_nav_button("Instructors Management", "instructors_btn", "assets/icons/users.png")
        self.course_list_btn = self._create_nav_button("Course Management", "course_list_btn", "assets/icons/graduation-cap.png")
        self.enrollment_btn = self._create_nav_button("Enrollment", "enrollment_btn", "assets/icons/school.png")
        self.transcripts_btn = self._create_nav_button("Transcripts", "transcripts_btn", "assets/icons/notebook.png")
        self.roles_permissions_btn = self._create_nav_button("Roles & Permissions", "roles_permissions_btn", "assets/icons/settings.png")
        self.logout_btn = self._create_nav_button("Logout", "logout_btn", "assets/icons/log-out.png")

        for btn in [
            self.dashboard_btn, 
            self.user_btn,
            self.students_btn,
            self.instructors_btn,
            self.course_list_btn, 
            self.enrollment_btn,
            self.transcripts_btn,
            self.roles_permissions_btn,
            self.logout_btn
        ]:
            self.main_layout.addWidget(btn)

        self.main_layout.addStretch()

        self.all_nav_buttons = [
            self.dashboard_btn,
            self.user_btn,
            self.students_btn,
            self.instructors_btn,
            self.course_list_btn,
            self.enrollment_btn,
            self.transcripts_btn,
            self.roles_permissions_btn,
            self.logout_btn
        ]

        for btn in self.all_nav_buttons:
            btn.clicked.connect(lambda checked, b=btn: self.set_active_button(b.objectName()))

        self.set_active_button("dashboard_btn")

    def _create_nav_button(self, text: str, object_name: str, icon_path: str):
        btn = QPushButton(text)
        btn.setObjectName(object_name)

        if os.path.exists(icon_path):
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(18, 18))
        else:
            print(f"Icon not found: {icon_path}")

        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #555555;
                font-size: 14px;
                text-align: left;
                padding: 10px 12px;
                border-radius: 18px;
            }
            QPushButton:hover {
                background-color: #E6E8F1;
                color: #1F1F1F;
            }
            QPushButton[active="true"] {
                background-color: #A8A3A3;
            }
        """)
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        return btn

    def set_active_button(self, active_object_name: str):
        for btn in self.all_nav_buttons:
            is_active = btn.objectName() == active_object_name
            btn.setProperty("active", is_active)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
