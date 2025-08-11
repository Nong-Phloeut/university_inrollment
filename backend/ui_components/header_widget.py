# ui_components/header_widget.py
from PyQt6.QtWidgets import (
    QWidget, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize


class HeaderWidget(QWidget):
    def __init__(self, username="Melvin Wilson"):
        super().__init__()

        self.setStyleSheet(self._get_base_stylesheet())
        self.setFixedHeight(60)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 10) # Internal padding of the header
        main_layout.setSpacing(15) # Spacing between major sections in header


        # Spacer to push elements to the right
        main_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self._add_profile_section(main_layout, username)

    def _get_base_stylesheet(self):
        """Returns the base stylesheet for the HeaderWidget."""
        return """
            QWidget {
                background-color: white; /* Header background */
                font-family: 'Segoe UI', sans-serif;
            }
        """ # No border-bottom as shadow handles separation

    def _get_icon_button_stylesheet(self):
        """Returns the stylesheet for icon buttons."""
        return """
            QPushButton {
                background: transparent;
                border: none;
                padding: 5px;
                border-radius: 3px;
                min-width: 30px; /* Ensure a minimum clickable area */
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """

    def _add_logo_and_app_name(self, layout):
        """Adds the application logo and name to the layout, with fallback."""
        logo_label = QLabel()
        logo_pix = QPixmap("assets/logo.png")
        if not logo_pix.isNull():
            logo_label.setPixmap(logo_pix.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            print("Warning: 'assets/logo.png' not found. Using placeholder.")
            logo_label.setText("APP") # Fallback text
            logo_label.setStyleSheet("color: #5c6ac4; font-weight: bold; font-size: 18px;")
        layout.addWidget(logo_label)

        app_name = QLabel("DISA <span style='color:#5c6ac4;'>PA</span>")
        app_name.setStyleSheet("font-size: 18px; font-weight: bold; color: #222;")
        layout.addWidget(app_name)

    def _add_icon_button(self, layout, icon_path, tooltip_text):
        """Helper to create and add an icon button, with robust fallback for missing icons."""
        btn = QPushButton()
        icon = QIcon(icon_path)
        if icon.isNull():
            print(f"Warning: Icon file '{icon_path}' not found. Using text fallback.")
            # Use a unicode character or first letter as fallback
            if "bell" in icon_path: btn.setText("🔔")
            elif "mail" in icon_path: btn.setText("✉️")
            elif "search" in icon_path: btn.setText("🔍")
            elif "menu" in icon_path: btn.setText("☰")
            else: btn.setText("?")
            btn.setStyleSheet(self._get_icon_button_stylesheet() + "color: #555; font-size: 18px;") # Style for text fallback
            btn.setFixedSize(30, 30) # Fixed size for text fallback buttons
        else:
            btn.setIcon(icon)
            btn.setIconSize(QSize(20, 20)) # Set consistent icon size
            btn.setStyleSheet(self._get_icon_button_stylesheet())

        btn.setToolTip(tooltip_text)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(btn)
        return btn # Return button if you need to connect signals externally

    def _add_profile_section(self, layout, username):
        """Adds the user profile picture and name."""
        profile_layout = QHBoxLayout()
        profile_layout.setContentsMargins(0, 0, 0, 0) # Tightly pack elements
        profile_layout.setSpacing(5)

        avatar_label = QLabel()
        profile_pix = QPixmap("assets/user_avatar.png")
        if not profile_pix.isNull():
            profile_pix_scaled = profile_pix.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            avatar_label.setPixmap(profile_pix_scaled)
        else:
            print("Warning: 'assets/user_avatar.png' not found. Using placeholder.")
            avatar_label.setText("👤") # Unicode avatar placeholder
            avatar_label.setStyleSheet("font-size: 20px; color: #555;")
        avatar_label.setFixedSize(32, 32)
        profile_layout.addWidget(avatar_label)

        name_label = QLabel(username)
        name_label.setStyleSheet("font-size: 14px; color: #333;")
        profile_layout.addWidget(name_label)

        # Add a dropdown arrow
        dropdown_arrow = QLabel("▼")
        dropdown_arrow.setStyleSheet("font-size: 10px; color: #555; margin-left: 5px;")
        profile_layout.addWidget(dropdown_arrow)

        profile_container = QWidget()
        profile_container.setLayout(profile_layout)
        profile_container.setCursor(Qt.CursorShape.PointingHandCursor)
        profile_container.setObjectName("profileWidget") # For specific styling
        profile_container.setStyleSheet("""
            #profileWidget {
                border-radius: 5px;
                padding: 5px 10px; /* More padding for a clickable area */
            }
            #profileWidget:hover {
                background-color: #f0f0f0;
            }
            #profileWidget QLabel { /* Ensure labels inside don't interfere with hover */
                background: transparent;
            }
        """)
        layout.addWidget(profile_container)