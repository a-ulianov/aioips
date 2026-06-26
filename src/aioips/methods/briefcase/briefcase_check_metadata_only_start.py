"""Метод запуска проверки метаданных Портфеля (только метаданные)."""

from typing import Any

from ...core import APIManager


class BriefcaseCheckMetadataOnlyStartMixin(APIManager):
    """Реализует ``POST /core/api/briefcase/CheckMetadataOnlyStart``.

    operationId ``Briefcase_CheckMetadataOnlyStart``.
    """

    async def briefcase_check_metadata_only_start(
        self: "BriefcaseCheckMetadataOnlyStartMixin",
        *,
        briefcase_id: str | None = None,
        briefcase_path: str | None = None,
        system_only: bool | None = None,
        confirm: bool = False,
    ) -> None:
        """Запускает проверку метаданных Портфеля без чтения данных (МУТИРУЮЩАЯ, ``confirm``).

        Портфель — это пакет экспорта/импорта объектов IPS («briefcase»). Метод стартует
        серверную фоновую задачу проверки СОВМЕСТИМОСТИ метаданных портфеля с текущей
        базой, не загружая сами объекты (лёгкая проверка перед импортом). Операция
        запускает фоновый процесс на сервере, поэтому защищена ``confirm``: без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО запроса. Результат
        проверки читают через :meth:`briefcase_check_metadata_result`, статус —
        :meth:`briefcase_status`; отмена — :meth:`briefcase_check_metadata_cancel`.
        Полная проверка (с данными) — :meth:`briefcase_check_metadata_start`.

        Портфель задаётся ЛИБО идентификатором (``briefcase_id``), ЛИБО путём к файлу
        (``briefcase_path``) — параметры передаются строкой запроса; тела у запроса нет.

        Args:
            briefcase_id: GUID портфеля (query ``briefcaseId``, формат uuid). ``None`` —
                параметр не передаётся.
            briefcase_path: Путь к файлу портфеля (query ``briefcasePath``). ``None`` —
                параметр не передаётся.
            system_only: Проверять только системные метаданные (query ``systemOnly``).
                ``None`` — параметр не передаётся (поведение сервера по умолчанию).
            confirm: Подтверждение запуска фоновой задачи. Без ``True`` метод не делает
                запрос и поднимает :class:`ValueError` (защитный гейт).

        Returns:
            ``None``. Метод лишь запускает проверку; её исход читается отдельно
            (:meth:`briefcase_check_metadata_result`). Успех старта подтверждается
            отсутствием исключения.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.briefcase_check_metadata_only_start(
                    briefcase_path="X:/export/parts.brief", confirm=True
                )
                result = await ips.briefcase_check_metadata_result()

        Notes:
            operationId ``Briefcase_CheckMetadataOnlyStart``; путь
            ``POST /core/api/briefcase/CheckMetadataOnlyStart`` (query ``briefcaseId``,
            ``briefcasePath``, ``systemOnly``; без тела). Связанные:
            :meth:`briefcase_check_metadata_start`,
            :meth:`briefcase_check_metadata_result`, :meth:`briefcase_status`.
        """
        if confirm is not True:
            raise ValueError(
                "Запуск проверки метаданных Портфеля стартует фоновую задачу: "
                "передайте confirm=True"
            )
        params: dict[str, Any] = {}
        if briefcase_id is not None:
            params["briefcaseId"] = briefcase_id
        if briefcase_path is not None:
            params["briefcasePath"] = briefcase_path
        if system_only is not None:
            params["systemOnly"] = str(system_only).lower()
        await self._request(
            "post",
            "/core/api/briefcase/CheckMetadataOnlyStart",
            json={},
            params=params,
        )
