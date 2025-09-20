from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLineEdit, QLabel
from PySide6.QtGui import QIcon
from ..config import (LIGHT_THEME_ICON, DARK_THEME_ICON,
                      REFRESH_LIGHT_ICON, REFRESH_DARK_ICON)

class HeaderView(QWidget):
    theme_toggled = Signal()
    refresh_requested = Signal()
    search_changed = Signal(str)
    export_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("headerContainer")
        self.setFixedHeight(70)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(15)

        title_label = QLabel("BLUE MOON")
        title_label.setObjectName("appTitle")

        self.theme_button = QPushButton()
        self.theme_button.setCheckable(True)
        self.theme_button.setFixedSize(40, 40)
        self.theme_button.setObjectName("themeButton")
        self.theme_button.clicked.connect(self.theme_toggled.emit)

        self.refresh_button = QPushButton("  Refresh")
        self.refresh_button.setObjectName("headerButton")
        self.refresh_button.clicked.connect(self.refresh_requested.emit)

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("🔍 Search cryptocurrencies...")
        self.search_field.setMinimumWidth(300)
        self.search_field.setObjectName("searchField")
        self.search_field.textChanged.connect(self.search_changed.emit)

        self.export_csv_button = QPushButton("Export CSV")
        self.export_csv_button.setObjectName("headerButton")
        self.export_csv_button.clicked.connect(self.export_requested.emit)
        # Initially enabled - will be updated by data availability signal
        self.export_csv_button.setEnabled(True)

        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(self.theme_button)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.search_field)
        layout.addWidget(self.export_csv_button)

    def update_theme_icon(self, is_dark: bool):
        """Updates icons based on the current theme."""
        if is_dark:
            self.theme_button.setIcon(QIcon(LIGHT_THEME_ICON))
            self.refresh_button.setIcon(QIcon(REFRESH_DARK_ICON))
        else:
            self.theme_button.setIcon(QIcon(DARK_THEME_ICON))
            self.refresh_button.setIcon(QIcon(REFRESH_LIGHT_ICON))
    
    def get_search_text(self) -> str:
        return self.search_field.text().strip()
    
    def clear_search(self):
        self.search_field.clear()
    
    def enable_export_btn(self, enable: bool):
        """Enable or disable the export button."""
        self.export_csv_button.setEnabled(enable)
        
        # Optional: Add visual feedback when disabled
        if not enable:
            self.export_csv_button.setToolTip("No data to export")
        else:
            self.export_csv_button.setToolTip("Export data to CSV")