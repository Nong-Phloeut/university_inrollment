import sys
from PyQt6.QtWidgets import QApplication
from layouts.main_layout import MainLayout

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainLayout()
    window.show()
    sys.exit(app.exec())
 