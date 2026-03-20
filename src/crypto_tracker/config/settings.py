"""
Application settings.
"""

import os
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from dotenv import load_dotenv

class Environment(Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"

class Theme(Enum):
    DARK = "dark"
    LIGHT = "light"

@dataclass
class Settings:
    app_name: str = "Crypto Tracker"
    app_version: str = "1.0.0"
    environment: Environment = Environment.DEVELOPMENT
    debug: bool = False
    api_base_url: str = "https://api.coingecko.com/api/v3"
    api_timeout: int = 20
    cache_ttl: int = 300
    theme: Theme = Theme.DARK
    log_level: str = "INFO"

settings = Settings()
