#!/usr/bin/env python3
"""
Main application entry point for Crypto Tracker.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path if needed
sys.path.insert(0, str(Path(__file__).parent))

from PySide6.QtWidgets import QApplication
from crypto_tracker.views.main_window import MainWindow
from crypto_tracker.utils.logger import get_logger


def main():
    """Main application entry point."""
    logger = get_logger(__name__)
    logger.info("Starting Crypto Tracker application")
    
    app = QApplication(sys.argv)
    app.setApplicationName("Crypto Tracker")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
