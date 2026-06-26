"""Метод получения прогресса экспорта Портфеля."""

from typing import Any

from ...core import APIManager
from ...schemas.briefcase import BriefcaseStatus


class BriefcaseExportProgressMixin(APIManager):
    """Реализует ``POST /core/api/briefcase/GetExportProgress``.

    operationId ``Briefcase_GetExportProgress``.
    """

    async def briefcase_export_progress(self: "BriefcaseExportProgressMixin") -> BriefcaseStatus:
        """Возвращает прогресс текущей операции экспорта Портфеля.

        Портфель — это пакет экспорта/импорта объектов IPS («briefcase»); экспорт
        выполняется на сервере асинхронно, а клиент опрашивает его ход. Этот метод
        специализирован на экспорте (в отличие от универсального :meth:`briefcase_status`).

        Read-only POST: доменного тела нет, но IPS требует тело, поэтому отправляется
        пустой объект ``{}``; параметров метод не принимает (операция определяется по
        сессии).

        Когда применять: для индикации хода экспорта. Если экспорт не запущен,
        возвращается «пустой» статус (``percent = 0``, ``status = None``,
        ``is_completed = False``) — это нормально, не ошибка.

        Returns:
            :class:`~aioips.schemas.briefcase.BriefcaseStatus`: снимок прогресса —
            ``percent`` (0–100), ``status`` (описание шага или ``None``), ``is_completed``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                progress = await ips.briefcase_export_progress()
                done = progress.is_completed

        Notes:
            operationId ``Briefcase_GetExportProgress``; путь
            ``POST /core/api/briefcase/GetExportProgress`` (тело ``{}``). Связанные:
            :meth:`briefcase_status`, :meth:`briefcase_cancel_export`.
        """
        payload: dict[str, Any] = {}
        data = await self._request("post", "/core/api/briefcase/GetExportProgress", json=payload)
        return BriefcaseStatus.model_validate(data)
