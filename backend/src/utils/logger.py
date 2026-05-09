"""
Logging utilities for CodeSurgeon.
"""

import logging
import sys
from pathlib import Path

from config import get_settings

# Create logs directory if it doesn't exist
log_dir = Path(__file__).parent.parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

# Get settings
settings = get_settings()

# Create logger
logger = logging.getLogger("codesurgeon")
logger.setLevel(getattr(logging, settings.log_level))

# Create formatters
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# File handler
file_handler = logging.FileHandler(log_dir / "app.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    """Get logger instance."""
    return logging.getLogger(f"codesurgeon.{name}")
