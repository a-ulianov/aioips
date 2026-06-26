"""Схема настройки типа атрибута для конкретного типа связи.

В IPS один и тот же тип атрибута может применяться не только к типам объектов, но и к
типам связей (``RelationType``) с индивидуальными настройками: обязательность,
вычисляемость, формула, ограничение ссылки и т.д. Эта схема описывает «привязку» типа
атрибута (``attribute_id``) к типу связи (``relation_type_id``) вместе с
переопределёнными для этой пары параметрами (см. ``vault/knowledge/ips-object-model.md``).

В отличие от ``AttributeForObjectType`` здесь нет полей ``public``/``unique``/``level_id``
(они не определены для атрибутов связей), а ключ привязки — ``relation_type_id``.

References:
    ``GET /core/api/metadata/attributeForRelationType/{relationTypeId}/{attributeTypeId}``
    и ``...List`` — DTO ``ImsAttributeForRelationTypeDto``.
"""

from typing import Annotated

from pydantic import Field

from ...common.enumerations.attribute import ComputeValueMode, FieldType
from ..base import EmptyListIfNone, IPSModel


class AttributeForRelationType(IPSModel):
    """Настройки применения типа атрибута к конкретному типу связи.

    Обязателен лишь идентификатор атрибута; прочие параметры в ответах присутствуют
    не всегда, поэтому объявлены необязательными — это устойчиво к различиям версий API.

    Attributes:
        attribute_id: Идентификатор типа атрибута (id-пространство типов атрибутов; ключ
            для :meth:`attribute_type`).
        computed: Режим вычисляемости (``ComputeValueMode``): ``notComputableValue``/
            ``storedValue``/``jitValue``/``indexValue``.
        formula: Формула вычисления значения для вычисляемого атрибута.
        language_id: Идентификатор языка.
        area_id: Идентификатор предметной области.
        optimization_mode: Режим оптимизации хранения значений атрибута.
        required: Режим обязательности/видимости атрибута для типа связи.
        is_content: Является ли атрибут содержимым (составным значением).
        options: Набор флагов-опций атрибута.
        master_attribute_id: Идентификатор мастер-атрибута для атрибута-ссылки.
        source_attribute_id: Идентификатор атрибута-источника значения мастер-атрибута.
        validation_rule: Правило валидации значения (например, ограничение ссылки).
        mask: Маска ввода значений атрибута.
        default_value: Текстовое представление значения по умолчанию.
        relation_type_id: Идентификатор типа связи (``RelationTypeID``), к которому
            привязан атрибут (по умолчанию ``-1``, если связь не задана).
        field_type: Тип данных атрибута (``FieldType``): ``ftString``/``ftObjectLink``/… .
        real_field_type: Реальный тип данных, если ``field_type == ftSystem``.
    """

    attribute_id: int = Field(description="ID типа атрибута (ключ для attribute_type)")
    computed: ComputeValueMode | None = Field(
        default=None, description="Вычисляемость (ComputeValueMode): storedValue/jitValue/…"
    )
    formula: str | None = Field(default=None, description="Формула вычисления значения")
    language_id: str | None = Field(default=None, description="Идентификатор языка")
    area_id: str | None = Field(default=None, description="Предметная область")
    optimization_mode: str | None = Field(default=None, description="Режим оптимизации хранения")
    required: str | None = Field(default=None, description="Режим обязательности/видимости")
    is_content: bool | None = Field(default=None, description="Является ли атрибут содержимым")
    options: Annotated[list[str], EmptyListIfNone] = Field(
        default_factory=list, description="Набор флагов-опций атрибута"
    )
    master_attribute_id: int | None = Field(
        default=None, description="Идентификатор мастер-атрибута"
    )
    source_attribute_id: int | None = Field(
        default=None, description="Идентификатор атрибута-источника"
    )
    validation_rule: str | None = Field(default=None, description="Правило валидации значения")
    mask: str | None = Field(default=None, description="Маска ввода значений")
    default_value: str | None = Field(default=None, description="Значение по умолчанию (текст)")
    relation_type_id: int | None = Field(default=None, description="Идентификатор типа связи")
    field_type: FieldType | None = Field(default=None, description="Тип данных атрибута")
    real_field_type: FieldType | None = Field(
        default=None, description="Реальный тип данных (если field_type == ftSystem)"
    )
