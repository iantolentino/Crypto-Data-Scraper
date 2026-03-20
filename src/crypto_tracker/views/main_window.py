"""Main window for Crypto Tracker."""

import requests
import pandas as pd
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel, 
    QPushButton, QApplication, QMessageBox, QSplitter
)
from PySide6.QtCore import Qt

from crypto_tracker.views.widgets.table_widget import TableWidget
from crypto_tracker.views.widgets.chart_widget import ChartWidget
from crypto_tracker.utils.logger import get_logger


class MainWindow(QWidget):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.logger = get_logger(__name__)
        self.setWindowTitle("Crypto Tracker")
        self.resize(1200, 800)
        
        # Center window on screen
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.center() - self.rect().center())
        
        # Setup UI
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("Crypto Tracker - Live Prices with Candlestick Charts")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title)
        
        # Create splitter for table and chart
        splitter = QSplitter(Qt.Vertical)
        
        # Table
        self.table = TableWidget()
        splitter.addWidget(self.table)
        
        # Chart
        self.chart = ChartWidget()
        splitter.addWidget(self.chart)
        
        # Set initial sizes (60% table, 40% chart)
        splitter.setSizes([480, 320])
        
        main_layout.addWidget(splitter)
        
        # Refresh button
        self.refresh_btn = QPushButton("Refresh Data")
        self.refresh_btn.clicked.connect(self.load_data)
        main_layout.addWidget(self.refresh_btn)
        
        # Status
        self.status_label = QLabel("Ready")
        main_layout.addWidget(self.status_label)
        
        self.setLayout(main_layout)
        
        # Connect table click to chart
        self.table.cellClicked.connect(self.on_table_click)
        
        # Load initial data
        self.load_data()
        
        self.logger.info("Main window initialized")
    
    def load_data(self):
        """Load real cryptocurrency data from CoinGecko API."""
        self.status_label.setText("Fetching live cryptocurrency data...")
        self.refresh_btn.setEnabled(False)
        
        # List of cryptocurrencies to track
        coins = [
            "bitcoin", "ethereum", "solana", "dogecoin", "cardano", "ripple",
            "polkadot", "litecoin", "tron", "polygon", "avalanche-2", "chainlink",
            "uniswap", "stellar", "internet-computer", "vechain", "cosmos",
            "filecoin", "aptos", "arbitrum"
        ]
        
        try:
            # Fetch from CoinGecko API
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                "vs_currency": "usd",
                "ids": ",".join(coins),
                "price_change_percentage": "24h,7d"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Populate the table with real data
            self.table.populate_data(data)
            self.status_label.setText(f"Updated: {len(data)} cryptocurrencies loaded. Click any coin to view chart.")
            self.logger.info(f"Loaded {len(data)} cryptocurrencies")
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to fetch data: {e}"
            self.status_label.setText(error_msg)
            QMessageBox.warning(self, "API Error", error_msg)
            self.logger.error(error_msg)
            
        except Exception as e:
            error_msg = f"Error: {e}"
            self.status_label.setText(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
            self.logger.exception(error_msg)
            
        finally:
            self.refresh_btn.setEnabled(True)
    
    def on_table_click(self, row, column):
        """Handle table cell click to load chart."""
        # Get coin ID from the clicked row
        coin_id = self.table.get_coin_id_at_row(row)
        if coin_id:
            self.load_chart(coin_id)
    
    def load_chart(self, coin_id):
        """Load candlestick chart for selected coin."""
        self.status_label.setText(f"Loading chart for {coin_id}...")
        
        try:
            # Fetch OHLC data from API
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"
            params = {"vs_currency": "usd", "days": 30}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                self.status_label.setText(f"No chart data available for {coin_id}")
                return
            
            # Convert to DataFrame
            df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df.set_index("timestamp", inplace=True)
            
            # Get coin name
            coin_name = self.table.get_coin_name_at_row(self.table.currentRow())
            
            # Draw chart
            self.chart.draw_candlestick(df, coin_name, 30)
            self.status_label.setText(f"Showing 30-day candlestick chart for {coin_name}")
            
        except Exception as e:
            error_msg = f"Failed to load chart: {e}"
            self.status_label.setText(error_msg)
            QMessageBox.warning(self, "Chart Error", error_msg)
            self.logger.error(error_msg)
