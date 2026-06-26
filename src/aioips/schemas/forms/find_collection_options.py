"""Схема параметров форменного поиска коллекции объектов IPS.

References:
    ``POST /core/api/forms/findApplicability`` · ``findCollection`` · ``findComposition``
    — тело запроса ``FindCollectionOptions``.
"""

from typing import Annotated

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel
from .widget_grid_column import WidgetGridColumn


class FindCollectionOptions(IPSModel):
    """Параметры форменного поиска коллекции/применимости/состава (``FindCollectionOptions``).

    Тело запроса для методов :meth:`forms_find_applicability`,
    :meth:`forms_find_collection`, :meth:`forms_find_composition`. Задаёт контекст формы
    (тип и версию объекта, контекст выбора), требуемые колонки результата, фильтры по
    типам атрибутов/связей и пагинацию.

    Предусловие по id-пространствам (важно): поля ``*_version_id`` — это идентификаторы
    ВЕРСИЙ (F_ID / ``versionID``), а ``object_type_id`` — идентификатор ТИПА объекта
    (метамодель), не версии и не объекта. См. [[ips-object-model]].

    Все поля необязательны: незаданные параметры сервер интерпретирует значениями по
    умолчанию. Сериализуйте тело как ``model_dump(mode="json", by_alias=True,
    exclude_none=True)``.

    Attributes:
        attribute_type_ids: Идентификаторы типов атрибутов для фильтрации
            (``attributeTypeIds``); ``null`` нормализуется в пустой список.
        columns: Описание колонок результата (``columns``, :class:`WidgetGridColumn`);
            ``null`` нормализуется в пустой список.
        context_object_version_id: Версия объекта-контекста (``contextObjectVersionID``).
        context_selection_version_id: Версия выбора-контекста
            (``contextSelectionVersionID``).
        object_type_id: Идентификатор ТИПА объекта (``objectTypeID``).
        object_version_id: Версия объекта поиска (``objectVersionID``).
        page: Номер страницы пагинации (``page``).
        page_size: Размер страницы пагинации (``pageSize``).
        relation_type_id_object_type_ids_collection: Фильтр пар «тип связи → типы
            объектов» (``relationTypeIDObjectTypeIdsCollection``); список сырых объектов
            ``RelationTypeIDObjectTypeIds``, ``null`` нормализуется в пустой список.
    """

    attribute_type_ids: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list,
        alias="attributeTypeIds",
        description="Идентификаторы типов атрибутов для фильтрации",
    )
    columns: Annotated[list[WidgetGridColumn], EmptyListIfNone] = Field(
        default_factory=list, description="Описание колонок результата"
    )
    context_object_version_id: int | None = Field(
        default=None,
        alias="contextObjectVersionID",
        description="Версия объекта-контекста",
    )
    context_selection_version_id: int | None = Field(
        default=None,
        alias="contextSelectionVersionID",
        description="Версия выбора-контекста",
    )
    object_type_id: int | None = Field(
        default=None, alias="objectTypeID", description="Идентификатор типа объекта"
    )
    object_version_id: int | None = Field(
        default=None, alias="objectVersionID", description="Версия объекта поиска"
    )
    page: int | None = Field(default=None, description="Номер страницы пагинации")
    page_size: int | None = Field(
        default=None, alias="pageSize", description="Размер страницы пагинации"
    )
    relation_type_id_object_type_ids_collection: Annotated[
        list[dict[str, object]], EmptyListIfNone
    ] = Field(
        default_factory=list,
        alias="relationTypeIDObjectTypeIdsCollection",
        description="Фильтр пар «тип связи → типы объектов»",
    )
