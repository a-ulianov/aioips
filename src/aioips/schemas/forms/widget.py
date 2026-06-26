"""Схема виджета (формы) IPS.

References:
    ``GET /core/api/forms/{versionId}`` — обёртка ``WidgetDtoNullableResultDto``
    над ``WidgetDto``. ``WidgetDto`` — рекурсивная UI-схема (виджет содержит
    вложенные виджеты ``widgets``).
"""

from typing import Annotated, Any

from pydantic import Field, model_validator

from ..base import EmptyListIfNone, IPSModel


class Widget(IPSModel):
    """Виджет формы IPS — корневой/вложенный UI-элемент (DTO ``WidgetDto``).

    Форма в IPS представлена деревом виджетов: корневой виджет (сама форма) содержит
    вложенные виджеты в поле ``widgets``. ``WidgetDto`` — очень крупная UI-схема
    (более сотни свойств оформления, привязок и поведения). Здесь извлечены
    верхнеуровневые **скалярные** поля, практически полезные для навигации по дереву
    и идентификации виджета (id, тип, имя, привязка к атрибуту, видимость, текст).

    Когда применять: при интерпретации результата :meth:`form` (получение формы по
    идентификатору версии). Для обхода дерева используйте поле ``widgets``.

    Решение по моделированию (обоснование ``Any``): остальные свойства ``WidgetDto`` —
    это вложенные объекты оформления (позиция, размер, шрифт, цвета, отступы, действия,
    изображение и т.п.) и рекурсивные/гетерогенные коллекции. Их структура обширна,
    нестабильна между версиями и не нужна для типового использования обёртки. Поэтому:

    - ``widgets`` (рекурсия) и ``column_collection`` — ``list[Any]`` (сырые объекты);
    - все вложенные UI-объекты сведены в ``properties`` — ``dict[str, Any]`` с сырым
      JSON виджета (поля доступны без потери данных, но без строгой типизации).

    Attributes:
        id: Идентификатор виджета (``id``, строка).
        name: Имя виджета (``name``).
        widget_type: Тип виджета (``widgetType``); определяет вид UI-элемента.
        attribute_type_id: Идентификатор типа привязанного атрибута (``attributeTypeId``).
        attribute_guid: GUID привязанного атрибута (``attributeGuid``).
        attribute_name: Имя привязанного атрибута (``attributeName``).
        text: Текст/подпись виджета (``text``).
        hint: Всплывающая подсказка (``hint``).
        visible: Признак видимости виджета (``visible``).
        disabled_in_design: Признак запрета редактирования в дизайнере
            (``disabledInDesign``).
        widgets: Вложенные виджеты (рекурсия); сырые объекты ``WidgetDto``.
        column_collection: Колонки табличного виджета (``columnCollection``);
            сырые объекты ``WidgetGridColumn``.
        properties: Полный сырой JSON виджета (все поля ``WidgetDto`` как есть),
            включая нетипизированные здесь UI-свойства оформления.
    """

    id: str | None = Field(default=None, description="Идентификатор виджета")
    name: str | None = Field(default=None, description="Имя виджета")
    widget_type: str | None = Field(
        default=None, alias="widgetType", description="Тип виджета (вид UI-элемента)"
    )
    attribute_type_id: int | None = Field(
        default=None,
        alias="attributeTypeId",
        description="Идентификатор типа привязанного атрибута",
    )
    attribute_guid: str | None = Field(
        default=None, alias="attributeGuid", description="GUID привязанного атрибута"
    )
    attribute_name: str | None = Field(
        default=None, alias="attributeName", description="Имя привязанного атрибута"
    )
    text: str | None = Field(default=None, description="Текст/подпись виджета")
    hint: str | None = Field(default=None, description="Всплывающая подсказка")
    visible: bool | None = Field(default=None, description="Признак видимости виджета")
    disabled_in_design: bool | None = Field(
        default=None,
        alias="disabledInDesign",
        description="Запрет редактирования в дизайнере",
    )
    widgets: Annotated[list[Any], EmptyListIfNone] = Field(
        default_factory=list, description="Вложенные виджеты (рекурсия), сырые объекты"
    )
    column_collection: Annotated[list[Any], EmptyListIfNone] = Field(
        default_factory=list,
        alias="columnCollection",
        description="Колонки табличного виджета, сырые объекты",
    )
    properties: dict[str, Any] = Field(
        default_factory=dict, description="Полный сырой JSON виджета (все поля WidgetDto)"
    )

    @model_validator(mode="before")
    @classmethod
    def _capture_properties(cls, data: Any) -> Any:
        """Сохраняет полный сырой JSON виджета в поле ``properties``."""
        if isinstance(data, dict) and "properties" not in data:
            data = {**data, "properties": dict(data)}
        return data
