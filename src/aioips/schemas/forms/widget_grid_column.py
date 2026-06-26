"""Схема колонки табличного виджета форм IPS.

References:
    ``GET /core/api/forms/getDefaultColumns4Widget`` — массив ``WidgetGridColumn``
    (колонки по умолчанию для табличного виджета). Вложенные ``attrInfo``/``uiInfo``
    в swagger описаны как ``ColAttrInfo``/``ColUiInfo``/``ColOrderInfo``.
"""

from typing import Any

from pydantic import Field

from ..base import IPSModel


class WidgetGridColumn(IPSModel):
    """Колонка табличного (grid) виджета формы IPS (DTO ``WidgetGridColumn``).

    Описывает одну колонку таблицы виджета: к какому атрибуту она привязана
    (``attr_info``), как отображается (``ui_info``), её порядок (``order``), а также
    флаги пользовательской/виртуальной природы. Возвращается набором колонок по
    умолчанию для виджета.

    Когда применять: при интерпретации результата
    :meth:`default_columns_for_widget` — чтобы построить раскладку таблицы
    виджета (состав колонок, привязку к атрибутам, порядок).

    Вложенные структуры ``attr_info`` и ``ui_info`` — крупные объекты метаданных
    атрибута и UI-представления соответственно (swagger-типы ``ColAttrInfo`` /
    ``ColUiInfo`` / ``ColOrderInfo``). Они моделируются как ``dict[str, Any]``: их
    внутренняя структура обширна, нестабильна между версиями и здесь не требуется —
    наружу отдаётся как есть, без потери данных.

    Attributes:
        attr_info: Метаданные привязки колонки к атрибуту (``attrInfo``,
            swagger ``ColAttrInfo``); сырой объект.
        ui_info: Параметры UI-представления колонки (``uiInfo``,
            swagger ``ColUiInfo``); сырой объект.
        order: Параметры сортировки/порядка колонки (``order``,
            swagger ``ColOrderInfo``); сырой объект либо ``None``.
        scheme: Имя схемы колонки (``scheme``).
        attr_type: Строковый тип атрибута колонки (``attrType``).
        is_custom: Признак пользовательской (добавленной вручную) колонки.
        is_virtual: Признак виртуальной (вычисляемой) колонки.
    """

    attr_info: dict[str, Any] = Field(
        default_factory=dict, description="Метаданные привязки к атрибуту (ColAttrInfo)"
    )
    ui_info: dict[str, Any] = Field(
        default_factory=dict, description="Параметры UI-представления колонки (ColUiInfo)"
    )
    order: dict[str, Any] | None = Field(
        default=None, description="Параметры порядка/сортировки колонки (ColOrderInfo)"
    )
    scheme: str | None = Field(default=None, description="Имя схемы колонки")
    attr_type: str | None = Field(default=None, description="Строковый тип атрибута колонки")
    is_custom: bool = Field(default=False, description="Пользовательская колонка")
    is_virtual: bool = Field(default=False, description="Виртуальная (вычисляемая) колонка")
