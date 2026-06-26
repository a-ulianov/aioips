"""Метод записи данных безопасности пользователя IPS (мутация)."""

from typing import Any

from ...core import APIManager


class AddOrUpdateSecurityDataMixin(APIManager):
    """Реализует ``POST /core/api/settings/addOrUpdateSecurityData``.

    operationId ``Settings_AddOrUpdateSecurityData``.
    """

    async def add_or_update_security_data(
        self: "AddOrUpdateSecurityDataMixin",
        data: dict[str, Any],
        *,
        confirm: bool = False,
    ) -> None:
        """Создаёт или обновляет данные безопасности пользователя (МУТАЦИЯ).

        Записывает связку ``userId`` ↔ группа безопасности инструментов
        (``UserSecurityData``): если запись для пользователя уже есть — она
        перезаписывается, иначе создаётся. Управляет тем, к какой группе безопасности
        инструментов отнесён пользователь. Это операция ЗАПИСИ, изменяющая серверное
        состояние прав.

        Когда применять: при назначении или изменении группы безопасности инструментов
        пользователю. Прочитать текущее распределение можно методом :meth:`security_data`,
        удалить запись пользователя — :meth:`remove_security_data`.

        Id-пространство: поле ``userId`` тела — идентификатор пользователя IPS (не объекта
        и не версии).

        Обратимость: операция ОБРАТИМА по схеме write-same-back — прочитайте текущую
        запись через :meth:`security_data`, сохраните её и для отката запишите обратно
        этим методом (либо удалите через :meth:`remove_security_data`, если записи не
        было). Затрагивает права доступа — выполняйте осознанно.

        Защита: меняет данные безопасности на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к серверу.

        Args:
            data: Тело — словарь ``UserSecurityData`` (ключи ``camelCase``: ``userId`` и
                группа безопасности, как их отдаёт :meth:`security_data`). Передаётся
                телом запроса (``json=data``) без преобразований.
            confirm: Подтверждение операции записи. Без ``True`` запрос НЕ выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                record = {"userId": 4210, "securityGroup": {"id": 3, "name": "Operators"}}
                await ips.add_or_update_security_data(record, confirm=True)

        Notes:
            operationId ``Settings_AddOrUpdateSecurityData``; путь
            ``POST /core/api/settings/addOrUpdateSecurityData``. Тело — ``UserSecurityData``
            (``json=data``); query не требуется. Ответ — void (None).
        """
        if confirm is not True:
            raise ValueError(
                "add_or_update_security_data меняет данные безопасности пользователя; "
                "передайте confirm=True",
            )
        await self._request("post", "/core/api/settings/addOrUpdateSecurityData", json=data)
        return None
