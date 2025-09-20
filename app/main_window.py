from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QIcon
from .views.header_view import HeaderView
from .views.table_view import TableView
from .views.chart_view import ChartView
from app.views.status_bar_view import StatusBarView
from .logic.data_controller import DataController
from app.logic.search_algorithm import SearchAlgorithm
from app.utils.dialog import ExportDialog
from app.utils.file_saver import FileSaver
from .config import LOGO_ICON

class MainWindow(QMainWindow):
    """Main application window for the Blue Moon cryptocurrency dashboard."""

    # Update the constructor to accept the stylesheet
    def __init__(self, style_sheet: str = ""):
        super().__init__()
        self.style_sheet = style_sheet # Store the stylesheet

        # Main window properties
        self.setWindowTitle("Crypto Dashboard")
        self.setWindowIcon(QIcon(LOGO_ICON))
        self.setGeometry(100, 100, 1200, 800)
        self.is_dark = False

        # Data controller
        self.data_controller = DataController()
        # Initialize UI components
        self.init_ui()
        # Apply initial theme
        self.apply_theme()

    def init_ui(self):
        """Initializes the main UI components and layout."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        self.header = HeaderView()
        main_layout.addWidget(self.header)

        # Content area with table and chart
        content_widget = QWidget()
        content_widget.setObjectName("contentWidget")
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        self.table = TableView(self, self.data_controller)
        self.chart = ChartView(self)
        content_layout.addWidget(self.table, 55)
        content_layout.addWidget(self.chart, 45)

        main_layout.addWidget(content_widget)

        # Status bar
        self.status_bar = StatusBarView(self)
        self.setStatusBar(self.status_bar)

        # Connect signals and slots
        self.header.refresh_requested.connect(self.table.refresh_data)
        self.table.status_update.connect(lambda msg, type: self.status_bar.show_message(msg, status_type=type))
        self.table.coin_selected.connect(self.chart.display_chart)
        self.chart.chart_status.connect(lambda msg, type: self.status_bar.show_message(msg, status_type=type))
        self.header.theme_toggled.connect(self.toggle_theme)
        self.header.search_changed.connect(self.on_search)
        self.header.export_requested.connect(self.export_csv)
        
        # Connect the new signal for data availability
        self.table.data_availability_changed.connect(self.header.enable_export_btn)

    def toggle_theme(self):
        """Toggles the application's theme between light and dark."""
        self.is_dark = not self.is_dark
        if self.is_dark:
            self.status_bar.show_message("Dark Mode", status_type="success")
        else:
            self.status_bar.show_message("Light Mode", status_type="success")
        self.apply_theme()

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
        
        # Tell chart to re-style itself if data is loaded
        if hasattr(self, "chart"):
            self.chart.update_chart_style()
    
    def on_search(self, query: str):
        searcher = SearchAlgorithm(self.table.all_data)
        filtered = searcher.search(query)
        self.table.current_data = filtered
        self.table.populate_table(filtered)
        # Clear chart if current coin not in search results
        current_coin = self.chart.current_coin_id()
        if current_coin and not any(c["id"] == current_coin for c in filtered):
            self.chart.clear_chart()

        # Update status bar based on search results
        if filtered:
            self.status_bar.show_message(f"{len(filtered)} coins found", status_type="success")
        else:
            self.status_bar.show_message("No coins matched your search", status_type="warning")
        
        self.table.clear_selection()
    
    def export_csv(self):
        # Only allow export if there's data available (even if it's old data)
        if not self.table.has_data():
            self.status_bar.show_message("No data to export", status_type="error")
            return

        # Confirm export options    
        dialog = ExportDialog(self)
        if dialog.exec():
            file_path, raw = dialog.get_options()
            if file_path:
                success = FileSaver.save_csv(file_path, self.table.all_data, raw=raw)
                if success:
                    self.status_bar.show_message(f"CSV exported to {file_path}", status_type="success")
                else:
                    self.status_bar.show_message("Export failed", status_type="error")