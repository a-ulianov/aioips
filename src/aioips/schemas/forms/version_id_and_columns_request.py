"""Схема запроса списка объектов формы по версиям и колонкам IPS.

References:
    ``POST /core/api/forms/findObjectsList`` — тело запроса
    ``VersionIdAndColumns4Request``.
"""

from typing import Annotated

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel
from .widget_grid_column import WidgetGridColumn


class VersionIdAndColumns4Request(IPSModel):
    """Параметры запроса списка объектов формы (``VersionIdAndColumns4Request``).

    Тело запроса для :meth:`forms_find_objects_list`. Задаёт перечень версий объектов,
    для которых нужно вернуть строки, набор колонок результата и режим трактовки
    переданных идентификаторов.

    Предусловие по id-пространству (важно): ``object_version_ids`` — идентификаторы
    ВЕРСИЙ объектов (F_ID / ``versionID``), не идентификаторы объектов. Флаг
    ``use_version_id`` управляет тем, как сервер трактует эти идентификаторы при выборке.
    См. [[ips-object-model]].

    Все поля необязательны. Сериализуйте тело как ``model_dump(mode="json",
    by_alias=True, exclude_none=True)``.

    Attributes:
        object_version_ids: Идентификаторы ВЕРСИЙ объектов (``objectVersionIds``);
            ``null`` нормализуется в пустой список.
        columns: Описание колонок результата (``columns``, :class:`WidgetGridColumn`);
            ``null`` нормализуется в пустой список.
        use_version_id: Трактовать идентификаторы как версии (``useVersionId``).
    """

    object_version_ids: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list,
        alias="objectVersionIds",
        description="Идентификаторы версий объектов",
    )
    columns: Annotated[list[WidgetGridColumn], EmptyListIfNone] = Field(
        default_factory=list, description="Описание колонок результата"
    )
    use_version_id: bool | None = Field(
        default=None,
        alias="useVersionId",
        description="Трактовать идентификаторы как версии",
    )
