"""
Application constants.
"""

COINS = [
    "bitcoin", "ethereum", "solana", "dogecoin", "cardano"
]

API_URL = "https://api.coingecko.com/api/v3/coins/markets"
MARKET_CHART_URL = "https://api.coingecko.com/api/v3/coins/{id}/ohlc"

REFRESH_OPTIONS = {"30s": 30000, "1m": 60000, "5m": 300000}
DEFAULT_REFRESH_LABEL = "1m"

TABLE_COLUMNS = [
    {"name": "Coin", "key": "name", "width": 150},
    {"name": "Price (USD)", "key": "current_price", "width": 120},
    {"name": "24h Change (%)", "key": "price_change_percentage_24h", "width": 120}
]

CHART_COLORS = {
    "dark": {"background": "#121212", "text": "white", "up": "lime", "down": "red"},
    "light": {"background": "white", "text": "black", "up": "green", "down": "red"}
}
