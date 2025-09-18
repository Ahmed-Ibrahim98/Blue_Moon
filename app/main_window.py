# app/main_window.py
# Add QApplication to the imports
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QIcon
from .views.header_view import HeaderView
from .views.table_view import TableView
from .views.chart_view import ChartView
from .logic.data_controller import DataController
from .config import LOGO_ICON

class MainWindow(QMainWindow):
    # Update the constructor to accept the stylesheet
    def __init__(self, style_sheet: str = ""):
        super().__init__()
        self.style_sheet = style_sheet # Store the stylesheet

        self.setWindowTitle("Crypto Dashboard")
        self.setWindowIcon(QIcon(LOGO_ICON))
        self.setGeometry(100, 100, 1200, 800)
        self.is_dark = False

        self.data_controller = DataController()
        self.init_ui()
        self.apply_theme()

    def init_ui(self):
        # This method remains unchanged
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.header = HeaderView()
        main_layout.addWidget(self.header)

        content_widget = QWidget()
        content_widget.setObjectName("contentWidget")
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        self.table = TableView(self.data_controller)
        self.chart = ChartView()
        content_layout.addWidget(self.table, 3)
        content_layout.addWidget(self.chart, 2)

        main_layout.addWidget(content_widget)

        self.header.refresh_requested.connect(self.table.refresh_data)
        self.header.theme_toggled.connect(self.toggle_theme)

    def toggle_theme(self):
        """Toggles the application's theme between light and dark."""
        self.is_dark = not self.is_dark
        self.apply_theme()

    # This is the corrected method
    def apply_theme(self):
        """Applies the current theme to the application."""
        self.header.update_theme_icon(self.is_dark)
        
        # Set a dynamic property on the main window for QSS to target
        self.setProperty("darkMode", self.is_dark)

        # Re-applying the stylesheet to the entire application ensures
        # all widgets properly update their styles.
        app = QApplication.instance()
        if app:
            app.setStyleSheet(self.style_sheet)