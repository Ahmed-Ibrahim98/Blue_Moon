from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QBrush
from typing import List, Dict
from datetime import datetime
from ..logic.data_controller import DataController
from ..utils.formatting import DataFormatter


class TableView(QWidget):
    """View for displaying cryptocurrency data in a table."""
    
    coin_selected = Signal(dict)  # Emitted when a coin is selected
    status_update = Signal(str, str)  # message, status_type
    data_availability_changed = Signal(bool)  # New signal for data availability

    def __init__(self, main_window, data_controller: DataController, parent=None):
        super().__init__(parent)
        self.data_controller = data_controller
        self.main_window = main_window
        self.setObjectName("coinsTable")

        self.all_data: List[Dict] = []
        self.current_data: List[Dict] = []

        self.sort_column = 0
        self.sort_order = Qt.SortOrder.AscendingOrder

        self.setup_ui()
        self.refresh_data()

    def setup_ui(self):
        """Set up the table UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setObjectName("cryptoTable")
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Rank", "Name (Symbol)", "Price", "24h %", "Market Cap"])

        header = self.table.horizontalHeader()
        # Set initial column widths with more space for Price and 24h %
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Rank
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Name - will take remaining space
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)  # Price - fixed width
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)  # 24h % - fixed width
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Interactive)  # Market Cap - fixed width
        
        # Set minimum widths to ensure content fits
        self.table.setColumnWidth(2, 120)  # Price column - wide enough for large values
        self.table.setColumnWidth(3, 80)   # 24h % column - wide enough for percentages like -10.00%
        self.table.setColumnWidth(4, 120)  # Market Cap column
        
        header.sectionClicked.connect(self.on_header_clicked)

        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)

        layout.addWidget(self.table)

    def refresh_data(self):
        """Fetch coins and emit status messages."""
        self.clear_selection()
        self.main_window.header.clear_search()
        self.status_update.emit("Fetching coin data...", "info")
        
        data = self.data_controller.fetch_top_coins()
        if data:
            self.all_data = data
            self.current_data = list(self.all_data)
            self.apply_sorting()
            timestamp = datetime.now().strftime("%H:%M")
            self.status_update.emit(f"Coins fetched at {timestamp}", "success")
            self.data_availability_changed.emit(True)  # Emit data available
        else:
            # Only show error message, don't disable export if we have existing data
            self.status_update.emit("Failed to fetch new data - using existing data", "warning")
            # Don't emit data_availability_changed(False) here - we still have old data to export

    def populate_table(self, data: List[Dict]):
        """Populate the table with given coin data."""

        # Clear selection before populating new data
        self.table.clearSelection()
        self.table.setRowCount(len(data))
        
        # Emit data availability status - check if we have ANY data (old or new)
        has_any_data = len(self.all_data) > 0
        self.data_availability_changed.emit(has_any_data)
        
        for row, coin in enumerate(data):
            self.add_table_row(row, coin)

    def add_table_row(self, row: int, coin: Dict):
        """Add a single row to the table for a coin."""

        # Add rank with UserRole data for selection
        rank_item = QTableWidgetItem(str(coin["rank"]))
        rank_item.setData(Qt.ItemDataRole.UserRole, coin)
        rank_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        items = [
            rank_item,
            QTableWidgetItem(f"{coin['name']} ({coin['symbol']})"),
            QTableWidgetItem(DataFormatter.format_price(coin["price"])),
            QTableWidgetItem(DataFormatter.format_percentage_change(coin["change_24h"])),
            QTableWidgetItem(DataFormatter.format_currency(coin["market_cap"]))
        ]

        # Numeric alignment
        items[2].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        items[3].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        items[4].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Color 24h change directly with QBrush
        change = coin.get("change_24h", 0)
        if change > 0:
            items[3].setForeground(QBrush(QColor("#16a34a")))  # green
        elif change < 0:
            items[3].setForeground(QBrush(QColor("#dc2626")))  # red
        else:
            items[3].setForeground(QBrush(QColor("#64748b")))  # neutral gray

        for col, item in enumerate(items):
            self.table.setItem(row, col, item)

    def on_header_clicked(self, column: int):
        # Clear selection when sorting
        self.table.clearSelection()
        
        if self.sort_column == column:
            self.sort_order = (
                Qt.SortOrder.DescendingOrder
                if self.sort_order == Qt.SortOrder.AscendingOrder
                else Qt.SortOrder.AscendingOrder
            )
        else:
            self.sort_column = column
            self.sort_order = Qt.SortOrder.AscendingOrder

        self.apply_sorting()
        sort_key_map = {0: "Rank", 1: "Name", 2: "Price", 3: "24h %", 4: "Market Cap"}
        self.status_update.emit(f"Sorted by {sort_key_map.get(column, 'Unknown')}", "info")

    def apply_sorting(self):
        """Sort current data based on selected column and order."""
        if not self.current_data:
            return
        reverse = self.sort_order == Qt.SortOrder.DescendingOrder
        sort_key_map = {0: "rank", 1: "name", 2: "price", 3: "change_24h", 4: "market_cap"}
        sort_key = sort_key_map.get(self.sort_column)
        if sort_key:
            self.current_data = sorted(self.current_data, key=lambda x: x[sort_key], reverse=reverse)
            self.populate_table(self.current_data)
            self.table.horizontalHeader().setSortIndicator(self.sort_column, self.sort_order)

    def on_selection_changed(self):
        """Emit signal with selected coin data."""
        selected_items = self.table.selectedItems()
        if selected_items:
            coin_data = selected_items[0].data(Qt.ItemDataRole.UserRole)
            self.coin_selected.emit(coin_data)

    def clear_selection(self):
        """Public method to clear table selection (for search, refresh, etc.)"""
        self.table.clearSelection()
        
    def has_data(self) -> bool:
        """Check if there's any data available for export."""
        return len(self.all_data) > 0