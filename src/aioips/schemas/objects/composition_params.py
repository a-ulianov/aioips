"""Схемы параметров запросов чтения объектов (версии и состав).

Содержит DTO-параметры для двух читающих POST-эндпоинтов раздела объектов:
:class:`AllObjectVersionsParameters` — выбор всех версий объекта по id, и
:class:`ObjectCompositionParams` — параметры контекста для получения состава по
версии проекта. Оба запроса только читают данные (без мутаций). См.
[[ips-object-model]] (разделы «Идентичность» и «Состав»).

References:
    ``POST /core/api/objects/allObjectVersions`` — ``Objects_GetAllObjectVersions``.
    ``POST /core/api/objects/{projectVersionId}/composition`` —
    ``Objects_GetObjectComposition``.
"""

from typing import Annotated, Any

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class AllObjectVersionsParameters(IPSModel):
    """Параметры выбора всех версий объекта (тело ``objects_all_versions``).

    Задаёт объект (или одну из его версий) идентификатором ``id`` и уточняет
    интерпретацию этого идентификатора флагом ``is_object_id``, а также состав
    выборки версий (заготовки, удалённые) и набор возвращаемых атрибутов.

    Внимание (id-пространство): семантика ``id`` зависит от ``is_object_id``.
    При ``is_object_id=False`` (по умолчанию на сервере) ``id`` трактуется как
    идентификатор ЛЮБОЙ версии объекта (в БД это F_OBJECT_ID — общий для версий);
    при ``is_object_id=True`` — как идентификатор конкретной версии (F_ID).
    Формулировки в swagger противоречивы, поэтому проверяйте на проде.

    Attributes:
        id: Идентификатор объекта либо его версии (трактовка — по ``is_object_id``).
        is_object_id: Как интерпретировать ``id`` (см. описание класса). По
            умолчанию ``None`` (серверное значение).
        show_blanks: Если ``True``, показывать также заготовки версий.
            ``None`` — серверное значение по умолчанию.
        show_deleted: Если ``True``, показывать также удалённые версии.
            ``None`` — серверное значение по умолчанию.
        attribute_ids: Перечень id атрибутов объекта для выборки (только атрибуты
            таблицы IMS_OBJECTS). Пустой список — вернуть все такие атрибуты.
            ``None`` — поле не передаётся.
    """

    id: int = Field(description="Идентификатор объекта или версии (трактовка — по is_object_id)")
    is_object_id: bool | None = Field(
        default=None,
        alias="isObjectId",
        description="Как интерпретировать id: False — id версии (F_OBJECT_ID), True — id (F_ID)",
    )
    show_blanks: bool | None = Field(
        default=None, description="True — показывать также заготовки версий"
    )
    show_deleted: bool | None = Field(
        default=None, description="True — показывать также удалённые версии"
    )
    attribute_ids: Annotated[list[int] | None, EmptyListIfNone] = Field(
        default=None,
        alias="attributeIdsToSelect",
        description="ID атрибутов IMS_OBJECTS для выборки; пустой список — все такие атрибуты",
    )


class ObjectCompositionParams(IPSModel):
    """Параметры контекста для получения состава объекта (``object_composition``).

    Несёт необязательное правило контекста ``context_rule`` (исходный
    ``ContextRuleDto``), влияющее на то, какие версии дочерних объектов попадают в
    состав. Передаётся как «сырой» словарь, чтобы не фиксировать здесь полную
    структуру серверного DTO (``versionRuleObjectId``, ``editingContextId``,
    ``editingContextMode``). Если правило не задано, в тело уходит пустой объект.

    Attributes:
        context_rule: Правило контекста версий (``ContextRuleDto``) как словарь
            ``{"versionRuleObjectId": ..., "editingContextId": ...,
            "editingContextMode": ...}`` или ``None`` (контекст по умолчанию).
    """

    context_rule: dict[str, Any] | None = Field(
        default=None,
        alias="contextRule",
        description="Правило контекста версий (ContextRuleDto) как словарь или None",
    )
