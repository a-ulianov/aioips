"""Метод получения результата проверки метаданных Портфеля."""

from typing import Any

from ...core import APIManager
from ...schemas.briefcase import CheckMetadataResponse


class BriefcaseCheckMetadataResultMixin(APIManager):
    """Реализует ``POST /core/api/briefcase/CheckMetadataResult``.

    operationId ``Briefcase_CheckMetadataResult``.
    """

    async def briefcase_check_metadata_result(
        self: "BriefcaseCheckMetadataResultMixin",
    ) -> CheckMetadataResponse:
        """Возвращает результат фоновой проверки совместимости метаданных Портфеля.

        Портфель — это пакет экспорта/импорта объектов IPS («briefcase»). Перед импортом
        сервер сверяет метаданные пакета (типы, атрибуты, словари) с метаданными
        базы-приёмника; данный метод отдаёт итог этой проверки.

        Read-only POST: доменного тела нет, но IPS требует тело, поэтому отправляется
        пустой объект ``{}``; параметров метод не принимает (проверка определяется по
        сессии). Текущую проверку можно прервать через :meth:`briefcase_check_metadata_cancel`.

        Когда применять: после запуска проверки метаданных — чтобы решить, безопасен ли
        импорт. Если проверка не выполнялась/не дала расхождений, ``error_message`` будет
        ``None``, а ``check_metadata_errors`` — пустым списком.

        Returns:
            :class:`~aioips.schemas.briefcase.CheckMetadataResponse`: ``error_message``
            (общая ошибка или ``None``) и ``check_metadata_errors`` — журнал расхождений
            метаданных (сырые записи лога: тип, категория, тексты различий).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                result = await ips.briefcase_check_metadata_result()
                if result.error_message or result.check_metadata_errors:
                    ...  # импорт небезопасен — разобрать расхождения

        Notes:
            operationId ``Briefcase_CheckMetadataResult``; путь
            ``POST /core/api/briefcase/CheckMetadataResult`` (тело ``{}``). Связанные:
            :meth:`briefcase_check_metadata_cancel`.
        """
        payload: dict[str, Any] = {}
        data = await self._request("post", "/core/api/briefcase/CheckMetadataResult", json=payload)
        return CheckMetadataResponse.model_validate(data)
