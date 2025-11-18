"""
Logging configuration for Panoptes Scout.

Provides structured logging for observability throughout the scout pipeline.
This is a required feature area for the hackathon submission.
"""

import logging
import sys
from typing import Optional


def configure_logging(level: Optional[int] = None) -> logging.Logger:
    """
    Configure and return the Panoptes Scout logger.

    Args:
        level: Logging level (e.g., logging.INFO, logging.DEBUG).
               Defaults to logging.INFO.

    Returns:
        logging.Logger: Configured logger instance.
    """
    if level is None:
        level = logging.INFO

    logger = logging.getLogger("panoptes_scout")

    # Clear any existing handlers
    logger.handlers = []

    # Create console handler with structured format
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False

    return logger


def get_logger(module_name: str) -> logging.Logger:
    """Get a logger for a specific module."""
    return logging.getLogger(f"panoptes_scout.{module_name}")


# Initialize default logger on import
_default_logger = configure_logging()
