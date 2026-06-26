"""Схема шаблона табличного отчёта IPS.

References:
    ``GET /core/api/tableReport/{objectId}/get`` — ``TableReportDto``.
"""

from typing import Annotated, Any

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class TableReport(IPSModel):
    """Шаблон табличного отчёта, настроенный для объекта IPS.

    Описывает, как для данного объекта формируется табличный отчёт: какой шаблон и
    отчёт применяются, какие колонки выводятся, как нумеруются строки и какие итоговые
    элементы (итоговая строка, количество позиций, дата печати, номера страниц) включены.
    Возвращается методом :meth:`table_report` по идентификатору ОБЪЕКТА.

    Идентификаторы шаблона и отчёта в API записаны с заглавным акронимом ``ID``
    (``templateID``, ``reportID``), поэтому для них заданы явные алиасы (автогенератор
    ``to_camel`` дал бы ``templateId``/``reportId`` и поля не считались бы).

    Крупные/вложенные структуры (``columns``, ``rowNumbers``, ``resultItem``) приходят как
    разнородные объекты конфигурации колонок и итогов; их детальная типизация выходит за
    рамки read-обёртки, поэтому они объявлены слабо типизированными (``list[Any]`` /
    ``dict[str, Any]``) — это устойчиво к различиям версий API и не теряет данные.

    Attributes:
        template_id: Идентификатор шаблона отчёта (``templateID``). Целое (int64).
        template_name: Название шаблона.
        report_id: Идентификатор отчёта (``reportID``). Целое (int64).
        report_name: Наименование отчёта.
        report_caption: Заголовок отчёта.
        columns: Описания колонок отчёта (разнородные объекты конфигурации).
        row_numbers: Признак вывода номеров строк (true — нумеровать строки).
        row_numbers_column_width: Ширина колонки с номерами строк, в мм.
        row_numbers_column_caption: Заголовок колонки с номерами строк.
        result_item: Признак вывода итоговой строки.
        count_items: Признак вывода количества позиций.
        date_print: Формат печати даты (enum ``DatePrintFormats``: ``none``/``date``/``time``
            и т. п.) строкой; ``None``, если не задан. Это НЕ дата, а режим её вывода.
        page_number: Позиция вывода номеров страниц (enum ``PageNumberPosition`` строкой).
        generated_doc_type_guid: GUID типа генерируемого по умолчанию документа.
    """

    template_id: int = Field(
        default=0, alias="templateID", description="Идентификатор шаблона отчёта"
    )
    template_name: str | None = Field(default=None, description="Название шаблона")
    report_id: int = Field(default=0, alias="reportID", description="Идентификатор отчёта")
    report_name: str | None = Field(default=None, description="Наименование отчёта")
    report_caption: str | None = Field(default=None, description="Заголовок отчёта")
    columns: Annotated[list[Any], EmptyListIfNone] = Field(
        default_factory=list, description="Описания колонок отчёта"
    )
    row_numbers: bool = Field(default=False, description="Выводить номера строк")
    row_numbers_column_width: int = Field(
        default=0, description="Ширина колонки с номерами строк, в мм"
    )
    row_numbers_column_caption: str | None = Field(
        default=None, description="Заголовок колонки с номерами строк"
    )
    result_item: bool = Field(default=False, description="Выводить итоговую строку")
    count_items: bool = Field(default=False, description="Выводить количество позиций")
    date_print: str | None = Field(default=None, description="Формат печати даты (enum-строка)")
    page_number: str | None = Field(default=None, description="Позиция номеров страниц (enum)")
    generated_doc_type_guid: str | None = Field(
        default=None, description="GUID типа генерируемого по умолчанию документа"
    )
