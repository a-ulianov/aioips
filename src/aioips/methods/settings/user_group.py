"""Метод чтения группы инструментов текущего пользователя."""

from typing import Any

from ...core import APIManager
from ...schemas.settings import ToolSecurityGroup


class UserGroupMixin(APIManager):
    """Реализует ``POST /core/api/settings/getUserGroup`` (``Settings_GetUserGroup``)."""

    async def user_group(self: "UserGroupMixin") -> ToolSecurityGroup:
        """Возвращает группу безопасности инструментов ТЕКУЩЕГО пользователя.

        Read-only POST: доменного тела нет, но IPS требует тело, поэтому отправляется
        пустой объект ``{}``. Группа определяется по сессии (текущий пользователь),
        параметров метод не принимает. Ответ — голая enum-строка.

        Когда применять: чтобы быстро узнать привилегированность текущего пользователя
        (администратор / обычный / ограниченный) и решить, показывать ли операции
        редактирования настроек. Тонкое разрешение на изменение настроек даёт
        :meth:`user_rights`. Группы по всем пользователям — :meth:`security_data`.

        Returns:
            Член :class:`~aioips.schemas.settings.ToolSecurityGroup`
            (``administrator`` / ``normalUser`` / ``restrictedUser``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.settings import ToolSecurityGroup

            async with IPSClient(config=config) as ips:
                group = await ips.user_group()
                is_admin = group is ToolSecurityGroup.ADMINISTRATOR

        Notes:
            operationId ``Settings_GetUserGroup``; путь
            ``POST /core/api/settings/getUserGroup`` (тело ``{}``).
        """
        payload: dict[str, Any] = {}
        data = await self._request("post", "/core/api/settings/getUserGroup", json=payload)
        return ToolSecurityGroup(data)
