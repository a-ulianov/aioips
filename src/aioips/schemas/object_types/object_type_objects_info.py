"""Схема сводки по объектам (экземплярам) типа (контроллер ``objectTypes``).

References:
    ``GET /core/api/objectTypes/{objectTypeId}/objectsInfo`` —
    ``ObjectTypes_GetObjectsInfo`` (``ObjectTypeObjectsInfo``, без обёртки).
"""

from pydantic import Field

from ..base import IPSModel


class ObjectTypeObjectsInfo(IPSModel):
    """Сводка по реальным объектам (экземплярам) заданного типа (``ObjectTypeObjectsInfo``).

    Возвращает агрегаты по ЭКЗЕМПЛЯРАМ типа: сколько объектов и сколько итераций
    (снимков) данного типа существует в базе. В отличие от определения типа
    (:class:`ObjectTypeDefinition`) и метамодели раздела ``metadata``, эта схема
    описывает не сам тип, а количество реальных объектов этого типа.

    Внимание (id-пространство): ``object_type`` — идентификатор ТИПА объекта
    (``ObjectTypeID``), к которому относится сводка, а не идентификатор объекта.

    Attributes:
        object_type: Идентификатор ТИПА объекта (``ObjectTypeID``), к которому относится
            сводка.
        objects_count: Количество объектов (экземпляров) данного типа.
        snapshots_count: Количество итераций (снимков) объектов данного типа.
    """

    object_type: int = Field(description="ObjectTypeID типа, к которому относится сводка")
    objects_count: int | None = Field(
        default=None, description="Количество объектов (экземпляров) данного типа"
    )
    snapshots_count: int | None = Field(
        default=None, description="Количество итераций (снимков) объектов данного типа"
    )
