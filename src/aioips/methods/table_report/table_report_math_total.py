"""Метод расчёта итога табличного отчёта по математическому выражению."""

from typing import Any

from ...core import APIManager


class TableReportMathTotalMixin(APIManager):
    """Реализует ``GET /core/api/tableReport/getMathTotal``.

    operationId ``TableReport_GetMathTotal``.
    """

    async def table_report_math_total(
        self: "TableReportMathTotalMixin",
        *,
        math_total: str | None = None,
    ) -> str:
        """Возвращает строковый итог табличного отчёта по математическому выражению.

        Сервер вычисляет итоговое значение на основе переданного математического
        выражения (формулы итога) и возвращает его строковое представление —
        пригодное, например, для вывода в итоговой строке отчёта.

        Когда применять: для получения готового текстового итога по формуле, не
        пересчитывая его на стороне клиента. Структуру самого отчёта (где задаётся
        итоговая строка) читает :meth:`table_report`.

        Args:
            math_total: Математическое выражение (формула) итога. Передаётся в строке
                запроса как ``mathTotal`` только если задано; при ``None`` параметр не
                отправляется, и метод возвращает пустую строку.

        Returns:
            Строковое представление вычисленного итога. Если ``math_total`` равно
            ``None`` (запрос без выражения), метод возвращает ``""``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                total = await ips.table_report_math_total(math_total="sum(weight)")
                print(total)

        Notes:
            operationId ``TableReport_GetMathTotal``; путь
            ``GET /core/api/tableReport/getMathTotal`` (ответ — строка).
        """
        if math_total is None:
            return ""
        params: dict[str, Any] = {"mathTotal": math_total}
        data = await self._request("get", "/core/api/tableReport/getMathTotal", params=params)
        return "" if data is None else str(data)
