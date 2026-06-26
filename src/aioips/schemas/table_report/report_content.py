"""Схемы генерации содержимого табличного отчёта IPS.

References:
    ``POST /core/api/tableReport/{objectId}/reportContent`` —
    запрос ``ReportCreatorParams``, ответ ``DocumentContentDto``.
"""

from typing import Annotated, Any

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class ReportCreatorParams(IPSModel):
    """Параметры формирования содержимого табличного отчёта.

    Управляет тем, какие позиции попадут в табличный отчёт объекта при вызове
    :meth:`report_content`: явный список выбранных элементов, тип родителя,
    флаг «только выбранные» и идентификатор именованной выборки. Все поля
    необязательны; при значениях по умолчанию формируется отчёт по полному составу.

    Attributes:
        selected_ids: Идентификаторы выбранных элементов (int64), которые включить в
            отчёт. ``None`` — без явного списка. Учитывается, когда ``only_selected``
            истинно. Это id элементов состава, а не идентификатор самого объекта-отчёта.
        parent_type_id: Идентификатор типа родителя (int32). ``0`` — не задан.
        only_selected: Включать в отчёт только элементы из ``selected_ids``.
            По умолчанию ``False`` (весь состав).
        selection_id: Идентификатор именованной серверной выборки (int32). ``0`` — без
            выборки.
    """

    selected_ids: list[int] | None = Field(
        default=None, description="Идентификаторы выбранных элементов (int64)"
    )
    parent_type_id: int = Field(default=0, description="Идентификатор типа родителя (int32)")
    only_selected: bool = Field(default=False, description="Только выбранные элементы")
    selection_id: int = Field(default=0, description="Идентификатор именованной выборки (int32)")


class DocumentContent(IPSModel):
    """Содержимое сгенерированного документа табличного отчёта IPS.

    Возвращается методом :meth:`report_content` и описывает дерево страниц
    документа, его метаданные и параметры оформления. Это представление содержимого
    документа в объектной модели IPS (не готовый бинарный файл): страницы и шаблон —
    деревья узлов документа.

    Крупные/вложенные структуры (страницы, корень шаблона, форматы, формулы) приходят
    как разнородные узлы документа; их детальная типизация выходит за рамки read-обёртки,
    поэтому они объявлены слабо типизированными (``list[Any]`` / ``dict[str, Any]``) —
    это устойчиво к различиям версий API и не теряет данные.

    Attributes:
        doc_pages: Страницы документа (узлы дерева ``DocTreeNode``).
        dpi: Разрешение документа (точек на дюйм) как структура координат.
        default_char_format: Формат символов по умолчанию.
        blob_id: Идентификатор BLOB-содержимого (int64).
        object_id: Идентификатор ОБЪЕКТА документа (``objectID`` / F_OBJECT_ID, int64).
        object_guid: GUID объекта документа.
        type_id: Идентификатор типа документа (int32).
        document_id: Строковый идентификатор документа.
        modified: Признак изменённого (несохранённого) состояния документа.
        file_name: Имя файла документа.
        is_template: Признак того, что документ является шаблоном.
        is_formula_lib: Признак того, что документ является библиотекой формул.
        is_scan_document: Признак документа-скана.
        template_root: Корневой узел дерева шаблона (``DocTreeNode``).
        mode: Режим открытия документа (enum ``OpenDocumentMode`` строкой).
        formulas: Описания формул документа.
    """

    doc_pages: Annotated[list[Any], EmptyListIfNone] = Field(
        default_factory=list, description="Страницы документа (узлы DocTreeNode)"
    )
    dpi: dict[str, Any] | None = Field(default=None, description="Разрешение документа (DPI)")
    default_char_format: dict[str, Any] | None = Field(
        default=None, description="Формат символов по умолчанию"
    )
    blob_id: int = Field(default=0, description="Идентификатор BLOB-содержимого (int64)")
    object_id: int = Field(default=0, description="Идентификатор ОБЪЕКТА документа (int64)")
    object_guid: str | None = Field(default=None, description="GUID объекта документа")
    type_id: int = Field(default=0, description="Идентификатор типа документа (int32)")
    document_id: str | None = Field(default=None, description="Строковый идентификатор документа")
    modified: bool = Field(default=False, description="Признак изменённого состояния")
    file_name: str | None = Field(default=None, description="Имя файла документа")
    is_template: bool = Field(default=False, description="Документ является шаблоном")
    is_formula_lib: bool = Field(default=False, description="Документ является библиотекой формул")
    is_scan_document: bool = Field(default=False, description="Документ-скан")
    template_root: dict[str, Any] | None = Field(
        default=None, description="Корневой узел дерева шаблона (DocTreeNode)"
    )
    mode: str | None = Field(default=None, description="Режим открытия документа (enum-строка)")
    formulas: Annotated[list[Any], EmptyListIfNone] = Field(
        default_factory=list, description="Описания формул документа"
    )
