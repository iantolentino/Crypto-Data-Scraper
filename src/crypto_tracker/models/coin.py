"""Coin data model."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class PriceChange:
    """Price change percentages."""
    day_24: Optional[float] = None
    day_7: Optional[float] = None


@dataclass
class Coin:
    """Cryptocurrency data model."""
    
    id: str
    name: str
    symbol: str
    current_price: Decimal
    market_cap: Decimal = Decimal("0")
    total_volume: Decimal = Decimal("0")
    circulating_supply: Decimal = Decimal("0")
    total_supply: Optional[Decimal] = None
    price_change: PriceChange = None
    
    def __post_init__(self):
        if self.price_change is None:
            self.price_change = PriceChange()
    
    @classmethod
    def from_api_response(cls, data: dict) -> "Coin":
        """Create Coin instance from API response."""
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            symbol=data.get("symbol", "").upper(),
            current_price=Decimal(str(data.get("current_price", 0))),
            market_cap=Decimal(str(data.get("market_cap", 0))),
            total_volume=Decimal(str(data.get("total_volume", 0))),
            circulating_supply=Decimal(str(data.get("circulating_supply", 0))),
            total_supply=Decimal(str(data.get("total_supply"))) if data.get("total_supply") else None,
            price_change=PriceChange(
                day_24=data.get("price_change_percentage_24h"),
                day_7=data.get("price_change_percentage_7d_in_currency")
            )
        )
