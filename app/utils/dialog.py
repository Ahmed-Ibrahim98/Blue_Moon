# app/utils/dialog.py
from PySide6.QtWidgets import QFileDialog, QCheckBox, QVBoxLayout, QDialog, QDialogButtonBox
from PySide6.QtCore import QDateTime

class ExportDialog(QDialog):
    """Dialog for exporting data with options."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Export Data")

        # Checkbox for raw data export
        self.raw_checkbox = QCheckBox("Export raw data (no formatting)")
        self.raw_checkbox.setChecked(False)

        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.raw_checkbox)
        layout.addWidget(buttons)

    def get_options(self):
        """Returns chosen file path + raw export flag."""
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd_HH-mm")
        suggested_name = f"coins_{timestamp}.csv"

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save CSV File",
            suggested_name,
            "CSV Files (*.csv)"
        )
        return file_path, self.raw_checkbox.isChecked()
