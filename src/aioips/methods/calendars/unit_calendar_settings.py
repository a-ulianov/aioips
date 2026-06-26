"""Метод загрузки календаря подразделения по его идентификатору."""

from ...core import APIManager
from ...schemas.calendars import Calendar


class UnitCalendarSettingsMixin(APIManager):
    """Реализует ``GET /core/api/calendars/unitCalendarSettings/{unitId}``.

    operationId ``Calendars_LoadUnitCalendarSettings``.
    """

    async def unit_calendar_settings(self: "UnitCalendarSettingsMixin", unit_id: int) -> Calendar:
        """Возвращает настройки календаря организационного подразделения (unit).

        Загружает производственный календарь, привязанный к организационному
        подразделению (``owner = organizationUnit``), со всеми настройками.
        Применяйте, когда планирование ведётся по календарю конкретного
        подразделения и его идентификатор уже известен.

        Предусловие по id-пространству: аргумент — это идентификатор ПОДРАЗДЕЛЕНИЯ
        (``unitId``), а не идентификатор пользователя или календаря. Если известен
        пользователь, а не подразделение, используйте :meth:`unit_calendar_for_user`
        (сервер сам найдёт подразделение). Для личного календаря пользователя —
        :meth:`user_calendar_settings`; для произвольного календаря по его id —
        :meth:`calendar_settings`.

        Args:
            unit_id: Идентификатор организационного подразделения (``unitId``).

        Returns:
            Календарь подразделения по схеме :class:`Calendar`.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если календаря нет).

        Example:
            async with IPSClient(config=config) as ips:
                cal = await ips.unit_calendar_settings(11)
                print(cal.calendar_id, cal.owner, cal.unit_id)

        Notes:
            operationId ``Calendars_LoadUnitCalendarSettings``; путь
            ``GET /core/api/calendars/unitCalendarSettings/{unitId}`` (``CalendarContract``).
            Связан с :meth:`calendars` (выбор календаря) и :meth:`calendar_settings`.
        """
        data = await self._request("get", f"/core/api/calendars/unitCalendarSettings/{unit_id}")
        return Calendar.model_validate(data)
