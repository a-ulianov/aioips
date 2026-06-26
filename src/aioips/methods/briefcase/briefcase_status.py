"""Метод получения статуса текущей задачи Портфеля."""

from typing import Any

from ...core import APIManager
from ...schemas.briefcase import BriefcaseStatus


class BriefcaseStatusMixin(APIManager):
    """Реализует ``POST /core/api/briefcase/GetStatus`` (``Briefcase_GetStatus``)."""

    async def briefcase_status(self: "BriefcaseStatusMixin") -> BriefcaseStatus:
        """Возвращает статус текущей фоновой задачи Портфеля (экспорта/импорта).

        Портфель — это пакет экспорта/импорта объектов IPS («briefcase»); его операции
        выполняются на сервере асинхронно, а клиент опрашивает их прогресс. Этот метод —
        универсальный опрос состояния (процент, текущий шаг, признак завершения).

        Read-only POST: доменного тела нет, но IPS требует тело, поэтому отправляется
        пустой объект ``{}``; параметров метод не принимает (задача определяется по
        сессии). Для прогресса именно экспорта см. :meth:`briefcase_export_progress`.

        Когда применять: для индикации хода длительной операции Портфеля. Если ничего не
        запущено, возвращается «пустой» статус (``percent = 0``, ``status = None``,
        ``is_completed = False``) — это нормально, не ошибка.

        Returns:
            :class:`~aioips.schemas.briefcase.BriefcaseStatus`: снимок прогресса —
            ``percent`` (0–100), ``status`` (описание шага или ``None``), ``is_completed``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                state = await ips.briefcase_status()
                if not state.is_completed:
                    print(f"{state.percent}% — {state.status}")

        Notes:
            operationId ``Briefcase_GetStatus``; путь
            ``POST /core/api/briefcase/GetStatus`` (тело ``{}``). Связанные:
            :meth:`briefcase_export_progress`, :meth:`briefcase_cancel_export`.
        """
        payload: dict[str, Any] = {}
        data = await self._request("post", "/core/api/briefcase/GetStatus", json=payload)
        return BriefcaseStatus.model_validate(data)
