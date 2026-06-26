"""Метод назначения базового календаря объекту (config-мутация, confirm-гейт)."""

from ...core import APIManager


class SetBaseCalendarMixin(APIManager):
    """Реализует ``POST /core/api/calendars/setBaseCalendar/{objectId}/{baseCalendarId}``.

    operationId ``Calendars_SetBaseCalendar``.
    """

    async def set_base_calendar(
        self: "SetBaseCalendarMixin",
        object_id: int,
        base_calendar_id: int,
        *,
        confirm: bool = False,
    ) -> None:
        """Назначает объекту базовый производственный календарь (МУТИРУЮЩАЯ, ``confirm``).

        Привязывает к объекту (например, проекту/задаче) указанный базовый календарь, от
        которого считается рабочее время при планировании. Мутация привязки — защищена
        ``confirm``: без ``confirm=True`` поднимается :class:`ValueError` до обращения к
        серверу. Оба идентификатора передаются в пути, тело не используется.

        Обратимость: чтобы вернуть прежнюю привязку, повторно вызовите метод с исходным
        ``base_calendar_id`` (сохраните его заранее). Для одноразового тест-объекта
        привязка снимается удалением самого объекта.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectId`` / ObjectID), которому
                назначается базовый календарь.
            base_calendar_id: Идентификатор базового календаря (``baseCalendarId``);
                список доступных календарей — :meth:`calendars`.
            confirm: Подтверждение мутирующей операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.set_base_calendar(102550, 1, confirm=True)

        Notes:
            operationId ``Calendars_SetBaseCalendar``; путь
            ``POST /core/api/calendars/setBaseCalendar/{objectId}/{baseCalendarId}`` (без
            тела; пустой ``json={}`` задаёт Content-Type во избежание 415). Список
            календарей — :meth:`calendars`.
        """
        if confirm is not True:
            raise ValueError(
                "set_base_calendar меняет привязку календаря объекта; передайте confirm=True"
            )
        path = f"/core/api/calendars/setBaseCalendar/{object_id}/{base_calendar_id}"
        await self._request("post", path, json={})
        return None
