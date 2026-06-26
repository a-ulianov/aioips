"""Схема предметной области форм IPS.

References:
    ``GET /core/api/forms/subjectAreaFindCollection`` — массив ``SubjectAreaDto``.
"""

from uuid import UUID

from pydantic import Field

from ..base import IPSModel


class SubjectArea(IPSModel):
    """Предметная область форм IPS (DTO ``SubjectAreaDto``).

    Предметная область — именованная группировка форм/виджетов в системе.
    Идентифицируется ``guid``; несёт отображаемое имя, примечание и символьный код.

    Когда применять: при интерпретации результата
    :meth:`subject_area_find_collection` — для перечня доступных предметных
    областей (например, чтобы предложить выбор области в редакторе форм).

    В swagger поля ``name``/``note``/``symbol`` помечены как required, но на практике
    могут отсутствовать, поэтому объявлены необязательными (``None``). Идентичность —
    только ``guid``.

    Attributes:
        guid: GUID предметной области (``guid``); первичный идентификатор.
        name: Отображаемое имя предметной области (``name``).
        note: Примечание/описание предметной области (``note``).
        symbol: Символьный код (мнемоника) предметной области (``symbol``).
    """

    guid: UUID = Field(description="GUID предметной области")
    name: str | None = Field(default=None, description="Отображаемое имя предметной области")
    note: str | None = Field(default=None, description="Примечание/описание")
    symbol: str | None = Field(default=None, description="Символьный код (мнемоника)")
