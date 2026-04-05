#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sys


def setup_logger(name: str = "minres", level: int = logging.INFO) -> logging.Logger:
    """
    Setup a global logger for the application.

    Args:
        name: Logger name
        level: Logging level

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers if called multiple times
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger


# Global logger instance
logger = setup_logger()