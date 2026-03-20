"""Table widget for cryptocurrency data."""

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from crypto_tracker.models.coin import Coin
from crypto_tracker.utils.logger import get_logger


class TableWidget(QTableWidget):
    """Custom table widget for cryptocurrency data."""
    
    def __init__(self):
        super().__init__()
        self.logger = get_logger(__name__)
        self.coin_data = {}
        self.setup_table()
    
    def setup_table(self):
        """Initialize table configuration."""
        # Define columns
        columns = [
            "Coin", "Price (USD)", "Market Cap", "24h Change (%)",
            "7d Change (%)", "24h Volume", "Circulating Supply", "Total Supply"
        ]
        
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
    
    def populate_data(self, coins_data):
        """Populate table with coin data."""
        self.setSortingEnabled(False)
        self.clearContents()
        self.setRowCount(len(coins_data))
        self.coin_data.clear()
        
        for row, coin_dict in enumerate(coins_data):
            coin = Coin.from_api_response(coin_dict)
            self.coin_data[coin.id] = coin
            
            # Coin name with ID stored
            name_item = QTableWidgetItem(f"{coin.name} ({coin.symbol})")
            name_item.setData(Qt.UserRole, coin.id)
            name_item.setData(Qt.UserRole + 1, coin.name)  # Store name too
            self.setItem(row, 0, name_item)
            
            # Price
            price_item = QTableWidgetItem(f"${coin.current_price:,.2f}")
            price_item.setData(Qt.EditRole, float(coin.current_price))
            self.setItem(row, 1, price_item)
            
            # Market Cap
            if coin.market_cap > 0:
                mcap_item = QTableWidgetItem(f"${coin.market_cap:,.0f}")
                mcap_item.setData(Qt.EditRole, float(coin.market_cap))
                self.setItem(row, 2, mcap_item)
            else:
                self.setItem(row, 2, QTableWidgetItem("N/A"))
            
            # 24h Change
            if coin.price_change.day_24 is not None:
                pct24_item = QTableWidgetItem(f"{coin.price_change.day_24:+.2f}%")
                pct24_item.setData(Qt.EditRole, coin.price_change.day_24)
                if coin.price_change.day_24 >= 0:
                    pct24_item.setForeground(QColor("green"))
                else:
                    pct24_item.setForeground(QColor("red"))
                self.setItem(row, 3, pct24_item)
            else:
                self.setItem(row, 3, QTableWidgetItem("N/A"))
            
            # 7d Change
            if coin.price_change.day_7 is not None:
                pct7_item = QTableWidgetItem(f"{coin.price_change.day_7:+.2f}%")
                pct7_item.setData(Qt.EditRole, coin.price_change.day_7)
                if coin.price_change.day_7 >= 0:
                    pct7_item.setForeground(QColor("green"))
                else:
                    pct7_item.setForeground(QColor("red"))
                self.setItem(row, 4, pct7_item)
            else:
                self.setItem(row, 4, QTableWidgetItem("N/A"))
            
            # Volume
            if coin.total_volume > 0:
                vol_item = QTableWidgetItem(f"${coin.total_volume:,.0f}")
                vol_item.setData(Qt.EditRole, float(coin.total_volume))
                self.setItem(row, 5, vol_item)
            else:
                self.setItem(row, 5, QTableWidgetItem("N/A"))
            
            # Circulating Supply
            if coin.circulating_supply > 0:
                supply_item = QTableWidgetItem(f"{coin.circulating_supply:,.0f}")
                supply_item.setData(Qt.EditRole, float(coin.circulating_supply))
                self.setItem(row, 6, supply_item)
            else:
                self.setItem(row, 6, QTableWidgetItem("N/A"))
            
            # Total Supply
            if coin.total_supply:
                total_item = QTableWidgetItem(f"{coin.total_supply:,.0f}")
                total_item.setData(Qt.EditRole, float(coin.total_supply))
                self.setItem(row, 7, total_item)
            else:
                self.setItem(row, 7, QTableWidgetItem("∞"))
        
        self.setSortingEnabled(True)
        self.logger.debug(f"Populated {len(coins_data)} coins")
    
    def get_coin_id_at_row(self, row):
        """Get coin ID at specified row."""
        item = self.item(row, 0)
        if item:
            return item.data(Qt.UserRole)
        return None
    
    def get_coin_name_at_row(self, row):
        """Get coin name at specified row."""
        item = self.item(row, 0)
        if item:
            return item.text().split(" (")[0]  # Extract name before the symbol
        return None
