"""Схемы legacy search-контроллера ``Relations`` (состав / вхождение по запросу).

Этот модуль описывает запрос и ответ АЛЬТЕРНАТИВНЫХ search-эндпоинтов связей с
заглавной буквы пути: ``POST /core/api/Relations/ConsistFromRequest`` (из чего
состоит объект) и ``POST /core/api/Relations/EntersInVersionRequest`` (куда входит
версия). Они НЕ совпадают с lowercase-методами ``relations/consistFrom`` и
``relations/entersInVersion`` (см. :mod:`aioips.schemas.relations.relations_select`):
тело здесь — :class:`RelationCollectionRequest` (id объекта + флаги обхода и фильтры
по типам), а результат — плоский список рёбер :class:`ObjectRelationDTO`, а не записи
с выбранными атрибутами связи.

Пространство идентификаторов (критично, см. [[ips-object-model]]):
    ``object_id`` запроса и ``parent_object_id`` / ``object_id`` ответа — id ОБЪЕКТОВ
    (F_OBJECT_ID), общие для версий, а НЕ id версий. ``part_id`` ответа — id ВЕРСИИ
    дочернего объекта в ребре (F_PART_ID); ``part_id`` ≠ ``object_id``.

References:
    ``POST /core/api/Relations/ConsistFromRequest`` — ``Relations_ConsistFromRequest``.
    ``POST /core/api/Relations/EntersInVersionRequest`` —
    ``Relations_EntersInVersionRequest``.
"""

from pydantic import Field

from ..base import IPSModel


class RelationCollectionRequest(IPSModel):
    """Запрос обхода связей объекта (тело ``Relations/*Request`` legacy-контроллера).

    Описывает один объект (``object_id``) и параметры обхода его связей: рекурсивный
    ли проход (``is_recure``), фильтр по типу связи (``relation_type_id``) и по типу
    объекта-результата (``object_type_id``), режим локальных типов. Применяется как
    АЛЬТЕРНАТИВА методам ``relations_consist_from`` / ``relations_enters_in_version``
    с параметрами-атрибутами: здесь возвращаются именно рёбра связей (см.
    :class:`ObjectRelationDTO`), без выборки значений атрибутов связи.

    Предусловие по id-пространству: ``object_id`` — идентификатор ОБЪЕКТА
    (F_OBJECT_ID), не версии.

    Attributes:
        object_id: Id ОБЪЕКТА (F_OBJECT_ID), для которого ищутся связи (обязателен).
        is_recure: Рекурсивный обход (раскрытие связей вглубь). По умолчанию ``False``.
        relation_type_id: Фильтр по id типа связи; ``None`` или ``-1`` — любой тип.
            По умолчанию ``-1``.
        object_type_id: Фильтр по id типа объекта-результата; ``-1`` — любой тип.
            По умолчанию ``-1``.
        local_types_mode: Режим локальных типов объектов. По умолчанию ``False``.
    """

    object_id: int = Field(description="Id ОБЪЕКТА (F_OBJECT_ID), для которого ищутся связи")
    is_recure: bool = Field(default=False, description="Рекурсивный обход связей")
    relation_type_id: int = Field(
        default=-1,
        alias="relationTypeID",
        description="Фильтр по id типа связи (-1/None — любой)",
    )
    object_type_id: int = Field(
        default=-1,
        alias="objectTypeID",
        description="Фильтр по id типа объекта-результата (-1 — любой)",
    )
    local_types_mode: bool = Field(default=False, description="Режим локальных типов объектов")


class ObjectRelationDTO(IPSModel):
    """Одно ребро связи в результате ``Relations/ConsistFromRequest|EntersInVersionRequest``.

    Элемент массива ответа legacy-контроллера. Описывает связь между родительским и
    дочерним объектом без значений атрибутов связи (для атрибутов используйте
    параметризованные методы ``relations_consist_from`` / ``relations_enters_in_version``).

    Пространство идентификаторов (критично, см. [[ips-object-model]]):
        ``parent_object_id`` и ``object_id`` — id ОБЪЕКТОВ (F_OBJECT_ID), общие для
        версий. ``object_guid`` — guid ОБЪЕКТА-результата. ``part_id`` — id ВЕРСИИ
        дочернего объекта в ребре (F_PART_ID), он НЕ равен ``object_id``.
        ``relation_id`` здесь не возвращается (он нестабилен и не кэшируется).

    Attributes:
        relation_type_id: Id типа связи.
        parent_object_id: Id ОБЪЕКТА-родителя в связи (F_OBJECT_ID).
        parent_object_type_id: Id типа объекта-родителя.
        object_id: Id ОБЪЕКТА-результата связи (F_OBJECT_ID).
        object_guid: Guid объекта-результата связи (``None``, если не задан).
        object_type_id: Id типа объекта-результата.
        part_id: Id ВЕРСИИ дочернего объекта в связи (F_PART_ID; ≠ ``object_id``).
    """

    relation_type_id: int = Field(default=0, description="Id типа связи")
    parent_object_id: int = Field(
        default=0, description="Id ОБЪЕКТА-родителя в связи (F_OBJECT_ID)"
    )
    parent_object_type_id: int = Field(default=0, description="Id типа объекта-родителя")
    object_id: int = Field(default=0, description="Id ОБЪЕКТА-результата связи (F_OBJECT_ID)")
    object_guid: str | None = Field(default=None, description="Guid объекта-результата связи")
    object_type_id: int = Field(default=0, description="Id типа объекта-результата")
    part_id: int = Field(
        default=0, description="Id ВЕРСИИ дочернего объекта (F_PART_ID; ≠ object_id)"
    )
