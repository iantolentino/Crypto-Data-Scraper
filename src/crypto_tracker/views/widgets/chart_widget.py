"""Chart widget for candlestick visualization."""

import pandas as pd
import mplfinance as mpf
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel
from PySide6.QtCore import Qt

from crypto_tracker.utils.logger import get_logger


class ChartCanvas(FigureCanvas):
    """Matplotlib canvas for chart rendering."""
    
    def __init__(self, parent=None, width=8, height=4, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.figure)
        self.setParent(parent)
        self.figure.patch.set_facecolor("#121212")
        self.setMinimumHeight(300)
    
    def clear(self):
        """Clear the canvas."""
        self.figure.clear()


class ChartWidget(QWidget):
    """Widget for displaying candlestick charts."""
    
    def __init__(self):
        super().__init__()
        self.logger = get_logger(__name__)
        self.current_data = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup chart widget UI."""
        layout = QVBoxLayout()
        
        # Chart controls
        controls = QHBoxLayout()
        controls.addWidget(QLabel("Chart:"))
        self.range_combo = QComboBox()
        self.range_combo.addItems(["7 Days", "30 Days", "90 Days", "365 Days"])
        self.range_combo.setCurrentText("30 Days")
        controls.addWidget(self.range_combo)
        controls.addStretch()
        layout.addLayout(controls)
        
        # Canvas
        self.canvas = ChartCanvas(self, width=9, height=5, dpi=100)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
    
    def draw_candlestick(self, df, coin_name, days):
        """
        Draw candlestick chart.
        
        Args:
            df: DataFrame with OHLC data
            coin_name: Name of the coin
            days: Number of days
        """
        try:
            self.current_data = (df, coin_name, days)
            self.canvas.clear()
            ax = self.canvas.figure.add_subplot(111)
            
            # Configure colors for dark theme
            self.canvas.figure.patch.set_facecolor("#121212")
            ax.set_facecolor("#121212")
            ax.tick_params(colors="white")
            ax.title.set_color("white")
            
            # Configure candlestick colors
            mc = mpf.make_marketcolors(up="lime", down="red", inherit=True)
            style = mpf.make_mpf_style(
                base_mpf_style="nightclouds",
                marketcolors=mc,
                gridcolor="#2c2c2c"
            )
            
            # Plot
            mpf.plot(
                df,
                type="candle",
                ax=ax,
                style=style,
                datetime_format="%m-%d",
                show_nontrading=True,
                volume=False
            )
            
            ax.set_title(f"{coin_name} — {days} days Candlestick Chart")
            self.canvas.draw()
            
            self.logger.debug(f"Drew chart for {coin_name}")
            
        except Exception as e:
            self.logger.exception(f"Error drawing chart: {e}")
            self.show_error_message(str(e))
    
    def show_error_message(self, message):
        """Show error message on chart."""
        self.canvas.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.text(0.5, 0.5, f"Error loading chart:\n{message}", 
                ha="center", va="center", color="red", fontsize=12)
        ax.set_facecolor("#121212")
        self.canvas.draw()
