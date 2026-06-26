"""Методы раздела табличных отчётов IPS Web API."""

from .table_report import TableReportMixin
from .table_report_content import ReportContentMixin
from .table_report_math_total import TableReportMathTotalMixin
from .update_report_template import UpdateReportTemplateMixin


class TableReportAPI(
    TableReportMixin,
    TableReportMathTotalMixin,
    ReportContentMixin,
    UpdateReportTemplateMixin,
):
    """Объединяет методы раздела табличных отчётов.

    References:
        Эндпоинты ``/core/api/tableReport/*`` IPS Server Web API.
    """


__all__ = ["TableReportAPI"]
