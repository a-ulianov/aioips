"""Метод чтения данных безопасности пользователей."""

from typing import Any

from ...core import APIManager
from ...schemas.settings import UserSecurityData


class SecurityDataMixin(APIManager):
    """Реализует ``POST /core/api/settings/getSecurityData`` (``Settings_GetSecurityData``)."""

    async def security_data(self: "SecurityDataMixin") -> list[UserSecurityData]:
        """Возвращает данные безопасности пользователей: связки ``userId`` ↔ группа.

        Read-only POST: тело запроса не требуется доменно, но IPS отвергает запрос без
        тела, поэтому отправляется пустой объект ``{}``. Метод перечисляет всех
        пользователей, для которых заданы данные безопасности инструментов, и их группу
        :class:`~aioips.schemas.settings.ToolSecurityGroup`.

        Когда применять: чтобы получить общую картину распределения пользователей по
        группам инструментов либо найти группу конкретного пользователя по его id.
        Для группы/прав именно ТЕКУЩЕГО пользователя используйте :meth:`user_group`
        и :meth:`user_rights`.

        Id-пространство: ``user_id`` — идентификатор пользователя IPS (не объекта и
        не версии).

        Returns:
            Список записей :class:`~aioips.schemas.settings.UserSecurityData` (голый
            JSON-массив в ответе). Пустой список — данные безопасности не заданы ни
            для одного пользователя.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                records = await ips.security_data()
                by_user = {r.user_id: r.security_group for r in records}

        Notes:
            operationId ``Settings_GetSecurityData``; путь
            ``POST /core/api/settings/getSecurityData`` (тело ``{}``).
        """
        payload: dict[str, Any] = {}
        data = await self._request("post", "/core/api/settings/getSecurityData", json=payload)
        items = data if isinstance(data, list) else []
        return [UserSecurityData.model_validate(item) for item in items]
