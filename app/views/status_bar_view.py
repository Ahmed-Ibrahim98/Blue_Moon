# status_bar_view.py
from PySide6.QtWidgets import QStatusBar, QLabel, QSizePolicy
from PySide6.QtCore import QTimer, Qt
import requests
from requests import RequestException

class StatusBarView(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        # ----- Temporary message label (left/main) -----
        self.message_label = QLabel("Ready")
        self.message_label.setObjectName("statusMessage")
        self.message_label.setProperty("statusType", "success")
        self.addWidget(self.message_label, 1)

        # Timer to auto-clear temporary messages
        self._clear_timer = QTimer(self)
        self._clear_timer.setSingleShot(True)
        self._clear_timer.timeout.connect(self.clear_message)

        # ----- Permanent network status label (far-right) -----
        self.network_label = QLabel("Checking…")
        self.network_label.setObjectName("networkStatus")
        self.network_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)

        # Use a compact policy so it doesn't take the main area
        self.network_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        # Add as permanent widget (no stretch) so it stays at the far-right
        self.addPermanentWidget(self.network_label)

        # Timer to check network every 3 seconds
        self._network_timer = QTimer(self)
        self._network_timer.timeout.connect(self.update_network_status)
        self._network_timer.start(3000)  # check every 3 seconds

        # Initial network check
        self.update_network_status()

    # ----- Temporary messages -----
    def show_message(self, text: str, status_type: str = None, timeout: int = 5000):
        """Show a status message with optional type (success/error/warning) and auto-clear timeout."""
        self.message_label.setText(text)
        if status_type:
            self.message_label.setProperty("statusType", status_type)
        else:
            self.message_label.setProperty("statusType", None)

        # Refresh QSS style for the message label
        self.message_label.style().unpolish(self.message_label)
        self.message_label.style().polish(self.message_label)

        # Start/restart auto-clear timer
        if timeout > 0:
            self._clear_timer.start(timeout)

    def clear_message(self):
        """Reset the temporary message to default 'Ready'."""
        # use timeout=0 so clear doesn't restart the timer
        self.show_message("Ready", status_type="success", timeout=0)

    # ----- Permanent network status -----
    def update_network_status(self):
        """Check internet connectivity and update the network label."""
        # Choose the host you prefer for the check; keep timeout very short.
        try:
            requests.get("https://www.google.com", timeout=2)
            self.network_label.setText("Online")
            self.network_label.setProperty("statusType", "success")
        except RequestException:
            self.network_label.setText("Offline")
            self.network_label.setProperty("statusType", "error")

        # force style refresh on the network label so the QSS [statusType=...] rules are applied immediately
        self.network_label.style().unpolish(self.network_label)
        self.network_label.style().polish(self.network_label)
