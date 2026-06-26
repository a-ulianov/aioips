"""Схема единицы измерения IPS.

References:
    ``GET /core/api/measureUnits`` — массив ``MeasureUnitDto``.
"""

from typing import Annotated
from uuid import UUID

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class MeasureUnit(IPSModel):
    """Единица измерения физической величины в справочнике IPS.

    Единицы измерения используются атрибутами типа ``ftMeasured`` (величина =
    числовое значение + единица измерения). Каждая единица принадлежит ровно одной
    физической величине (``physical_quantity_id``) и связана с ней коэффициентом
    приведения ``k`` к базовой единице этой величины (для базовой единицы ``k = 1``).

    Обязательны только поля идентичности (``id``, ``guid``) и привязки к физической
    величине. Прочие поля объявлены необязательными с дефолтами — это устойчиво к
    различиям между единицами и версиями API.

    Attributes:
        id: Числовой идентификатор единицы измерения.
        guid: Глобальный идентификатор единицы измерения.
        long_name: Полное наименование единицы измерения (например, «миллиметр»).
        short_name: Краткое наименование (обозначение) единицы измерения (например, «мм»).
        k: Коэффициент приведения значения к базовой единице величины (для базовой — 1).
        physical_quantity_id: Идентификатор физической величины, к которой относится единица.
        physical_quantity_guid: Глобальный идентификатор физической величины.
        is_default: Признак единицы измерения по умолчанию для своей величины.
        short_name_index: Альтернативные краткие обозначения, поддерживающие индексацию.
        operation_list: Список операций, для которых применима данная единица измерения.
    """

    id: int = Field(description="Идентификатор единицы измерения")
    guid: UUID = Field(description="Глобальный идентификатор единицы измерения")
    long_name: str | None = Field(default=None, description="Полное наименование единицы измерения")
    short_name: str | None = Field(
        default=None, description="Краткое наименование (обозначение) единицы измерения"
    )
    k: float = Field(default=1.0, description="Коэффициент приведения к базовой единице величины")
    physical_quantity_id: int = Field(description="Идентификатор физической величины")
    physical_quantity_guid: UUID | None = Field(
        default=None, description="Глобальный идентификатор физической величины"
    )
    is_default: bool = Field(
        default=False, description="Единица измерения по умолчанию для своей величины"
    )
    short_name_index: Annotated[list[str], EmptyListIfNone] = Field(
        default_factory=list, description="Альтернативные краткие обозначения с индексацией"
    )
    operation_list: Annotated[list[str], EmptyListIfNone] = Field(
        default_factory=list, description="Операции, для которых применима единица измерения"
    )
