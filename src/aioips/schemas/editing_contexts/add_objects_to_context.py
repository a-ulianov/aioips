"""Схема запроса добавления объектов в контекст редактирования.

References:
    ``POST /core/api/editingContexts/{editingContextId}/add`` — тело ``AddObjectsToContextDto``.
"""

from enum import StrEnum

from pydantic import Field

from ..base import IPSModel


class AddObjectsToEditingContextType(StrEnum):
    """Способ добавления объектов в контекст редактирования.

    Управляет тем, попадут ли в контекст только сами указанные версии объектов
    или ещё и их состав (вложенные объекты). Соответствует enum
    ``AddObjectsToEditingContextType`` IPS Web API.

    Семантика членов:
        OBJECTS: ``objects`` — добавить только перечисленные версии объектов.
        OBJECTS_WITH_COMPOSITION: ``objectsWithComposition`` — добавить объекты
            вместе с их непосредственным составом (один уровень вложенности).
        OBJECTS_WITH_RECURSIVE_COMPOSITION: ``objectsWithRecursiveComposition`` —
            добавить объекты вместе со всем составом рекурсивно (все уровни).
    """

    OBJECTS = "objects"
    OBJECTS_WITH_COMPOSITION = "objectsWithComposition"
    OBJECTS_WITH_RECURSIVE_COMPOSITION = "objectsWithRecursiveComposition"


class AddObjectsToContext(IPSModel):
    """Тело запроса добавления объектов в контекст редактирования.

    Описывает, какие версии объектов добавить в контекст редактирования и нужно ли
    при этом захватывать их состав. Идентификаторы — это ``id`` ВЕРСИЙ объектов
    (F_ID), а не ``objectID`` объектов.

    Attributes:
        object_version_ids: Идентификаторы ВЕРСИЙ объектов (``id`` / F_ID) для
            добавления в контекст. Обязательное непустое поле.
        add_objects_to_context_type: Способ добавления (только объекты, объекты с
            составом, объекты с рекурсивным составом). Обязательное поле.
    """

    object_version_ids: list[int] = Field(
        description="Идентификаторы версий объектов (id / F_ID) для добавления"
    )
    add_objects_to_context_type: AddObjectsToEditingContextType = Field(
        description="Способ добавления объектов в контекст (с составом или без)"
    )
