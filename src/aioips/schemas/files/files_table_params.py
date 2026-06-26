"""Схемы тел запросов табличных методов сервиса имён файлов IPS Web API.

References:
    DTO ``ObjectIdsWithColumnsDto`` (``Files_GetFilesTableByFields``),
    ``ObjectIdsWithColumnsFileNameDto`` (``Files_GetFilesTableAllAttributes``),
    ``ObjectSnapshotIds`` (``Files_GetFilesTableWithSnapshotIds``).
"""

from typing import Annotated

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class ObjectIdsWithColumnsDto(IPSModel):
    """Тело запроса: список объектов и выбираемые колонки таблицы файлов.

    Используется методом ``get_files_table_by_fields``: задаёт, по каким объектам
    собрать таблицу файлов и какие колонки (поля) включить в результат.

    Предусловие по id-пространству: :attr:`object_ids` — ``ObjectID``
    (F_OBJECT_ID), а не ``id`` версий.

    Attributes:
        object_ids: Идентификаторы ОБЪЕКТОВ (DTO ``objectIds`` / ``ObjectID``,
            int64), для которых нужна таблица файлов. ``null`` → ``[]``.
        column_names: Имена колонок (полей), включаемых в результат (DTO
            ``columnNames``). Пустой список — поведение по умолчанию сервера.
            ``null`` → ``[]``.
    """

    object_ids: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list, description="Идентификаторы объектов (ObjectID)"
    )
    column_names: Annotated[list[str], EmptyListIfNone] = Field(
        default_factory=list, description="Имена колонок, включаемых в выборку"
    )


class ObjectIdsWithColumnsFileNameDto(IPSModel):
    """Тело запроса: объекты, колонки и фильтр по имени файла для таблицы файлов.

    Используется методом ``get_files_table_all_attributes``: то же, что
    :class:`ObjectIdsWithColumnsDto`, плюс необязательный фильтр по имени файла.

    Attributes:
        file_name: Имя файла для фильтрации (DTO ``fileName``). ``None`` —
            фильтр не применяется.
        object_ids: Идентификаторы ОБЪЕКТОВ (DTO ``objectIds`` / ``ObjectID``,
            int64). ``null`` → ``[]``.
        column_names: Имена колонок (полей) результата (DTO ``columnNames``).
            ``null`` → ``[]``.
    """

    file_name: str | None = Field(default=None, description="Имя файла для фильтрации")
    object_ids: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list, description="Идентификаторы объектов (ObjectID)"
    )
    column_names: Annotated[list[str], EmptyListIfNone] = Field(
        default_factory=list, description="Имена колонок, включаемых в выборку"
    )


class ObjectSnapshotIds(IPSModel):
    """Тело запроса: пары «объект — снимок» для таблицы файлов на момент снимка.

    Используется методом ``get_files_table_with_snapshot_ids``: задаёт объекты и
    соответствующие им идентификаторы снимков (snapshot), чтобы получить таблицу
    файлов в состоянии на момент конкретных снимков, а не текущем.

    Предусловие по id-пространству: :attr:`object_ids` — ``ObjectID``;
    :attr:`snapshot_ids` — идентификаторы СНИМКОВ (отдельное пространство id,
    не версии и не объекты).

    Attributes:
        object_ids: Идентификаторы ОБЪЕКТОВ (DTO ``objectIds`` / ``ObjectID``,
            int64). ``null`` → ``[]``.
        snapshot_ids: Идентификаторы СНИМКОВ (DTO ``snapshotIds``, int64),
            позиционно сопоставляемые объектам. ``null`` → ``[]``.
    """

    object_ids: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list, description="Идентификаторы объектов (ObjectID)"
    )
    snapshot_ids: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list, description="Идентификаторы снимков (snapshot)"
    )
