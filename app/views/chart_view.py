from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
import time

from app.logic.data_controller import DataController
from app.utils.graph_painter import ChartWidget


class ChartView(QWidget):
    chart_status = Signal(str, str)
    
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.setObjectName("coinChart")
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Placeholder
        self.chart_placeholder = QLabel(
            "Price Chart Will Appear Here\n\n"
            "Select a cryptocurrency from the table\n"
            "to view its price chart."
        )
        self.chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.chart_placeholder.setObjectName("chartPlaceholder")
        layout.addWidget(self.chart_placeholder)

        # Custom chart widget (imported from graph_painter)
        self.chart_widget = ChartWidget()
        self.chart_widget.hide()
        layout.addWidget(self.chart_widget)

        # Data controller
        self.controller = DataController()

        # Store chart data
        self._chart_data = None
        self._current_coin_id = None
        self._coin_name = None

    def display_chart(self, coin_data: dict):
        """Fetch and display the 7-day price chart for a coin."""
        coin_id = coin_data.get("id")
        self._coin_name = coin_data.get("name") or coin_id
        if not coin_id:
            return

        history = self.controller.get_coin_history(coin_id)
        
        if not history:
            coin_name = self._coin_name
            self.show_error(f"⚠️ Failed to load chart data for {coin_name}")
            self.chart_status.emit(f"Failed to load chart for {coin_name}", "error")
            return

        # Store data
        self._chart_data = history
        self._current_coin_id = coin_id
        
        # Update chart
        self.chart_widget.set_chart_data(history["timestamps"], history["prices"], self._coin_name)
        self.chart_widget.set_theme(self.main_window.is_dark)
        self.chart_widget.show()
        self.chart_placeholder.hide()
        
        self.chart_status.emit(f"Chart loaded for {self._coin_name}", "success")

    def update_chart_style(self):
        """Update chart theme - called when theme changes"""
        if self._chart_data:
            self.chart_widget.set_theme(self.main_window.is_dark)
            self.chart_widget.update()

    def clear_chart(self):
        """Reset chart to placeholder."""
        self._chart_data = None
        self._current_coin_id = None
        self._coin_name = None
        self.chart_widget.hide()
        self.chart_placeholder.show()

    def show_error(self, message: str):
        """Show an error message in the placeholder."""
        self._chart_data = None
        self._current_coin_id = None
        self._coin_name = None
        self.chart_widget.hide()
        self.chart_placeholder.setText(message)
        self.chart_placeholder.show()

    def current_coin_id(self):
        """Return the coin_id of the currently displayed chart, or None."""
        return self._current_coin_id