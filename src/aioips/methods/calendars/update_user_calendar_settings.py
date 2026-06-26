"""Метод записи настроек пользовательского календаря (config-мутация, confirm-гейт)."""

from typing import Any

from ...core import APIManager
from ...schemas.calendars import Calendar


class UpdateUserCalendarSettingsMixin(APIManager):
    """Реализует ``POST /core/api/calendars/userCalendarSettings``.

    operationId ``Calendars_UpdateUserCalendarSettings``.
    """

    async def update_user_calendar_settings(
        self: "UpdateUserCalendarSettingsMixin",
        calendar: Calendar | dict[str, Any],
        *,
        confirm: bool = False,
    ) -> None:
        """Записывает настройки ПОЛЬЗОВАТЕЛЬСКОГО календаря (МУТИРУЮЩАЯ, ``confirm``).

        Сохраняет персональное определение календаря пользователя (его рабочее время,
        исключения) поверх базового. Личный масштаб (затрагивает планирование задач
        пользователя), но всё же мутация — поэтому защищено ``confirm``: без ``confirm=True``
        поднимается :class:`ValueError` до обращения к серверу.

        Обратимость: прочитайте текущее определение через :meth:`user_calendar_settings`,
        сохраните, при необходимости запишите обратно. Идентификатор пользователя/календаря
        передаётся ВНУТРИ тела (``CalendarContract``), отдельного path-параметра нет.

        Args:
            calendar: Определение календаря (:class:`Calendar`) или эквивалентный словарь.
                Для точного round-trip передавайте «сырой» словарь из ответа
                :meth:`user_calendar_settings`.
            confirm: Подтверждение мутирующей операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                cur = await ips.user_calendar_settings(42)            # бэкап
                await ips.update_user_calendar_settings(cur, confirm=True)

        Notes:
            operationId ``Calendars_UpdateUserCalendarSettings``; путь
            ``POST /core/api/calendars/userCalendarSettings``; тело — ``CalendarContract``.
            Парный read — :meth:`user_calendar_settings`. Глобальный календарь —
            :meth:`update_calendar_settings`.
        """
        if confirm is not True:
            raise ValueError(
                "update_user_calendar_settings мутирует календарь; передайте confirm=True"
            )
        if isinstance(calendar, Calendar):
            payload: Any = calendar.model_dump(mode="json", by_alias=True, exclude_none=True)
        else:
            payload = calendar
        await self._request("post", "/core/api/calendars/userCalendarSettings", json=payload)
        return None
