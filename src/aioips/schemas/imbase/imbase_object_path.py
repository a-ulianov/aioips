"""Схема пути к объекту справочной системы IMBASE.

References:
    ``GET /core/api/imbase/object/{objectId}/path`` и связанные эндпоинты —
    ``ImBaseObjectPathDto`` (внутри обёртки ``...NullableResultDto``).
"""

from typing import Annotated, Any

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class ImBaseObjectPath(IPSModel):
    """Путь к объекту IMBASE в иерархии каталогов и справочников.

    Описывает положение объекта IMBASE в дереве справочной системы: цепочку узлов
    от корневого каталога верхнего уровня до самого объекта (включительно).
    Применяется для навигации, построения «хлебных крошек» и определения каталога,
    которому принадлежит объект.

    Когда применять: при отображении местоположения записи/папки IMBASE в дереве.
    Отдаётся методами :meth:`imbase_object_path` (по id объекта),
    :meth:`imbase_object_path_by_key` (по id ключа) и
    :meth:`imbase_linked_object_path` (для связанного объекта).

    Поля ``path`` и ``objects_path`` описывают один и тот же путь в разных формах:
    ``path`` — строковые идентификаторы узлов дерева, ``objects_path`` — структуры
    «ключ объекта» (``objectId`` + нестабильный ``relationId``). ``object_id`` —
    идентификатор объекта IMBASE (id-пространство объектов IMBASE), ``record_id`` —
    id записи таблицы, если объект является записью Ярлыка таблицы IMBASE.

    Attributes:
        top_parent_object_id: Идентификатор родительского объекта верхнего уровня
            (как правило, каталога).
        top_parent_catalog_type: Тип каталога верхнего уровня (``None``, если не задан).
        path: Идентификаторы узлов дерева на пути к объекту, включая его самого
            (строковые значения).
        objects_path: Узлы пути в виде структур «ключ объекта» (``object_id`` +
            необязательный ``relation_id``); ``relation_id`` нестабилен, не кэшировать.
        record_id: Идентификатор записи таблицы, если объект — запись Ярлыка таблицы
            IMBASE (иначе ``None``).
        object_id: Идентификатор объекта IMBASE.
    """

    top_parent_object_id: int = Field(
        description="Идентификатор родительского объекта верхнего уровня (каталога)"
    )
    top_parent_catalog_type: str | None = Field(
        default=None, description="Тип каталога верхнего уровня (None, если не задан)"
    )
    path: Annotated[list[str], EmptyListIfNone] = Field(
        default_factory=list,
        description="Идентификаторы узлов дерева на пути к объекту, включая его самого",
    )
    objects_path: Annotated[list[dict[str, Any]], EmptyListIfNone] = Field(
        default_factory=list,
        description="Узлы пути как структуры «ключ объекта» (objectId + relationId)",
    )
    record_id: int | None = Field(
        default=None,
        description="Id записи таблицы, если объект — запись Ярлыка таблицы IMBASE",
    )
    object_id: int = Field(description="Идентификатор объекта IMBASE")
