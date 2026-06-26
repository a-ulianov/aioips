"""Схема демонстрационного раздела значений (samples/values)."""

from ..base import IPSModel


class UserGreeting(IPSModel):
    """Приветствие для текущего пользователя (``UserGreetingDTO``).

    Назначение: типизированный разбор ответа :meth:`sample_values`. Раздел
    ``samples`` — учебный (демо-API); приветствие применяют для проверки
    авторизации и базовой доступности сервера.

    Поля:
        text: Текст приветствия (непустая строка).

    Notes:
        operationId ``Values_GetGreeting``; путь ``GET /core/api/samples/values``.
    """

    text: str
