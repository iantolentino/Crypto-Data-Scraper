## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

* CoinGecko for providing the cryptocurrency data API
* PySide6 team for the Qt framework bindings
* mplfinance for candlestick charting capabilities

## Support

* Documentation: [https://docs.crypto-tracker.com](https://docs.crypto-tracker.com)
* Issues: [https://github.com/yourusername/crypto-tracker/issues](https://github.com/yourusername/crypto-tracker/issues)
* Discord: [https://discord.gg/crypto-tracker](https://discord.gg/crypto-tracker)

---

## CONTRIBUTING.md

````markdown
# Contributing to Crypto Tracker

Thank you for considering contributing to Crypto Tracker. This document outlines the process for contributing to the project.

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

## Getting Started

1. Fork the repository.
2. Clone your fork:

   ```bash
   git clone https://github.com/yourusername/crypto-tracker.git
   cd crypto-tracker
````

3. Set up the development environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements-dev.txt
   pre-commit install
   ```

4. Create a branch for your feature:

   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Code Standards

* Follow PEP 8 style guide
* Use type hints for all function signatures
* Write docstrings for all public functions and classes
* Maximum line length: 88 characters (Black default)
* Use meaningful variable names

### Testing Requirements

* Write unit tests for new functionality
* Maintain minimum 80% test coverage
* Run tests before submitting a PR:

  ```bash
  pytest tests/ --cov=crypto_tracker
  ```

### Commit Messages

Use conventional commit messages:

* feat: New feature
* fix: Bug fix
* docs: Documentation
* style: Code style
* refactor: Code refactoring
* test: Testing
* chore: Maintenance

Example:

```
feat: Add portfolio tracking feature

- Add portfolio model and database schema
- Implement portfolio view widget
- Add portfolio calculation logic
```

## Pull Request Process

* Update documentation for any changed features
* Add tests for new functionality
* Ensure all tests pass
* Update the README.md if needed
* Submit PR with a clear description of changes

## Project Structure

```text
crypto-tracker/
├── src/crypto_tracker/
│   ├── config/         # Configuration files
│   ├── models/         # Data models
│   ├── views/          # UI components
│   ├── controllers/    # Business logic
│   ├── services/       # External services
│   ├── workers/        # Background threads
│   └── utils/          # Utilities
├── tests/              # Test files
├── resources/          # Static resources
└── docs/               # Documentation
```

## Adding New Features

### Adding a New Cryptocurrency

* Add coin ID to `config/constants.py` `COINS` list
* Update tests to include new coin
* Verify API response structure matches model

### Adding New Chart Types

* Create new chart widget in `views/widgets/`
* Add chart type to chart controller
* Update UI to include new chart option
* Add tests for new chart type

### Adding New Views

* Create new view widget in `views/widgets/`
* Add view to main window stacked widget
* Implement view controller logic
* Add tests for view functionality

## Debugging

### Using Logging

```python
from crypto_tracker.utils.logger import get_logger

logger = get_logger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Qt Debugging

```python
import os
os.environ["QT_DEBUG_PLUGINS"] = "1"
```

## Release Process

* Update version in `setup.py` and `config/settings.py`

* Update `CHANGELOG.md`

* Create release branch

* Run full test suite

* Build distribution packages:

  ```bash
  python setup.py sdist bdist_wheel
  ```

* Create GitHub release with release notes

* Upload to PyPI:

  ```bash
  twine upload dist/*
  ```

## Code Review Guidelines

### What to Look For

* Code correctness and functionality
* Test coverage and quality
* Documentation completeness
* Performance implications
* Security considerations
* Error handling
* Code style compliance

### Review Process

* Automated checks must pass
* At least one maintainer approval required
* Address all review comments
* Squash commits before merge

## Questions

If you have questions about contributing:

* Open an issue with your question
* Join our Discord community
* Contact the maintainers directly

Thank you for contributing to Crypto Tracker.

````

---

## How to Test

### 1. Unit Tests

Create `tests/test_models.py`:

```python
import pytest
from decimal import Decimal
from crypto_tracker.models.coin import Coin, PriceChange

def test_coin_creation():
    coin_data = {
        "id": "bitcoin",
        "name": "Bitcoin",
        "symbol": "btc",
        "current_price": 50000,
        "market_cap": 1000000000,
        "total_volume": 50000000,
        "circulating_supply": 19000000,
        "total_supply": 21000000,
        "price_change_percentage_24h": 5.0,
        "price_change_percentage_7d_in_currency": 10.0
    }

    coin = Coin.from_api_response(coin_data)

    assert coin.id == "bitcoin"
    assert coin.name == "Bitcoin"
    assert coin.current_price == Decimal("50000")
    assert coin.price_change.day_24 == 5.0
    assert coin.formatted_price() == "$50,000.00"

def test_price_change_formats():
    change = PriceChange(day_24=5.5, day_7=-2.3)

    assert change.formatted_day_24() == "+5.50%"
    assert change.formatted_day_7() == "-2.30%"
    assert change.is_positive() is True
````

### 2. Integration Tests

Create `tests/test_api.py`:

```python
import pytest
from crypto_tracker.services.api_client import APIClient

def test_api_connection():
    client = APIClient()
    data = client.get_markets(vs_currency="usd", coin_ids=["bitcoin"])

    assert data is not None
    assert len(data) > 0
    assert data[0]["id"] == "bitcoin"

def test_ohlc_fetch():
    client = APIClient()
    data = client.get_ohlc("bitcoin", days=7)

    assert data is not None
    assert len(data) > 0
    assert len(data[0]) == 5
```

### 3. Run Tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
pytest --cov=crypto_tracker tests/ --cov-report=html
pytest tests/test_models.py -v
pytest tests/ -v --tb=short
```

### 4. Manual Testing Checklist

* Application starts without errors
* Market data loads within 5 seconds
* Table shows all 20+ cryptocurrencies
* Sorting works on all columns
* Search filters correctly by name and symbol
* Card view displays all coins
* Theme switching works without UI glitches
* Chart loads when clicking table rows
* Chart loads when clicking cards
* Auto-refresh updates data at correct intervals
* Icons load for all cards
* No UI freezes during data refresh
* Error handling works (simulate network failure)
* Window resize maintains layout
* Memory usage remains stable over time
