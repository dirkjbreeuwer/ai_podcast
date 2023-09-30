"""
Logging Utility Module.

This module provides a utility function to easily set up and retrieve logger instances
with a predefined format. The logging level is set to INFO by default, and the format
includes the timestamp, logger name, log level, and the actual log message.

Example:
    >>> from logging_util import get_logger
    >>> logger = get_logger("my_module")
    >>> logger.info("This is an info message")

Attributes:
    logging (module): The standard Python logging module.

Functions:
    get_logger(name): Returns a logger instance with the specified name.
"""

import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def get_logger(name):
    """
    Returns a logger instance with the specified name.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: A logger instance with the given name.

    Example:
        >>> logger = get_logger("my_module")
        >>> logger.info("This is an info message")
    """
    return logging.getLogger(name)
