"""Тесты подсистемы логирования."""

import json
import logging

from aioips.infrastructure.logging import (
    JsonFormatter,
    configure_logging,
    get_logger,
)


def test_get_logger_namespacing():
    assert get_logger().name == "aioips"
    assert get_logger("core").name == "aioips.core"


def test_json_formatter_outputs_valid_json_with_extra():
    record = logging.LogRecord(
        name="aioips.test",
        level=logging.INFO,
        pathname="f.py",
        lineno=1,
        msg="привет %s",
        args=("мир",),
        exc_info=None,
    )
    record.correlation_id = "abc-123"

    data = json.loads(JsonFormatter().format(record))

    assert data["message"] == "привет мир"
    assert data["level"] == "INFO"
    assert data["logger"] == "aioips.test"
    assert data["correlation_id"] == "abc-123"


def test_configure_logging_is_idempotent():
    configure_logging("INFO", json=True)
    configure_logging("DEBUG", json=False)

    logger = logging.getLogger("aioips")
    managed = [h for h in logger.handlers if getattr(h, "_aioips_managed", False)]
    assert len(managed) == 1
    assert logger.level == logging.DEBUG
