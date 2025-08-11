# main_layout.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QGraphicsDropShadowEffect, QLabel, QFrame, QApplication
)
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt

# Make sure these imports are correct based on your project structure
from views.dashboard_view import DashboardView 
from views.course_management_view import CourseManagementView         
from views.course_enrollment_view import  EnrollmentView        
from views.roles_permissions_view import  RoleView        
from views.user_management_view import  UserManagementView        
from views.student_management_view import  StudentManagementView        
from views.instructor_management_view import  InstructorManagementView        
from views.transcripts_view import  TranscriptsView        
from ui_components.sidebar_widget import SidebarWidget
from ui_components.header_widget import HeaderWidget


class MainLayout(QMainWindow):
    def __init__(self, controller=None): # Added default None for controller for standalone testing
        super().__init__()
        self.setWindowTitle("University Dashboard")
        self.setStyleSheet("background-color: #F5F6FA;") # Light background for the entire application window
        self.resize(1200, 800)

        # Set a consistent font for the entire application
        font = QFont('SF Pro', 14)
        QApplication.instance().setFont(font)

        # Root Widget & Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0) # Remove any default margins
        main_layout.setSpacing(0) # Remove spacing between sidebar and content area

        # === Sidebar ===
        self.sidebar = SidebarWidget()
        # Apply shadow to the sidebar
        self._apply_shadow(self.sidebar, dx=2, dy=0, blur=15, color=QColor(0, 0, 0, 20)) # Subtle right shadow
        main_layout.addWidget(self.sidebar)

        # === Main Content Area (Header + Stacked Views) ===
        content_container = QWidget() # This widget holds header and main views
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0) # No margins within this vertical container
        content_layout.setSpacing(0) # No spacing between header and the main view area

        # === Header ===
        self.header = HeaderWidget(username="Melvin Wilson")
        # Apply shadow to the header
        self._apply_shadow(self.header, dx=0, dy=2, blur=15, color=QColor(0, 0, 0, 20)) # Subtle bottom shadow
        content_layout.addWidget(self.header)

        # === Main Content Wrapper (holds QStackedWidget and provides padding/background) ===
        # This wrapper will have the light background and padding for your actual content views
        main_content_wrapper = QWidget()
        main_content_wrapper.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF; /* White background for the main content area */
                border-radius: 8px; /* Subtle rounding for the content area if desired */
                /* For a fully white area that fills, remove border-radius if it creates unwanted gaps */
            }
        """)
        main_content_layout = QVBoxLayout(main_content_wrapper)
        main_content_layout.setContentsMargins(20, 20, 20, 20) # Padding around your stacked views
        main_content_layout.setSpacing(20) # Spacing between elements *within* your views if they exist

        # === QStackedWidget for Views ===
        self.stack = QStackedWidget()
        # Ensure your DashboardView and UserView have layouts that make them fill space
        self.dashboard_view = DashboardView(controller)
        self.course_management_view = CourseManagementView(controller)
        self.enrollment_view = EnrollmentView(controller)
        self.roles_permissions_view = RoleView(controller)
        self.user_management_view = UserManagementView(controller)
        self.student_management_view = StudentManagementView(controller)
        self.instructor_management_view = InstructorManagementView(controller)
        self.transcripts_view = TranscriptsView(controller)

        self.stack.addWidget(self.dashboard_view)
        self.stack.addWidget(self.course_management_view)
        self.stack.addWidget(self.enrollment_view)
        self.stack.addWidget(self.roles_permissions_view)
        self.stack.addWidget(self.user_management_view)
        self.stack.addWidget(self.student_management_view)
        self.stack.addWidget(self.instructor_management_view)
        self.stack.addWidget(self.transcripts_view)
        main_content_layout.addWidget(self.stack) # Add the stacked widget to the wrapper's layout

        # Add the main content wrapper to the overall content container
        content_layout.addWidget(main_content_wrapper, stretch=1) # Make sure it stretches to fill remaining space

        # Add the main content container to the horizontal main layout
        main_layout.addWidget(content_container, stretch=1)

        # Connect sidebar buttons to switch views and update header title
        # In all connect() calls: remove the third argument (objectName)
        self.sidebar.dashboard_btn.clicked.connect(
            lambda: self.switch_view(self.dashboard_view, "Dashboard")
        )
        self.sidebar.user_btn.clicked.connect(
            lambda: self.switch_view(self.user_management_view, "User Management")
        )
        # User Management
        self.sidebar.students_btn.clicked.connect(
            lambda: self.switch_view(self.student_management_view, "Student Management")
        )
        self.sidebar.instructors_btn.clicked.connect(
            lambda: self.switch_view(self.instructor_management_view, "Instructors Management")
        )
        # Course Management
        self.sidebar.course_list_btn.clicked.connect(
            lambda: self.switch_view(self.course_management_view, "Course List")
        )
        self.sidebar.enrollment_btn.clicked.connect(
            lambda: self.switch_view(self.enrollment_view, "Enrollment")
        )
        # Report Management
        self.sidebar.transcripts_btn.clicked.connect(
            lambda: self.switch_view(self.transcripts_view, "Transcripts")
        )
        # Settings
        self.sidebar.roles_permissions_btn.clicked.connect(
            lambda: self.switch_view(self.roles_permissions_view, "Roles & Permissions")
        )
        # Logout
        self.sidebar.logout_btn.clicked.connect(
            lambda: self.switch_view(self.logout_view, "Logout")
        )


    def _apply_shadow(self, widget, dx=0, dy=2, blur=15, color=QColor(0, 0, 0, 20)):
        """Applies a QGraphicsDropShadowEffect to a widget."""
        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(dx, dy)
        shadow.setBlurRadius(blur)
        shadow.setColor(color)
        widget.setGraphicsEffect(shadow)

    def switch_view(self, view: QWidget, title: str):
        self.stack.setCurrentWidget(view)
        # self.header.set_page_title(title)

    # Assuming your HeaderWidget has this method



