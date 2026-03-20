# Crypto Tracker – Enterprise Cryptocurrency Market Analysis Tool

A professional-grade desktop application for tracking cryptocurrency prices, analyzing market trends, and visualizing candlestick charts with real-time data from CoinGecko API.

## Features

* Real-time cryptocurrency price tracking for 20+ major cryptocurrencies
* Interactive candlestick charts with configurable time ranges (7, 30, 90, 365 days)
* Dual view modes: table view for detailed data and card view for visual overview
* Search and filter functionality across coin names and symbols
* Automatic data refresh with configurable intervals (30s, 1m, 5m, 10m)
* Light and dark theme support with persistent preferences
* Non-blocking background data fetching for smooth UI experience
* Local caching of market data and charts for improved performance
* Comprehensive error handling and logging

## System Requirements

* Python 3.9 or higher
* PySide6 6.5+
* Internet connection for API access
* 4GB RAM minimum (8GB recommended)
* 100MB free disk space

## Installation

### Development Environment

1. Clone the repository:

```bash
git clone https://github.com/yourusername/crypto-tracker.git
cd crypto-tracker
```

2. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment:

```bash
cp .env.example .env
# Edit .env with your preferences
```

### Production Installation

```bash
pip install crypto-tracker

docker build -t crypto-tracker .
docker run -d --name crypto-tracker -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix crypto-tracker
```

## Usage

### Running the Application

```bash
python -m crypto_tracker.main
```

Or if installed via pip:

```bash
crypto-tracker
```

### Interface Overview

**Top Controls**

* Search Bar: Filter coins by name or symbol
* Chart Range: Select candlestick time period (7, 30, 90, 365 days)
* Auto-refresh: Set automatic data update interval
* View Toggle: Switch between table and card views
* Theme Toggle: Switch between light and dark themes
* Refresh Button: Manually update market data

**Table View**

* Sortable columns for all metrics
* Color-coded price changes (green = positive, red = negative)
* Click any row to load chart for that coin

**Card View**

* Visual representation with coin icons
* Quick view of price and 24h change
* Click any card to load chart

**Chart View**

* Interactive candlestick charts
* Automatic theme adaptation
* Real-time chart updates on coin selection

## Customizing Coins

Edit `src/crypto_tracker/config/constants.py` to modify the list of tracked cryptocurrencies:

```python
COINS = [
    "bitcoin",
    "ethereum",
    # Add more coin IDs from CoinGecko
]
```

## Testing

### Running Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest tests/

# Run with coverage
pytest --cov=crypto_tracker tests/

# Run specific test file
pytest tests/test_models.py
```

### Test Coverage Requirements

* Unit tests: 80% minimum coverage
* Integration tests: All API endpoints
* UI tests: Critical user workflows

## Architecture

### Component Structure

```text
crypto-tracker/
├── src/crypto_tracker/
│   ├── config/         # Configuration management
│   ├── models/         # Data models (Coin, MarketData)
│   ├── views/          # UI components (Table, Cards, Chart)
│   ├── controllers/    # Business logic
│   ├── services/       # External services (API, Cache)
│   ├── workers/        # Background threads
│   └── utils/          # Utilities (logging, validation)
├── tests/              # Unit and integration tests
├── resources/          # Static resources (themes, icons)
└── docs/               # Documentation
```

### Data Flow

* User interacts with UI components
* Controllers handle business logic
* Services fetch data via API with caching
* Workers manage background operations
* Models represent and validate data
* Views update based on controller signals

## API Integration

**Source:** CoinGecko API

**Endpoints**

* `/coins/markets` – Current market data
* `/coins/{id}/ohlc` – Historical OHLC data

**Rate Limiting**

* 1 request per second

**Caching**

* 5 minutes for market data
* 1 hour for charts

## Performance Optimization

* Threading: All network operations run in background threads
* Caching: Multi-level cache with TTL expiration
* Icon Loading: Batch processing with lazy loading
* UI Rendering: Virtual scrolling for table, lazy card loading
* Memory Management: Automatic cache cleanup, weak references

## Security

* No API keys required for CoinGecko public endpoints
* Input validation on all user inputs
* Network timeouts to prevent hanging
* Exception handling with logging

## Troubleshooting

### Common Issues

**No data showing**

* Check internet connection
* Verify CoinGecko API is accessible
* Check firewall settings

**Slow performance**

* Clear cache: Delete `~/.cache/crypto-tracker/`
* Reduce number of tracked coins
* Increase cache TTL

**UI freezes**

* Check thread count in task manager
* Reduce auto-refresh frequency
* Update graphics drivers

## Logs

Log files are stored at:

* Linux: `~/.local/share/crypto-tracker/logs/`
* macOS: `~/Library/Logs/crypto-tracker/`
* Windows: `%APPDATA%\crypto-tracker\logs/`
