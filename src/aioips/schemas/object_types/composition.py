"""Схемы состава ОБЪЕКТОВ заданного типа (контроллер ``objectTypes``).

Содержит DTO для читающего POST-эндпоинта
``POST /core/api/objectTypes/{objectTypeId}/composition``
(``Objects_GetObjectsComposition``):
:class:`ObjectsCompositionParams` — тело-параметры запроса (набор атрибутов и
правило контекста версий), и :class:`ObjectWithCompositionDto` — элемент ответа
(объект состава с его под-составом и запрошенными атрибутами).

Внимание (id-пространства): аргумент пути ``objectTypeId`` — это id ТИПА
(``ObjectTypeID``); поле ``object_id`` (=``objectID``) в ответе — id ОБЪЕКТА
(F_OBJECT_ID), общий для всех версий объекта. См. [[ips-object-model]]
(разделы «Идентичность» и «Состав»).

References:
    ``POST /core/api/objectTypes/{objectTypeId}/composition`` —
    ``Objects_GetObjectsComposition`` (тело ``ObjectsCompositionParamsDto``,
    ответ ``list[ObjectWithCompositionDto]``).
"""

from typing import Annotated, Any

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class ObjectsCompositionParams(IPSModel):
    """Параметры запроса состава объектов типа (тело ``object_type_composition``).

    Тело POST-запроса ``Objects_GetObjectsComposition``: задаёт, какие атрибуты
    добавить к каждому объекту состава, и необязательное правило контекста версий.
    Оба поля необязательны; пустое тело допустимо (вернётся состав в контексте по
    умолчанию без дополнительных атрибутов).

    Правило контекста ``context_rule`` передаётся как «сырой» словарь, чтобы не
    фиксировать здесь полную структуру серверного ``ContextRuleDto``
    (``versionRuleObjectId``, ``editingContextId``, ``editingContextMode``).

    Attributes:
        attribute_ids: Перечень id атрибутов объекта, которые добавить в результат
            (поле ``attributes`` каждого :class:`ObjectWithCompositionDto`). Пустой
            список — без дополнительных атрибутов. ``None`` — поле не передаётся.
        context_rule: Правило контекста версий (``ContextRuleDto``) как словарь
            ``{"versionRuleObjectId": ..., "editingContextId": ...,
            "editingContextMode": ...}`` или ``None`` (контекст по умолчанию).
    """

    attribute_ids: Annotated[list[int] | None, EmptyListIfNone] = Field(
        default=None,
        alias="attributeIdsToSelect",
        description="ID атрибутов объекта для добавления в результат; None — не передаётся",
    )
    context_rule: dict[str, Any] | None = Field(
        default=None,
        alias="contextRule",
        description="Правило контекста версий (ContextRuleDto) как словарь или None",
    )


class ObjectWithCompositionDto(IPSModel):
    """Объект состава с его под-составом и запрошенными атрибутами (элемент ответа).

    Элемент массива-ответа ``Objects_GetObjectsComposition``. Описывает один объект
    заданного типа: его идентификатор, дополнительно запрошенные атрибуты и состав
    (дочерние объекты со связями).

    Внимание (id-пространство): ``object_id`` (=``objectID``=F_OBJECT_ID) —
    идентификатор ОБЪЕКТА (общий для всех версий), НЕ идентификатор типа и НЕ
    идентификатор версии. Под-состав ``object_compositions`` оставлен «сырым»
    (``list[dict]``): каждый элемент — ``ObjectCompositionDto`` с ключами ``object``
    (вложенный ``ObjectDto``) и ``relation`` (``RelationDto`` — связь
    родитель→потомок). Так структура остаётся устойчивой к расхождениям со swagger
    и не тянет рекурсивную типизацию.

    Attributes:
        object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для
            всех версий объекта. По умолчанию 0, если сервер не вернул поле.
        attributes: Дополнительно запрошенные атрибуты (по
            ``ObjectsCompositionParams.attribute_ids``). Каждый элемент —
            ``{"attributeId": int, "value": Any}``. ``null`` нормализуется в ``[]``.
        object_compositions: Состав объекта — список элементов
            ``ObjectCompositionDto`` ``{"object": ObjectDto, "relation": RelationDto}``
            как «сырые» словари. ``null`` нормализуется в ``[]``.
    """

    object_id: int = Field(
        default=0,
        alias="objectID",
        description="Идентификатор ОБЪЕКТА (objectID / F_OBJECT_ID), общий для версий",
    )
    attributes: Annotated[list[dict[str, Any]], EmptyListIfNone] = Field(
        default_factory=list,
        description="Запрошенные атрибуты [{attributeId, value}, ...]",
    )
    object_compositions: Annotated[list[dict[str, Any]], EmptyListIfNone] = Field(
        default_factory=list,
        alias="objectCompositions",
        description="Состав объекта [{object: ObjectDto, relation: RelationDto}, ...]",
    )
