# app/views/chart_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class ChartView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("coinChart")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.chart_placeholder = QLabel(
            "Price Chart Will Appear Here\n\n"
            "Select a cryptocurrency from the table\n"
            "to view its price chart."
        )
        self.chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.chart_placeholder.setObjectName("chartPlaceholder")
        layout.addWidget(self.chart_placeholder)