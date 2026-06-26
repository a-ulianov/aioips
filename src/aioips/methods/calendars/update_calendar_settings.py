"""Метод записи настроек календаря (config-мутация, confirm-гейт)."""

from typing import Any

from ...core import APIManager
from ...schemas.calendars import Calendar


class UpdateCalendarSettingsMixin(APIManager):
    """Реализует ``POST /core/api/calendars/calendarSettings``.

    operationId ``Calendars_UpdateCalendarSettings``.
    """

    async def update_calendar_settings(
        self: "UpdateCalendarSettingsMixin",
        calendar: Calendar | dict[str, Any],
        *,
        confirm: bool = False,
    ) -> None:
        """Записывает настройки производственного календаря (МУТИРУЮЩАЯ, ``confirm``).

        Сохраняет полное определение календаря (рабочие/выходные дни, часы, исключения)
        по его ``calendar_id`` внутри тела. Это ГЛОБАЛЬНАЯ настройка, влияющая на
        планирование (improjects/Gantt), поэтому операция защищена ``confirm``: без
        ``confirm=True`` поднимается :class:`ValueError` ещё до обращения к серверу.

        Обратимость: операция обратима «вручную» — прочитайте текущее определение через
        :meth:`calendar_settings` и сохраните его, затем при необходимости запишите его
        обратно этим методом. Идентификатор календаря передаётся ВНУТРИ тела
        (``calendar_id``), отдельного path-параметра нет.

        Args:
            calendar: Определение календаря (:class:`Calendar`) или эквивалентный словарь
                (``CalendarContract``). Для точного round-trip без потери полей передавайте
                «сырой» словарь, полученный из ответа :meth:`calendar_settings`.
            confirm: Подтверждение мутирующей операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                cur = await ips.calendar_settings(1)            # бэкап
                await ips.update_calendar_settings(cur, confirm=True)  # запись обратно

        Notes:
            operationId ``Calendars_UpdateCalendarSettings``; путь
            ``POST /core/api/calendars/calendarSettings``; тело — ``CalendarContract``
            (``calendar_id`` внутри тела). Парный read — :meth:`calendar_settings`.
            Пользовательский календарь — :meth:`update_user_calendar_settings`.
        """
        if confirm is not True:
            raise ValueError(
                "update_calendar_settings мутирует глобальный календарь; передайте confirm=True"
            )
        if isinstance(calendar, Calendar):
            payload: Any = calendar.model_dump(mode="json", by_alias=True, exclude_none=True)
        else:
            payload = calendar
        await self._request("post", "/core/api/calendars/calendarSettings", json=payload)
        return None
