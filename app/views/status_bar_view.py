# status_bar_view.py
from PySide6.QtWidgets import QStatusBar, QLabel
from PySide6.QtCore import QTimer

class StatusBarView(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.message_label = QLabel("Ready")
        self.message_label.setObjectName("statusMessage")
        self.addWidget(self.message_label, 1)

        # Timer to auto-clear messages
        self._clear_timer = QTimer(self)
        self._clear_timer.setSingleShot(True)
        self._clear_timer.timeout.connect(self.clear_message)

    def show_message(self, text: str, status_type: str = None, timeout: int = 5000):
        """Show a status message with optional status type and auto-clear timeout."""
        self.message_label.setText(text)
        if status_type:
            self.message_label.setProperty("statusType", status_type)
        else:
            self.message_label.setProperty("statusType", None)

        # Refresh styles
        self.message_label.style().unpolish(self.message_label)
        self.message_label.style().polish(self.message_label)

        # Start/restart timer if timeout > 0
        if timeout > 0:
            self._clear_timer.start(timeout)

    def clear_message(self):
        """Reset the message to default 'Ready'."""
        self.show_message("Ready", status_type=None, timeout=0)
