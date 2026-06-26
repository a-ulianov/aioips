"""Метод отмены текущего экспорта Портфеля."""

from typing import Any

from ...core import APIManager


class BriefcaseCancelExportMixin(APIManager):
    """Реализует ``POST /core/api/briefcase/CancelExport`` (``Briefcase_CancelExport``)."""

    async def briefcase_cancel_export(self: "BriefcaseCancelExportMixin") -> None:
        """Отменяет текущую операцию экспорта Портфеля.

        Портфель — это пакет экспорта/импорта объектов IPS («briefcase»). Метод посылает
        запрос на прерывание выполняющегося экспорта. Операция безопасна: если экспорт не
        запущен, вызов является фактическим no-op и не считается ошибкой.

        POST без доменного тела: IPS требует тело, поэтому отправляется пустой объект
        ``{}``; параметров метод не принимает (операция определяется по сессии). Прогресс
        экспорта — :meth:`briefcase_export_progress`.

        Returns:
            ``None``. Успех подтверждается отсутствием исключения.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.briefcase_cancel_export()  # безопасно, даже если экспорта нет

        Notes:
            operationId ``Briefcase_CancelExport``; путь
            ``POST /core/api/briefcase/CancelExport`` (тело ``{}``). Связанные:
            :meth:`briefcase_export_progress`, :meth:`briefcase_status`.
        """
        payload: dict[str, Any] = {}
        await self._request("post", "/core/api/briefcase/CancelExport", json=payload)
