# main.py
import sys
from PySide6.QtWidgets import QApplication
from app.main_window import MainWindow
from app.config import STYLESHEET_PATH

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Load stylesheet content
    style_sheet = ""
    try:
        with open(STYLESHEET_PATH, "r") as f:
            style_sheet = f.read()
            app.setStyleSheet(style_sheet)
    except FileNotFoundError:
        print(f"Stylesheet not found at: {STYLESHEET_PATH}")

    # Pass the stylesheet content to the main window
    main_window = MainWindow(style_sheet=style_sheet)
    main_window.show()
    sys.exit(app.exec())