# app/views/chart_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objs as go
import plotly.io as pio

from app.logic.data_controller import DataController


class ChartView(QWidget):
    chart_status = Signal(str, str)
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.setObjectName("coinChart")
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Placeholder (when no coin is selected yet)
        self.chart_placeholder = QLabel(
            "Price Chart Will Appear Here\n\n"
            "Select a cryptocurrency from the table\n"
            "to view its price chart."
        )
        self.chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.chart_placeholder.setObjectName("chartPlaceholder")
        layout.addWidget(self.chart_placeholder)

        # Plotly chart inside a QWebEngineView
        self.browser = QWebEngineView()
        layout.addWidget(self.browser)
        self.browser.hide()

        # 🔹 Make browser background transparent
        self.browser.setStyleSheet("background: transparent; border: none;")
        self.browser.page().setBackgroundColor(Qt.transparent)

        # Data controller
        self.controller = DataController()

        # Store chart data so we can restyle without re-fetch
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
            self.show_error("⚠️ Failed to load chart data.")
            self.chart_status.emit(f"Failed to load chart for {coin_name}", "error")
            return

        # Store data so we can re-style later
        self._chart_data = history
        self._current_coin_id = coin_id
        self.update_chart_style()
        # Status for successful chart load
        self.chart_status.emit(f"Chart loaded for {self._coin_name}", "success")


    def update_chart_style(self):
        """Re-render the chart with the current theme (no re-fetch)."""
        if not self._chart_data:
            return

        timestamps, prices = self._chart_data["timestamps"], self._chart_data["prices"]

        # Light/dark from main_window
        is_dark = self.main_window.is_dark

        # Theme-aware colors (match QSS palette)
        if is_dark:
            bg_color = "#1e293b"
            grid_color = "rgba(255,255,255,0.2)"
            font_color = "#e2e8f0"
            line_color = "#60a5fa"
        else:
            bg_color = "#ffffff"
            grid_color = "rgba(0,0,0,0.1)"
            font_color = "#1a2a3a"
            line_color = "#2c5bdc"

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=timestamps,
            y=prices,
            mode="lines",
            line=dict(color=line_color, width=3),
            hovertemplate="Date: %{x}<br>Price: $%{y:.2f}<extra></extra>"
        ))

        fig.update_layout(
            title=f"{self._coin_name} - 7-Day Price (USD)",
            title_x=0.5,
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            xaxis=dict(showgrid=True, gridcolor=grid_color, zeroline=False, color=font_color),
            yaxis=dict(showgrid=True, gridcolor=grid_color, zeroline=False, color=font_color),
            font=dict(size=12, color=font_color),
        )

        html = pio.to_html(
            fig,
            full_html=False,
            include_plotlyjs="cdn",
            config={"displayModeBar": True, "displaylogo": False}
        )

        self.browser.setHtml(html)
        self.browser.show()
        self.chart_placeholder.hide()

    def clear_chart(self):
        """Reset chart to placeholder."""
        self._chart_data = None
        self._current_coin_id = None
        self._coin_name = None
        self.browser.hide()
        self.chart_placeholder.setText(
            "Price Chart Will Appear Here\n\n"
            "Select a cryptocurrency from the table\n"
            "to view its price chart."
        )
        self.chart_placeholder.show()

    def show_error(self, message: str):
        """Show an error message in the placeholder."""
        self._chart_data = None
        self._current_coin_id = None
        self._coin_name = None
        self.browser.hide()
        self.chart_placeholder.setText(message)
        self.chart_placeholder.show()

    def current_coin_id(self):
        """Return the coin_id of the currently displayed chart, or None."""
        return self._current_coin_id
