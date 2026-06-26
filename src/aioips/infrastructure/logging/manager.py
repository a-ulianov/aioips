"""Настройка и получение логгеров библиотеки aioips.

Все логгеры библиотеки — потомки корневого логгера ``aioips``. По умолчанию
библиотека не навязывает обработчики приложению (следует рекомендации Python
для библиотек: вешать ``NullHandler``), а настройка вывода выполняется явно
через :func:`configure_logging` или самим приложением.
"""

import logging

from .formatters import JsonFormatter

ROOT_LOGGER_NAME = "aioips"

_DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Библиотека по умолчанию молчит, пока приложение не настроит логирование.
logging.getLogger(ROOT_LOGGER_NAME).addHandler(logging.NullHandler())


def get_logger(name: str | None = None) -> logging.Logger:
    """Возвращает именованный логгер в пространстве имён библиотеки.

    Args:
        name: Имя дочернего логгера (например, ``"core"``). Если ``None``,
            возвращается корневой логгер ``aioips``.

    Returns:
        Экземпляр ``logging.Logger`` с именем ``aioips`` или ``aioips.<name>``.

    Examples:
        >>> logger = get_logger("core")
        >>> logger.name
        'aioips.core'
    """
    if name is None:
        return logging.getLogger(ROOT_LOGGER_NAME)
    return logging.getLogger(f"{ROOT_LOGGER_NAME}.{name}")


def configure_logging(
    level: str = "ERROR",
    *,
    json: bool = False,
    fmt: str = _DEFAULT_FORMAT,
) -> None:
    """Настраивает вывод логов библиотеки в стандартный поток.

    Идемпотентна: повторный вызов заменяет ранее добавленный обработчик,
    не накапливая дубликаты.

    Args:
        level: Уровень логирования (``DEBUG``, ``INFO``, ``WARNING``, ``ERROR``, ``CRITICAL``).
        json: Если ``True``, использовать структурный JSON-формат.
        fmt: Шаблон текстового формата (игнорируется при ``json=True``).

    Examples:
        >>> configure_logging("INFO", json=True)
    """
    logger = logging.getLogger(ROOT_LOGGER_NAME)
    logger.setLevel(level.upper())

    for existing in list(logger.handlers):
        if getattr(existing, "_aioips_managed", False):
            logger.removeHandler(existing)

    handler: logging.Handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter() if json else logging.Formatter(fmt))
    handler._aioips_managed = True  # type: ignore[attr-defined]
    logger.addHandler(handler)
