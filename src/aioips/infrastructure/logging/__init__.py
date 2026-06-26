"""Подсистема логирования библиотеки aioips."""

from .formatters import JsonFormatter
from .manager import ROOT_LOGGER_NAME, configure_logging, get_logger

aioips_logger = get_logger()

__all__ = [
    "ROOT_LOGGER_NAME",
    "JsonFormatter",
    "aioips_logger",
    "configure_logging",
    "get_logger",
]
