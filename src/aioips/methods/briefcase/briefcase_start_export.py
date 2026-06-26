"""Метод запуска экспорта объектов в Портфель."""

from typing import Any

from ...core import APIManager


class BriefcaseStartExportMixin(APIManager):
    """Реализует ``POST /core/api/briefcase/StartExport`` (``Briefcase_StartExport``)."""

    async def briefcase_start_export(
        self: "BriefcaseStartExportMixin",
        request: dict[str, Any],
        *,
        confirm: bool = False,
    ) -> None:
        """Запускает экспорт объектов в Портфель (СОЗДАЁТ артефакт, ``confirm``).

        Портфель — это пакет экспорта/импорта объектов IPS. Метод стартует серверную
        фоновую задачу экспорта объектов в файл портфеля. Операция СОЗДАЁТ артефакт на
        сервере (файл портфеля) и потребляет ресурсы, поэтому защищена ``confirm``: без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО запроса. Прогресс
        отслеживают через :meth:`briefcase_export_progress`, общий статус —
        :meth:`briefcase_status`; отмена — :meth:`briefcase_cancel_export`. Экспорт не
        изменяет существующие объекты базы (в отличие от импорта).

        Тело ``request`` (``BriefcaseExportRequest``) описывает состав и режим экспорта:
        ``id``/``path`` (что и куда), ``newOwnerId``, ``onlySystem``, ``withSequrity``,
        ``withLocalization``, ``exportCategories``, ``comment``, ``expandedLog``,
        ``fullDatabaseMode``.

        Args:
            request: Тело запроса ``BriefcaseExportRequest`` в виде словаря;
                отправляется как JSON-тело.
            confirm: Подтверждение создания артефакта. Без ``True`` метод не делает
                запрос и поднимает :class:`ValueError` (защитный гейт).

        Returns:
            ``None``. Метод лишь запускает экспорт; прогресс/исход читаются отдельно
            (:meth:`briefcase_export_progress`, :meth:`briefcase_status`).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.briefcase_start_export(
                    {"path": "X:/export/parts.brief", "comment": "узлы серии 550"},
                    confirm=True,
                )
                progress = await ips.briefcase_export_progress()

        Notes:
            operationId ``Briefcase_StartExport``; путь
            ``POST /core/api/briefcase/StartExport`` (тело ``BriefcaseExportRequest``).
            Связанные: :meth:`briefcase_export_progress`,
            :meth:`briefcase_cancel_export`, :meth:`briefcase_status`.
        """
        if confirm is not True:
            raise ValueError(
                "Запуск экспорта Портфеля создаёт артефакт на сервере: передайте confirm=True"
            )
        await self._request(
            "post",
            "/core/api/briefcase/StartExport",
            json=request,
        )
