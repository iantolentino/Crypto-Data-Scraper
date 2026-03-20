"""
Simple tests to verify the application works.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_imports():
    """Test that all major modules can be imported."""
    from crypto_tracker.config import TABLE_COLUMNS, COINS
    from crypto_tracker.models import Coin
    from crypto_tracker.utils import get_logger
    
    assert len(COINS) > 0
    assert len(TABLE_COLUMNS) > 0
    assert Coin is not None
    assert get_logger is not None


def test_config():
    """Test configuration loading."""
    from crypto_tracker.config import Settings
    settings = Settings()
    assert settings.app_name == "Crypto Tracker"


@pytest.mark.skip(reason="Requires Qt and GUI")
def test_gui_import():
    """Test GUI components can be imported."""
    from crypto_tracker.views import MainWindow
    from crypto_tracker.views.widgets import TableWidget, ChartWidget
    
    assert MainWindow is not None
    assert TableWidget is not None
    assert ChartWidget is not None


def test_coin_model():
    """Test coin model creation."""
    from crypto_tracker.models import Coin
    from decimal import Decimal
    
    test_data = {
        "id": "test",
        "name": "Test Coin",
        "symbol": "test",
        "current_price": 100.0,
        "price_change_percentage_24h": 5.0
    }
    
    coin = Coin.from_api_response(test_data)
    assert coin.id == "test"
    assert coin.name == "Test Coin"
    assert coin.current_price == Decimal("100.0")
