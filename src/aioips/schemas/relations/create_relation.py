"""Схема запроса создания связи между информационными объектами IPS.

``CreateRelation`` (DTO ``CreateRelationDto``) описывает связь «родитель → потомок»,
которую нужно создать. Связь направленная: родитель задаётся ``proj_version_id``
(это ``ObjectID`` объекта-родителя, общий для всех его версий), потомок —
``part_version_id`` (``ObjectID`` объекта-потомка; ``0``, если связь не привязана к
конкретной версии). Тип связи (``relation_type``) определяет семантику отношения и
берётся из справочника типов (см. :meth:`relation_types`).

Дополнительно при создании можно сразу задать атрибуты связи через ``attribute_values``
(список :class:`AttributeValues`). Имена .NET-свойств DTO сериализуются в ``camelCase``
без заглавных суффиксов-акронимов (``relationType``, ``projVersionId``, ``partVersionId``,
``attributeValues``), поэтому здесь достаточно автогенератора алиасов базовой модели.

References:
    ``POST /core/api/relations`` — ``Relations_CreateRelation`` (``CreateRelationDto``).
    ``POST /core/api/relations/collection`` — ``Relations_CreateRelations``.
"""

from pydantic import Field

from ..base import IPSModel
from ..objects import AttributeValues


class CreateRelation(IPSModel):
    """DTO запроса создания связи «родитель → потомок» (``CreateRelationDto``).

    Описывает одну создаваемую связь. Родитель адресуется по ``proj_version_id``
    (``ObjectID`` родителя — общий для всех его версий), потомок — по
    ``part_version_id`` (``ObjectID`` потомка; ``0`` означает связь без привязки к
    конкретной версии). Внимание на id-пространство: оба поля принимают ``ObjectID``
    объектов, а НЕ ``ID`` версий.

    Attributes:
        relation_type: Идентификатор ТИПА связи (из справочника типов, см.
            :meth:`relation_types`).
        proj_version_id: ``ObjectID`` объекта-РОДИТЕЛЯ (``IDBObject.ObjectID``).
        part_version_id: ``ObjectID`` объекта-ПОТОМКА (``IDBObject.ObjectID``); ``0``,
            если связь не привязана к конкретной версии потомка.
        attribute_values: Опциональный список атрибутов, которыми сразу инициализируется
            создаваемая связь (схема :class:`AttributeValues`, DTO ``AttributeValuesDto``).
            ``None`` — связь создаётся без атрибутов.
    """

    relation_type: int = Field(alias="relationType", description="Идентификатор типа связи")
    proj_version_id: int = Field(alias="projVersionId", description="ObjectID объекта-родителя")
    part_version_id: int = Field(
        alias="partVersionId", description="ObjectID объекта-потомка (0 — не по версии)"
    )
    attribute_values: list[AttributeValues] | None = Field(
        default=None,
        alias="attributeValues",
        description="Атрибуты, которыми инициализируется создаваемая связь",
    )
