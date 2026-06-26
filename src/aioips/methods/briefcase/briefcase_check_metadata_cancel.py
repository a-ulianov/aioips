"""Метод отмены текущей проверки метаданных Портфеля."""

from typing import Any

from ...core import APIManager


class BriefcaseCheckMetadataCancelMixin(APIManager):
    """Реализует ``POST /core/api/briefcase/CheckMetadataCancel``.

    operationId ``Briefcase_CheckMetadataCancel``.
    """

    async def briefcase_check_metadata_cancel(
        self: "BriefcaseCheckMetadataCancelMixin",
    ) -> None:
        """Отменяет текущую проверку совместимости метаданных Портфеля.

        Портфель — это пакет экспорта/импорта объектов IPS («briefcase»). Перед импортом
        сервер сверяет метаданные пакета с базой-приёмником; этот метод прерывает такую
        проверку. Операция безопасна: если проверка не запущена, вызов является фактическим
        no-op и не считается ошибкой.

        POST без доменного тела: IPS требует тело, поэтому отправляется пустой объект
        ``{}``; параметров метод не принимает (проверка определяется по сессии). Результат
        проверки — :meth:`briefcase_check_metadata_result`.

        Returns:
            ``None``. Успех подтверждается отсутствием исключения.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.briefcase_check_metadata_cancel()  # безопасно, даже если проверки нет

        Notes:
            operationId ``Briefcase_CheckMetadataCancel``; путь
            ``POST /core/api/briefcase/CheckMetadataCancel`` (тело ``{}``). Связанные:
            :meth:`briefcase_check_metadata_result`.
        """
        payload: dict[str, Any] = {}
        await self._request("post", "/core/api/briefcase/CheckMetadataCancel", json=payload)
