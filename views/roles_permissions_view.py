# views/role_view.py
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QLineEdit,
    QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView, QAbstractItemView
)
from PyQt6.QtCore import Qt

# Make sure this path is correct relative to where you run your app
from models.role_model import RoleModel

class RoleView(QWidget):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        self.role_model = RoleModel() # Instantiate your role model
        self.init_ui()
        self.load_roles() # Load roles when the view is initialized

        # Ensure the view has a consistent background color
        self.setStyleSheet("background-color: #FFFFFF;")

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 5, 5, 10) # Padding around the content
        main_layout.setSpacing(20) # Spacing between major sections

        # === Title ===
        title = QLabel("Role Management")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #333333;")
        title.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(title)

        # === Add Role Section ===
        add_role_group_layout = QVBoxLayout()
        add_role_group_layout.setSpacing(10)
        
        add_role_label = QLabel("Add New Role")
        add_role_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #555555;")
        add_role_group_layout.addWidget(add_role_label)

        input_layout = QHBoxLayout()
        self.role_input = QLineEdit()
        self.role_input.setPlaceholderText("Enter new role name (e.g., Editor, Viewer)")
        self.role_input.setFixedHeight(38)
        self.role_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                font-size: 15px;
            }
            QLineEdit:focus {
                border: 1px solid #007bff; /* Highlight on focus */
            }
        """)

        add_button = QPushButton("Add Role")
        add_button.setFixedHeight(38)
        add_button.setFixedWidth(120) # Fixed width for consistency
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745; /* Green */
                color: white;
                border-radius: 5px;
                padding: 5px 15px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        add_button.clicked.connect(self.add_role)

        input_layout.addWidget(self.role_input)
        input_layout.addWidget(add_button)
        add_role_group_layout.addLayout(input_layout)
        main_layout.addLayout(add_role_group_layout)

        # === Role List Table ===
        self.role_table = QTableWidget()
        self.role_table.setColumnCount(2) # ID, Role Name
        self.role_table.setHorizontalHeaderLabels(["ID", "Role Name"])

        # Table Styling
        self.role_table.setStyleSheet("""
            QTableWidget {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                font-size: 14px;
                selection-background-color: #e9ecef; /* Light grey selection */
                selection-color: #333333;
                gridline-color: #e0e0e0;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                color: #495057;
                padding: 8px;
                border: 1px solid #dee2e6;
                font-weight: bold;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #d1e7dd; /* Light green for selected row */
                color: #212529;
            }
        """)
        
        # Adjust header behavior
        self.role_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # ID column
        self.role_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) # Role Name column stretches
        self.role_table.verticalHeader().setVisible(False) # Hide vertical header (row numbers)

        # Selection behavior
        self.role_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows) # Select whole rows
        self.role_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection) # Only one row at a time
        
        # Disable editing cells directly
        self.role_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        main_layout.addWidget(self.role_table)

        # === Actions Button Layout (e.g., Delete) ===
        action_button_layout = QHBoxLayout()
        action_button_layout.addStretch() # Push buttons to the right

        delete_button = QPushButton("Delete Role")
        delete_button.setFixedHeight(38)
        delete_button.setFixedWidth(120)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545; /* Red */
                color: white;
                border-radius: 5px;
                padding: 5px 15px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
            QPushButton:disabled {
                background-color: #e0e0e0;
                color: #a0a0a0;
            }
        """)
        delete_button.clicked.connect(self.delete_role)
        # Disable delete button initially if no role is selected
        delete_button.setEnabled(False) 
        self.role_table.itemSelectionChanged.connect(lambda: delete_button.setEnabled(len(self.role_table.selectedItems()) > 0))

        action_button_layout.addWidget(delete_button)
        main_layout.addLayout(action_button_layout)

        main_layout.addStretch() # Pushes all content to the top

    def load_roles(self):
        """Loads roles from the model into the QTableWidget."""
        self.role_table.setRowCount(0) # Clear existing rows
        roles = self.role_model.get_all_roles()
        
        # Populate table
        for row_idx, role in enumerate(roles):
            self.role_table.insertRow(row_idx)
            id_item = QTableWidgetItem(str(role['id']))
            name_item = QTableWidgetItem(role['name'])
            
            # Set items to be non-editable
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            self.role_table.setItem(row_idx, 0, id_item)
            self.role_table.setItem(row_idx, 1, name_item)

    def add_role(self):
        """Adds a new role based on input field."""
        role_name = self.role_input.text().strip()
        if not role_name:
            QMessageBox.warning(self, "Input Error", "Role name cannot be empty.")
            return

        success = self.role_model.insert_role(role_name)
        if success:
            QMessageBox.information(self, "Success", f"Role '{role_name}' added successfully.")
            self.role_input.clear() # Clear input field
            self.load_roles() # Refresh the table
        else:
            QMessageBox.critical(self, "Error", f"Failed to add role '{role_name}'. It may already exist.")

    def delete_role(self):
        """Deletes the selected role from the table and model."""
        selected_items = self.role_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Selection Error", "Please select a role to delete.")
            return

        # Get the ID from the first column of the selected row
        selected_row = selected_items[0].row()
        role_id_item = self.role_table.item(selected_row, 0)
        role_name_item = self.role_table.item(selected_row, 1)

        if not role_id_item or not role_name_item:
            QMessageBox.critical(self, "Error", "Could not retrieve role information for deletion.")
            return
        
        role_id = int(role_id_item.text())
        role_name = role_name_item.text()

        reply = QMessageBox.question(self, "Confirm Deletion",
                                     f"Are you sure you want to delete role '{role_name}' (ID: {role_id})?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            success = self.role_model.delete_role(role_id)
            if success:
                QMessageBox.information(self, "Success", f"Role '{role_name}' deleted successfully.")
                self.load_roles() # Refresh table
            else:
                QMessageBox.critical(self, "Error", f"Failed to delete role '{role_name}'. Role not found or an error occurred.")