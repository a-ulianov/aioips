"""Схема группы атрибутов метаданных IPS.

Группа атрибутов — это узел иерархии, объединяющий типы атрибутов в логические
наборы (для удобства администрирования и отображения). Группы образуют дерево:
поле ``parent_id`` указывает на родительскую группу, ``0`` — корневой уровень.

References:
    ``GET /core/api/metadata/attributeGroups/{id}`` — DTO ``ImsAttributeGroupDto``
    (в обёртке ``ImsAttributeGroupDtoNullableResultDto``).
"""

from uuid import UUID

from pydantic import Field

from ..base import IPSModel


class AttributeGroup(IPSModel):
    """Описание группы атрибутов в метаданных IPS.

    Группа атрибутов объединяет типы атрибутов в иерархический набор. Состав группы
    (входящие в неё типы атрибутов) хранится отдельно и читается методами
    ``attributes_in_group_ids`` / ``attributes_in_group_guids``, а не полями этой
    схемы. Иерархия групп задаётся полем ``parent_id``.

    Обязательны поля идентичности и структуры (``id``, ``guid``, ``name``,
    ``parent_id``); ``note``/``area_id``/``language_id`` присутствуют не всегда и
    объявлены необязательными. Поля DTO в camelCase без акронимов ``ID``/``GUID``
    (``areaId``, ``parentId``), поэтому сопоставление с ``snake_case`` выполняет
    автогенератор алиасов ``to_camel`` — явные ``alias`` не требуются.

    Attributes:
        id: Числовой идентификатор группы атрибутов (id-пространство ГРУПП атрибутов;
            не тип атрибута и не значение атрибута).
        guid: Глобальный идентификатор группы (переносим между базами IPS).
        name: Название группы.
        note: Примечание к группе (``None``, если не задано).
        area_id: Идентификатор предметной области (``None``, если не задан).
        language_id: Идентификатор языка (``None``, если не задан).
        parent_id: Идентификатор родительской группы, в которую входит данная группа.
            ``0`` — группа находится на верхнем уровне иерархии (корневая).
    """

    id: int = Field(description="ID группы атрибутов (id-пространство групп атрибутов)")
    guid: UUID = Field(description="GUID группы атрибутов (переносим между базами)")
    name: str = Field(description="Название группы")
    note: str | None = Field(default=None, description="Примечание")
    area_id: str | None = Field(default=None, description="Идентификатор предметной области")
    language_id: str | None = Field(default=None, description="Идентификатор языка")
    parent_id: int = Field(
        description="ID родительской группы; 0 — группа на верхнем уровне иерархии"
    )
