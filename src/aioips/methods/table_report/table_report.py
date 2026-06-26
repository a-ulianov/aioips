"""Метод получения шаблона табличного отчёта объекта."""

from ...core import APIManager
from ...schemas.table_report import TableReport


class TableReportMixin(APIManager):
    """Реализует ``GET /core/api/tableReport/{objectId}/get``.

    operationId ``TableReport_GetTemplateOfTableReportService``.
    """

    async def table_report(self: "TableReportMixin", object_id: int) -> TableReport:
        """Возвращает шаблон табличного отчёта, настроенный для объекта.

        Описывает, как для данного объекта формируется табличный отчёт: применяемые
        шаблон и отчёт, состав колонок, нумерация строк и набор итоговых элементов
        (итоговая строка, количество позиций, дата печати, номера страниц).

        Когда применять: чтобы прочитать текущую конфигурацию табличного отчёта объекта
        (например, перед генерацией документа отчёта или для отображения настроек).
        Для расчёта итогового значения по математическому выражению используйте
        :meth:`table_report_math_total`.

        Предусловие по id-пространству: аргумент — идентификатор ОБЪЕКТА (``objectID`` /
        F_OBJECT_ID), общий для всех версий, а не идентификатор версии (``id`` / F_ID).

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), для которого
                запрашивается шаблон табличного отчёта. Не идентификатор версии.

        Returns:
            Шаблон отчёта по схеме :class:`TableReport`. Значимые поля идентичности —
            ``template_id`` (``templateID``) и ``report_id`` (``reportID``); состав
            колонок — ``columns``; итоговые флаги — ``result_item``, ``count_items``.

        Raises:
            IPSError: При ошибочном ответе сервера (в т. ч. 404, если для объекта нет
                настроенного табличного отчёта).

        Example:
            async with IPSClient(config=config) as ips:
                report = await ips.table_report(102550)  # 102550 = objectID
                print(report.report_caption, len(report.columns))

        Notes:
            operationId ``TableReport_GetTemplateOfTableReportService``; путь
            ``GET /core/api/tableReport/{objectId}/get`` (ответ — ``TableReportDto``).
        """
        data = await self._request("get", f"/core/api/tableReport/{object_id}/get")
        return TableReport.model_validate(data)
