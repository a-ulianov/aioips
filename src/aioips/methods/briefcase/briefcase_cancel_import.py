"""Метод отмены текущего импорта Портфеля."""

from typing import Any

from ...core import APIManager


class BriefcaseCancelImportMixin(APIManager):
    """Реализует ``POST /core/api/briefcase/CancelImport`` (``Briefcase_CancelImport``)."""

    async def briefcase_cancel_import(self: "BriefcaseCancelImportMixin") -> None:
        """Отменяет текущую операцию импорта Портфеля.

        Портфель — это пакет экспорта/импорта объектов IPS («briefcase»). Метод посылает
        запрос на прерывание выполняющегося импорта. Операция безопасна: если импорт не
        запущен, вызов является фактическим no-op и не считается ошибкой.

        POST без доменного тела: IPS требует тело, поэтому отправляется пустой объект
        ``{}``; параметров метод не принимает (операция определяется по сессии). Общий
        статус задачи — :meth:`briefcase_status`.

        Returns:
            ``None``. Успех подтверждается отсутствием исключения.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.briefcase_cancel_import()  # безопасно, даже если импорта нет

        Notes:
            operationId ``Briefcase_CancelImport``; путь
            ``POST /core/api/briefcase/CancelImport`` (тело ``{}``). Связанные:
            :meth:`briefcase_status`, :meth:`briefcase_check_metadata_result`.
        """
        payload: dict[str, Any] = {}
        await self._request("post", "/core/api/briefcase/CancelImport", json=payload)
