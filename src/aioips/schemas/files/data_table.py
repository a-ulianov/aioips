"""Схема обобщённой табличной выборки (DataTable) IPS Web API.

References:
    DTO ``DataTableDto`` — ответ табличных методов сервиса имён файлов
    (``/core/api/files/fileNamesService/getFile*Table*``), например
    operationId ``Files_GetFileNameTable``, ``Files_GetFilesTable``.
"""

from typing import Annotated, Any

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class DataTableDto(IPSModel):
    """Обобщённая табличная выборка: имена колонок плюс строки-массивы ячеек.

    Универсальный контейнер для табличных данных IPS (аналог ``DataTable``).
    Возвращается методами выборки метаданных о файлах vault, отдающими результат
    в виде таблицы: каждая строка — массив значений ячеек, порядок ячеек
    соответствует порядку колонок в :attr:`columns`. Это операции ЧТЕНИЯ
    (POST-verb, но данные не изменяются).

    Чтобы прочитать значение конкретной колонки строки, найдите её индекс в
    :attr:`columns` и обратитесь к этому индексу в массиве строки
    (``row[columns.index("ИмяКолонки")]``). Типы ячеек разнородны
    (строки/числа/даты), поэтому моделируются как ``Any``.

    Attributes:
        columns: Имена колонок (DTO ``columns``, ``ColumnName``) в порядке
            следования ячеек в каждой строке. ``null`` от сервера → ``[]``.
        rows: Строки таблицы (DTO ``rows``); каждая строка — массив значений
            ячеек, выровненный по :attr:`columns`. ``null`` от сервера → ``[]``.
            Пустой список — нет данных.
    """

    columns: Annotated[list[str], EmptyListIfNone] = Field(
        default_factory=list, description="Имена колонок (ColumnName)"
    )
    rows: Annotated[list[list[Any]], EmptyListIfNone] = Field(
        default_factory=list, description="Строки таблицы (массивы значений ячеек)"
    )
