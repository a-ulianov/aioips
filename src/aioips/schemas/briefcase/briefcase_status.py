"""Схема статуса выполнения задачи Портфеля IPS.

References:
    ``POST /core/api/briefcase/GetStatus`` и ``POST /core/api/briefcase/GetExportProgress``
    — объект ``BriefcaseStatusDTO``.
"""

from pydantic import Field

from ..base import IPSModel


class BriefcaseStatus(IPSModel):
    """Статус выполнения текущей фоновой задачи Портфеля (экспорта/импорта).

    Портфель — это пакет экспорта/импорта объектов IPS («briefcase»); операции с ним
    выполняются на сервере асинхронно, а клиент опрашивает их прогресс. Данная схема —
    снимок такого прогресса на момент запроса.

    Когда применять: для индикации хода длительной операции Портфеля. Если ни одна
    задача не запущена, сервер обычно возвращает «пустой» статус (``percent = 0``,
    ``status = None``, ``is_completed = False``) — это нормально и не является ошибкой.

    Attributes:
        percent: Процент выполнения (0–100).
        status: Текстовое описание текущего шага операции; ``None``, если шаг не задан.
        is_completed: Признак завершения (в том числе завершения с ошибкой).
    """

    percent: int = Field(default=0, description="Процент выполнения (0–100)")
    status: str | None = Field(default=None, description="Описание выполняемой операции")
    is_completed: bool = Field(
        default=False, description="Завершено (включая завершение с ошибкой)"
    )
