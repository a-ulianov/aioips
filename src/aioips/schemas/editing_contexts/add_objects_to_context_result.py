"""Схема результата добавления объектов в контекст редактирования.

References:
    ``POST /core/api/editingContexts/{editingContextId}/add`` — ответ
    ``AddObjectsToContextResultDto``.
"""

from typing import Annotated, Any

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class AddObjectsToContextResult(IPSModel):
    """Результат операции добавления объектов в контекст редактирования.

    Содержит счётчики добавленных и пропущенных объектов, а также журнал записей
    о проблемах, возникших по отдельным объектам. Журнал передаётся как список
    сырых записей (``dict``), так как структура записи (код/описание ошибки,
    идентификатор версии) может расширяться сервером.

    Attributes:
        editing_context_log_entities: Журнал записей о проблемах по отдельным
            объектам (каждая запись — сырой ``dict`` ``EditingContextsLogEntryDto``:
            ``errorCode``, ``errorDescription``, ``objectVersionId``). Пустой список,
            если проблем не было.
        added_objects_count: Количество объектов, фактически добавленных в контекст.
        skipped_objects_count: Количество объектов, пропущенных при добавлении.
    """

    editing_context_log_entities: Annotated[list[dict[str, Any]], EmptyListIfNone] = Field(
        default_factory=list,
        description="Журнал записей о проблемах по отдельным объектам",
    )
    added_objects_count: int = Field(
        default=0, description="Количество добавленных в контекст объектов"
    )
    skipped_objects_count: int = Field(
        default=0, description="Количество пропущенных при добавлении объектов"
    )
