"""
main.py

Entry point for the Blue Moon application.
Initializes the QApplication, loads the stylesheet, and launches the main window.
"""

import sys
from PySide6.QtWidgets import QApplication
from app.main_window import MainWindow
from app.config import STYLESHEET_PATH

if __name__ == "__main__":
    # Create the Qt application
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Set the Fusion style for consistency

    # Load stylesheet content
    style_sheet = ""
    try:
        # Read the stylesheet file for custom UI styling
        with open(STYLESHEET_PATH, "r", encoding="utf-8") as f:
            style_sheet = f.read()
            app.setStyleSheet(style_sheet)
    except FileNotFoundError:
        print(f"Stylesheet not found at: {STYLESHEET_PATH}")

    # Instantiate and show the main window, passing the stylesheet
    main_window = MainWindow(style_sheet=style_sheet)
    main_window.show()
    sys.exit(app.exec())