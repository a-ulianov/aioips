"""Схема применяемости типа объекта в составе IPS.

Применяемость (applicability) — это правило объектной модели, описывающее тройку
(тип-родителя, тип-связи, тип-потомка): какой тип объекта по какой связи может входить
в состав объекта другого типа. На её основе сервер валидирует добавление объектов в
состав. Подробнее — ``vault/knowledge/ips-object-model.md`` (раздел «Связи и состав»).

References:
    Эндпоинты ``/core/api/metadata/applicabilities/*`` IPS Web API; DTO ответа —
    ``ImsApplicabilityDto`` (в обёртке ``ImsApplicabilityDtoListNullableResultDto``).
"""

from typing import Annotated

from pydantic import Field

from ...common.enumerations.metadata import InheritMode
from ..base import EmptyListIfNone, IPSModel


class ObjectTypeApplicability(IPSModel):
    """Правило применяемости: что и по какой связи входит в состав типа объекта.

    Описывает одну допустимую тройку объектной модели: объект типа
    ``child_object_type_id`` может входить по связи ``relation_type_id`` в состав
    объекта типа ``in_object_type_id``. Сопутствующие поля задают ограничения этой
    применяемости: режим контроля состава/удаления (``relation_constraint_mode``),
    обязательность (``applicability_mode``), лимит числа связей (``maximum_links``)
    и признак «является содержимым» (``is_content``).

    Все поля DTO в camelCase без акронимов ``ID``/``GUID`` (``relationTypeId`` и т.п.),
    поэтому сопоставление с ``snake_case`` выполняет автогенератор алиасов ``to_camel``
    — явные ``alias`` не требуются. Обязателен лишь ``id``; остальные поля помечены
    необязательными для устойчивости к различиям версий API.

    Attributes:
        id: Идентификатор записи применяемости (служебный, id-пространство правил
            применяемости — не тип объекта и не связь).
        relation_type_id: Идентификатор типа связи, по которой допустимо вхождение
            (``RelationType``; ``-1`` — не задан).
        in_object_type_id: Идентификатор типа РОДИТЕЛЬСКОГО объекта — в состав которого
            входит потомок (``ObjectTypeID``; ``-1`` — не задан).
        child_object_type_id: Идентификатор типа ДОЧЕРНЕГО объекта — который входит в
            состав родителя (``ObjectTypeID``; ``-1`` — не задан).
        clone_child_relations: Клонировать ли связи потомка при копировании родителя.
        checkout_files: Брать ли файлы потомка на checkout вместе с родителем.
        maximum_links: Максимум связей данного типа (``Int32.MaxValue`` — без ограничения).
        relation_constraint_mode: Режим ограничения состава/удаления, налагаемый связью
            (``RelationConstraintModes``: ``none``/``childConstrained``/
            ``parentConstrained``/``childDelete``/… ).
        applicability_mode: Режим применяемости (``ApplicabilityModes``): ``enabled``/
            ``required``/``anyRequired``/``disabled``.
        is_content: Является ли потомок содержимым родителя. Если ``True``, удаление
            родителя удаляет потомков, у которых ``is_content == True``.
        options: Набор флагов-опций применяемости (``ApplicabilityOptions``):
            ``enableMultiLink``/``defaultRelation``/``oneChildObject``/… .
        public: Режим наследования настройки применяемости по иерархии типов
            (``InheritMode``): ``private``/``public``/``inherited``.
    """

    id: int = Field(description="ID записи применяемости (служебный)")
    relation_type_id: int | None = Field(default=None, description="ID типа связи (-1 — не задан)")
    in_object_type_id: int | None = Field(
        default=None, description="ID типа родительского объекта (в состав которого входит потомок)"
    )
    child_object_type_id: int | None = Field(
        default=None, description="ID типа дочернего объекта (входящего в состав)"
    )
    clone_child_relations: bool | None = Field(
        default=None, description="Клонировать ли связи потомка при копировании родителя"
    )
    checkout_files: bool | None = Field(
        default=None, description="Брать ли файлы потомка на checkout с родителем"
    )
    maximum_links: int | None = Field(
        default=None, description="Максимум связей (Int32.MaxValue — без ограничения)"
    )
    relation_constraint_mode: str | None = Field(
        default=None, description="Режим ограничения состава/удаления (RelationConstraintModes)"
    )
    applicability_mode: str | None = Field(
        default=None, description="Режим применяемости (ApplicabilityModes)"
    )
    is_content: bool | None = Field(
        default=None, description="Является ли потомок содержимым родителя"
    )
    options: Annotated[list[str], EmptyListIfNone] = Field(
        default_factory=list, description="Флаги-опции применяемости (ApplicabilityOptions)"
    )
    public: InheritMode | None = Field(
        default=None, description="Режим наследования настройки (InheritMode)"
    )
