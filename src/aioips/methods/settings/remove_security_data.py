"""Метод удаления данных безопасности пользователя IPS (мутация)."""

from typing import Any

from ...core import APIManager


class RemoveSecurityDataMixin(APIManager):
    """Реализует ``POST /core/api/settings/removeSecurityData``.

    operationId ``Settings_RemoveSecurityData``.
    """

    async def remove_security_data(
        self: "RemoveSecurityDataMixin",
        *,
        user_id: int | None = None,
        confirm: bool = False,
    ) -> None:
        """Удаляет данные безопасности пользователя (РАЗРУШАЮЩАЯ операция).

        Удаляет запись «данные безопасности инструментов» для указанного пользователя
        (``UserSecurityData``): связка ``userId`` ↔ группа безопасности перестаёт
        существовать. После удаления пользователь больше не отнесён к группе инструментов.
        Это операция ЗАПИСИ, изменяющая серверное состояние прав.

        Когда применять: при снятии пользователя с группы безопасности инструментов.
        Прочитать текущие записи можно методом :meth:`security_data`, создать/обновить —
        :meth:`add_or_update_security_data`.

        Id-пространство: ``user_id`` — идентификатор пользователя IPS (не объекта и не
        версии).

        Обратимость: операция НЕОБРАТИМА — прежняя группа сервером не возвращается; для
        восстановления потребуется заново задать запись через
        :meth:`add_or_update_security_data` (сохраните её заранее через
        :meth:`security_data`). Защищена параметром ``confirm``.

        Args:
            user_id: Идентификатор пользователя IPS (query-параметр ``userId``), чьи
                данные безопасности удаляются. ``None`` — параметр не передаётся.
            confirm: Подтверждение необратимой операции. Без ``True`` запрос НЕ
                выполняется и поднимается :class:`ValueError` ещё до обращения к серверу.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.remove_security_data(user_id=4210, confirm=True)

        Notes:
            operationId ``Settings_RemoveSecurityData``; путь
            ``POST /core/api/settings/removeSecurityData``. Query — ``userId`` (int64);
            тело не требуется (``json={}``). Ответ — void (None).
        """
        if confirm is not True:
            raise ValueError(
                "remove_security_data удаляет данные безопасности пользователя (необратимо); "
                "передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        await self._request("post", "/core/api/settings/removeSecurityData", params=params, json={})
        return None
