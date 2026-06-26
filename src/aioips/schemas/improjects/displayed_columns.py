"""Схема набора отображаемых колонок грида проекта IPS (Improject).

References:
    ``GET /core/api/improjects/grid-columns`` — ``DisplayedColumnsDto``.
"""

from typing import Annotated, Any

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class DisplayedColumns(IPSModel):
    """Набор колонок, отображаемых в гриде (таблице) проекта Improject.

    Возвращается методом :meth:`grid_columns`. Описывает, какие колонки
    показывать в табличном представлении проекта управления проектами и в каком
    порядке. Используйте для построения шапки таблицы задач на клиенте/в MCP-
    инструменте перед загрузкой самого проекта через :meth:`project`.

    Элементы ``columns`` (DTO ``ColumnDto``) типизированы как «сырые» словари
    (``list[dict[str, Any]]``): структура колонки невелика, но нестабильна между
    версиями API (значимые ключи — ``id`` строкового идентификатора колонки и
    необязательная ``width``); для раздела READ достаточно доступа к ним без
    жёсткой схемы.

    Обязательных полей нет — при отсутствии настроек список колонок пуст.

    Attributes:
        columns: Колонки грида проекта (элементы ``ColumnDto`` в виде «сырых»
            словарей; ключ ``id`` — строковый идентификатор колонки, ``width`` —
            ширина в пикселях, может отсутствовать).
    """

    columns: Annotated[list[dict[str, Any]], EmptyListIfNone] = Field(
        default_factory=list, description="Колонки грида проекта (ColumnDto)"
    )
