"""Схема запроса обновления состава объектов контекста редактирования.

References:
    ``POST /core/api/editingContexts/{editingContextId}/update`` — тело
    ``UpdateEditingContextObjectsInDto``.
"""

from pydantic import Field

from ..base import IPSModel


class UpdateEditingContextObjectsIn(IPSModel):
    """Тело запроса обновления версий объектов в контексте редактирования.

    Задаёт перечень версий объектов контекста редактирования, которые нужно
    обновить (привести к актуальному состоянию). Идентификаторы — это ``id``
    ВЕРСИЙ объектов (F_ID), а не ``objectID`` объектов.

    Attributes:
        object_version_ids: Идентификаторы версий объектов (``id`` / F_ID) контекста
            редактирования, подлежащих обновлению. Обязательное поле.
    """

    object_version_ids: list[int] = Field(
        description="Идентификаторы версий объектов (id / F_ID) для обновления в контексте"
    )
