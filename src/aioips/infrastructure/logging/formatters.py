"""Форматтеры логов: текстовый по умолчанию и структурный JSON.

Структурный JSON-формат удобен для машинной обработки и агрегации логов
(ELK, Loki и т.п.). Текстовый формат — для локальной разработки.
"""

import json
import logging
from typing import Any


class JsonFormatter(logging.Formatter):
    """Форматирует записи лога в одну строку JSON.

    В вывод попадают стандартные поля записи и любые дополнительные ключи,
    переданные через параметр ``extra`` при логировании.
    """

    _RESERVED: frozenset[str] = frozenset(logging.makeLogRecord({}).__dict__.keys()) | {
        "message",
        "asctime",
        "taskName",
    }

    def format(self, record: logging.LogRecord) -> str:
        """Преобразует запись лога в JSON-строку.

        Args:
            record: Запись лога стандартной библиотеки ``logging``.

        Returns:
            Строка с сериализованным в JSON содержимым записи.
        """
        payload: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        for key, value in record.__dict__.items():
            if key not in self._RESERVED and not key.startswith("_"):
                payload[key] = value

        return json.dumps(payload, ensure_ascii=False, default=str)
