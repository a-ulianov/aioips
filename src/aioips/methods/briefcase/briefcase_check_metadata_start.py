"""Метод запуска проверки метаданных Портфеля (по тегам импорта)."""

from typing import Any

from ...core import APIManager


class BriefcaseCheckMetadataStartMixin(APIManager):
    """Реализует ``POST /core/api/briefcase/CheckMetadataStart``.

    operationId ``Briefcase_CheckMetadataStart``.
    """

    async def briefcase_check_metadata_start(
        self: "BriefcaseCheckMetadataStartMixin",
        request: dict[str, Any],
        *,
        confirm: bool = False,
    ) -> None:
        """Запускает полную проверку метаданных Портфеля по запросу импорта (МУТИРУЮЩАЯ).

        Портфель — это пакет экспорта/импорта объектов IPS. Метод стартует серверную
        фоновую задачу проверки метаданных для конкретного запроса импорта
        (``ImportRequestDTO``) — более полную, чем
        :meth:`briefcase_check_metadata_only_start`. Операция запускает фоновый процесс,
        поэтому защищена ``confirm``: без ``confirm=True`` поднимается :class:`ValueError`
        ещё ДО запроса. Это безопасный предимпортный шаг: он НЕ записывает объекты в базу
        (в отличие от :meth:`briefcase_start_import`). Результат читают через
        :meth:`briefcase_check_metadata_result`, статус — :meth:`briefcase_status`.

        Тело ``request`` (``ImportRequestDTO``) описывает источник портфеля и режим:
        ``id``/``path``/``location`` (что импортировать), ``importObjectsOnly``,
        ``ignoreErrors``, ``createOnly``, ``synchronizeIMS_CONFIGS``, ``newOwnerId``.

        Args:
            request: Тело запроса ``ImportRequestDTO`` в виде словаря; отправляется
                как JSON-тело.
            confirm: Подтверждение запуска фоновой задачи. Без ``True`` метод не делает
                запрос и поднимает :class:`ValueError` (защитный гейт).

        Returns:
            ``None``. Метод лишь запускает проверку; её исход читается отдельно
            (:meth:`briefcase_check_metadata_result`).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.briefcase_check_metadata_start(
                    {"path": "X:/export/parts.brief", "ignoreErrors": False},
                    confirm=True,
                )
                result = await ips.briefcase_check_metadata_result()

        Notes:
            operationId ``Briefcase_CheckMetadataStart``; путь
            ``POST /core/api/briefcase/CheckMetadataStart`` (тело ``ImportRequestDTO``).
            Связанные: :meth:`briefcase_check_metadata_only_start`,
            :meth:`briefcase_check_metadata_result`, :meth:`briefcase_start_import`.
        """
        if confirm is not True:
            raise ValueError(
                "Запуск проверки метаданных Портфеля стартует фоновую задачу: "
                "передайте confirm=True"
            )
        await self._request(
            "post",
            "/core/api/briefcase/CheckMetadataStart",
            json=request,
        )
