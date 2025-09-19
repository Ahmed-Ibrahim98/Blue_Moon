# app/views/table_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QBrush
from typing import List, Dict
from ..logic.data_controller import DataController
from ..utils.formatting import DataFormatter

class TableView(QWidget):
    coin_selected = Signal(dict)

    def __init__(self, data_controller: DataController, parent=None):
        super().__init__(parent)
        self.data_controller = data_controller
        self.setObjectName("coinsTable")

        # Store both full dataset and filtered/visible data
        self.all_data: List[Dict] = []
        self.current_data: List[Dict] = []

        self.sort_column = 0  # Default: Rank
        self.sort_order = Qt.SortOrder.AscendingOrder

        self.setup_ui()
        self.refresh_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setObjectName("cryptoTable")
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Rank", "Name (Symbol)", "Price", "24h %", "Market Cap"])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.sectionClicked.connect(self.on_header_clicked)

        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)

        layout.addWidget(self.table)

    def refresh_data(self):
        """Fetches fresh data from the controller and repopulates the table."""
        data = self.data_controller.fetch_top_coins()
        if data:
            self.all_data = data  # keep full dataset
            self.current_data = list(self.all_data)  # working copy for filtering/sorting
            self.apply_sorting()

    def populate_table(self, data: List[Dict]):
        self.table.setRowCount(len(data))
        for row, coin in enumerate(data):
            self.add_table_row(row, coin)

    def add_table_row(self, row: int, coin: Dict):
        # Store the raw coin data in the first item of the row for easy access
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
        
        # Set alignment for numeric columns
        items[2].setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        items[3].setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        items[4].setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        # Color code the 24h change
        change = coin.get("change_24h", 0)
        if change > 0:
            items[3].setForeground(QBrush(QColor('#16a34a'))) # Green
        elif change < 0:
            items[3].setForeground(QBrush(QColor('#dc2626'))) # Red
        
        for col, item in enumerate(items):
            self.table.setItem(row, col, item)

    def on_header_clicked(self, column: int):
        if self.sort_column == column:
            self.sort_order = Qt.SortOrder.DescendingOrder if self.sort_order == Qt.SortOrder.AscendingOrder else Qt.SortOrder.AscendingOrder
        else:
            self.sort_column = column
            self.sort_order = Qt.SortOrder.AscendingOrder
        
        self.apply_sorting()

    def apply_sorting(self):
        """Sort only the currently visible (filtered) data, not the full dataset."""
        if not self.current_data:
            return
        
        reverse = (self.sort_order == Qt.SortOrder.DescendingOrder)
        sort_key_map = {
            0: "rank",
            1: "name",
            2: "price",
            3: "change_24h",
            4: "market_cap"
        }
        
        sort_key = sort_key_map.get(self.sort_column)
        if sort_key:
            self.current_data = sorted(self.current_data, key=lambda x: x[sort_key], reverse=reverse)
            self.populate_table(self.current_data)
            self.table.horizontalHeader().setSortIndicator(self.sort_column, self.sort_order)

    def on_selection_changed(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            # Retrieve data from the first item in the selected row
            coin_data = selected_items[0].data(Qt.ItemDataRole.UserRole)
            self.coin_selected.emit(coin_data)
