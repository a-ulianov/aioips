"""Схема краткой информации о типе объекта (контроллер ``objectTypes``).

References:
    ``GET /core/api/objectTypes/{objectTypeId}/objectTypeInfo`` —
    ``ObjectTypes_GetObjectTypeInfo`` (обёртка
    ``QuickObjectTypeInfoDtoNullableResultDto`` → ``entity``).
"""

from uuid import UUID

from pydantic import Field

from ..base import IPSModel


class QuickObjectTypeInfo(IPSModel):
    """Краткая информация о типе объекта (``QuickObjectTypeInfoDto``).

    Облегчённая запись о ТИПЕ объекта: только идентичность (id, GUID) и наименование.
    Применяется, когда нужно дёшево узнать имя/GUID типа по его идентификатору без
    загрузки полного определения :class:`ObjectTypeDefinition`.

    Внимание (id-пространство): ``id`` здесь — идентификатор ТИПА объекта
    (``ObjectTypeID``), а не идентификатор объекта или его версии.

    Attributes:
        id: Идентификатор ТИПА объекта (``ObjectTypeID``; только для чтения).
        guid: Глобальный идентификатор типа объектов (переносим между базами).
        name: Наименование типа объектов.
    """

    id: int = Field(description="ObjectTypeID типа объекта (только для чтения)")
    guid: UUID | None = Field(default=None, description="GUID типа объектов")
    name: str | None = Field(default=None, description="Наименование типа объектов")
