"""
Pytest configuration and fixtures.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from crypto_tracker.config.settings import Settings
from crypto_tracker.views.styles.theme_manager import ThemeManager


@pytest.fixture
def settings():
    """Provide test settings."""
    settings = Settings()
    settings.debug = True
    return settings


@pytest.fixture
def theme_manager():
    """Provide theme manager."""
    return ThemeManager()


@pytest.fixture
def sample_coin_data():
    """Provide sample coin data for testing."""
    return [
        {
            "id": "bitcoin",
            "name": "Bitcoin",
            "symbol": "btc",
            "current_price": 50000.0,
            "market_cap": 1000000000000.0,
            "total_volume": 50000000000.0,
            "circulating_supply": 19000000.0,
            "total_supply": 21000000.0,
            "price_change_percentage_24h": 5.5,
            "price_change_percentage_7d_in_currency": 10.2,
            "image": "https://example.com/bitcoin.png"
        },
        {
            "id": "ethereum",
            "name": "Ethereum",
            "symbol": "eth",
            "current_price": 3000.0,
            "market_cap": 350000000000.0,
            "total_volume": 20000000000.0,
            "circulating_supply": 120000000.0,
            "total_supply": None,
            "price_change_percentage_24h": -2.3,
            "price_change_percentage_7d_in_currency": -5.1,
            "image": "https://example.com/ethereum.png"
        }
    ]


@pytest.fixture
def sample_ohlc_data():
    """Provide sample OHLC data for testing."""
    return [
        [1700000000000, 50000, 51000, 49000, 50500],
        [1700003600000, 50500, 51500, 50000, 51200],
        [1700007200000, 51200, 52000, 50800, 51800],
    ]
