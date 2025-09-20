from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QBrush
from typing import List, Tuple, Optional


class ChartWidget(QWidget):
    """A custom QWidget to display a 7-day price chart for a cryptocurrency.
    Supports light/dark themes and hover tooltips."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data: Optional[Tuple[List[str], List[float]]] = None
        self.coin_name: str = ""
        self.is_dark: bool = False
        self.setMinimumSize(400, 300)
        self.setMouseTracking(True)
        self.hover_index: int = -1
        self.points: List[QPointF] = []
        
        # Set tooltip style
        self.setStyleSheet("""
            QToolTip {
                background-color: #1e40af;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
                border: 1px solid #3b82f6;
                font-size: 11px;
                font-weight: 500;
            }
        """)
        
    def set_chart_data(self, timestamps: List[str], prices: List[float], coin_name: str) -> None:
        """Set the chart data to display."""
        if not timestamps or not prices or len(timestamps) != len(prices):
            print("Invalid chart data received")
            return
            
        self.data = (timestamps, prices)
        self.coin_name = coin_name
        self.points = []
        self.hover_index = -1
        self.update()
        
    def set_theme(self, is_dark: bool) -> None:
        """Set the theme (light/dark mode)."""
        self.is_dark = is_dark
        self.update()
        
    def mouseMoveEvent(self, event) -> None:
        """Handle mouse movement for hover effects."""
        if not self.data or not self.points:
            return
            
        # Find closest point to mouse
        min_dist = float('inf')
        closest_index = -1
        
        for i, point in enumerate(self.points):
            dist = (event.position().x() - point.x()) ** 2 + (event.position().y() - point.y()) ** 2
            if dist < min_dist:
                min_dist = dist
                closest_index = i
        
        # Show tooltip if close enough to a point
        if closest_index != -1 and min_dist < 400:
            self.hover_index = closest_index
            timestamps, prices = self.data
            tooltip_text = f"Date: {timestamps[closest_index]}\nPrice: ${prices[closest_index]:.6f}"  # Show more decimals for stablecoins
            self.setToolTip(tooltip_text)
        else:
            self.hover_index = -1
            self.setToolTip("")
            
        self.update()
        
    def leaveEvent(self, event) -> None:
        """Handle mouse leaving the widget."""
        self.hover_index = -1
        self.setToolTip("")
        self.update()
        
    def paintEvent(self, event) -> None:
        """Paint the chart on the widget."""
        if not self.data:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Get data with validation
        timestamps, prices = self.data
        if not timestamps or not prices or len(timestamps) != len(prices):
            return
        
        # Draw the chart
        self.points = self._draw_chart(painter, timestamps, prices)
        painter.end()

    def _draw_chart(self, painter: QPainter, timestamps: List[str], prices: List[float]) -> List[QPointF]:
        """Internal method to draw the chart."""
        # Setup colors based on theme
        if self.is_dark:
            bg_color = QColor("#1e293b")
            text_color = QColor("#e2e8f0")
            grid_color = QColor("#475569")
            line_color = QColor("#60a5fa")
            hover_color = QColor("#90cdf4")
            stablecoin_line_color = QColor("#94a3b8")
        else:
            bg_color = QColor("#ffffff")
            text_color = QColor("#1a2a3a")
            grid_color = QColor("#adb5be")
            line_color = QColor("#2c5bdc")
            hover_color = QColor("#2563eb")
            stablecoin_line_color = QColor("#64748b")
        
        # Fill background
        painter.fillRect(0, 0, self.width(), self.height(), bg_color)
        
        # Calculate required margin for Y-axis labels
        font = QFont()
        font.setPointSize(8)
        painter.setFont(font)
        
        # STABLECOIN DETECTION - Check if this is essentially a stablecoin
        is_stablecoin = False
        if len(prices) > 1:
            price_range_val = max(prices) - min(prices)
            avg_price = sum(prices) / len(prices)
            # If price moves less than 2% total and average is near $1, treat as stablecoin
            if price_range_val < 0.02 and 0.98 < avg_price < 1.02:
                is_stablecoin = True
        
        if is_stablecoin:
            # For stablecoins, use a fixed range around $1.00
            min_price = 0.995  # Show from $0.995
            max_price = 1.005  # to $1.005
            price_range = max_price - min_price
            
            # Draw stablecoin indicator line at $1.00
            dash_pen = QPen(stablecoin_line_color, 1, Qt.PenStyle.DashLine)
            painter.setPen(dash_pen)
        else:
            # Normal price calculation
            try:
                min_price = min(prices)
                max_price = max(prices)
                price_range = max(max_price - min_price, 0.001)  # Avoid division by zero
            except (ValueError, TypeError):
                return []
        
        # Calculate maximum label width needed for Y-axis
        max_label_width = 0
        for i in range(5):
            price_val = min_price + (i / 4) * price_range
            if is_stablecoin:
                label_text = f"${price_val:.3f}"  # Show 3 decimals for stablecoins
            else:
                label_text = f"${price_val:,.2f}"
            text_width = painter.fontMetrics().horizontalAdvance(label_text)
            max_label_width = max(max_label_width, text_width)
        
        # Add padding to the calculated width
        y_axis_margin = max_label_width + 20  # 20px padding
        
        # Calculate chart area with dynamic margins
        margin_top = 50
        margin_bottom = 50
        margin_left = y_axis_margin  # Dynamic left margin based on label width
        margin_right = 20
        
        chart_rect = QRectF(margin_left, margin_top, 
                           self.width() - margin_left - margin_right, 
                           self.height() - margin_top - margin_bottom)
        
        if chart_rect.width() <= 0 or chart_rect.height() <= 0:
            return []
            
        # Draw stablecoin indicator line if applicable
        if is_stablecoin:
            center_y = chart_rect.bottom() - ((1.0 - min_price) / price_range) * chart_rect.height()
            painter.drawLine(chart_rect.left(), center_y, chart_rect.right(), center_y)
            
        # Draw grid
        grid_pen = QPen(grid_color, 1, Qt.PenStyle.DotLine)
        painter.setPen(grid_pen)
        
        # Horizontal grid lines
        for i in range(5):
            y = chart_rect.bottom() - (i / 4) * chart_rect.height()
            painter.drawLine(chart_rect.left(), y, chart_rect.right(), y)
            
        # Vertical grid lines - only if we have reasonable data
        if len(timestamps) > 1:
            for i in range(len(timestamps)):
                x = chart_rect.left() + (i / (len(timestamps) - 1)) * chart_rect.width()
                painter.drawLine(x, chart_rect.top(), x, chart_rect.bottom())
        
        # Draw price labels with proper alignment
        painter.setPen(text_color)
        
        for i in range(5):
            """this loop draws the Y-axis price labels"""
            price_val = min_price + (i / 4) * price_range
            y = chart_rect.bottom() - (i / 4) * chart_rect.height()
            
            # Format label based on whether it's a stablecoin
            if is_stablecoin:
                label_text = f"${price_val:.3f}"  # Show 3 decimals for stablecoins
            else:
                label_text = f"${price_val:,.2f}"
                
            # Draw label with right alignment within the left margin
            text_rect = QRectF(0, y - 10, margin_left - 5, 20)
            painter.drawText(text_rect, 
                            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                            label_text)
        
        # Draw date labels - with bounds checking
        for i, date_str in enumerate(timestamps):
            if i >= len(timestamps):  # Safety check
                break
            x = chart_rect.left() + (i / max(len(timestamps) - 1, 1)) * chart_rect.width()
            painter.drawText(QRectF(x - 25, chart_rect.bottom() + 5, 50, 20),
                            Qt.AlignmentFlag.AlignCenter,
                            str(date_str)[:10])  # Limit string length
        
        # Draw price line and store points for hover detection
        line_pen = QPen(line_color, 2)
        painter.setPen(line_pen)
        
        points = []
        for i, price in enumerate(prices):
            if i >= len(prices):  # Safety check
                break
            x = chart_rect.left() + (i / max(len(prices) - 1, 1)) * chart_rect.width()
            y = chart_rect.bottom() - ((price - min_price) / price_range) * chart_rect.height()
            point = QPointF(x, y)
            points.append(point)
            
        # Draw the line with bounds checking
        for i in range(len(points) - 1):
            if i + 1 < len(points):
                painter.drawLine(points[i], points[i + 1])
        
        # Draw data points
        point_pen = QPen(line_color, 2)
        painter.setPen(point_pen)
        
        for i, point in enumerate(points):
            if i >= len(points):  # Safety check
                break
            # Draw larger point for hover
            if i == self.hover_index:
                painter.setBrush(QBrush(hover_color))
                painter.drawEllipse(point, 6, 6)
            else:
                painter.setBrush(QBrush(line_color))
                painter.drawEllipse(point, 3, 3)
        
        # Draw title with stablecoin indicator if applicable
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(text_color)

        # Set title with stablecoin note if applicable
        title = f"{self.coin_name} - 7-Day Price (USD)"
        if is_stablecoin:
            title += " (Stablecoin)"
            
        title = title[:50]  # Limit title length
        painter.drawText(QRectF(0, 10, self.width(), 30),
                        Qt.AlignmentFlag.AlignCenter,
                        title)
        
        return points