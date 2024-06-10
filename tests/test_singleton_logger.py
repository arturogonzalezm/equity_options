"""
Test the SingletonLogger class.
"""

import pytest
import logging
from backend.singleton_logger import SingletonLogger


def test_singleton_instance():
    """
    Test that the SingletonLogger class returns the same instance when called multiple times.
    :return: None
    """
    logger1 = SingletonLogger().get_logger()
    logger2 = SingletonLogger().get_logger()
    assert logger1 is logger2


def test_logger_initialization():
    """
    Test that the logger is initialized correctly with the default settings.
    :return: None
    """
    logger = SingletonLogger().get_logger()
    assert logger.level == logging.DEBUG

    console_handler = None
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            console_handler = handler
            break

    assert console_handler is not None
    assert console_handler.level == logging.DEBUG
    assert isinstance(console_handler.formatter, logging.Formatter)
    assert console_handler.formatter._fmt == "%(asctime)s - %(threadName)s - %(levelname)s - %(message)s"


def test_logger_name():
    """
    Test that the logger name is set correctly.
    :return: None
    """
    SingletonLogger._instance = None  # Reset singleton instance
    logger_instance = SingletonLogger(logger_name="test_logger")
    logger = logger_instance.get_logger()
    assert logger.name == "test_logger"


def test_logger_custom_format():
    """
    Test that the logger is initialized with a custom format.
    :return:
    """
    SingletonLogger._instance = None  # Reset singleton instance
    custom_format = "%(levelname)s: %(message)s"
    logger_instance = SingletonLogger(log_format=custom_format)
    logger = logger_instance.get_logger()

    console_handler = None
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            console_handler = handler
            break

    assert console_handler is not None
    assert console_handler.formatter._fmt == custom_format


if __name__ == "__main__":
    pytest.main()
