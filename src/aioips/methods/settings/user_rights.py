"""Метод чтения уровня прав на настройки текущего пользователя."""

from typing import Any

from ...core import APIManager
from ...schemas.settings import ToolSecurityRights


class UserRightsMixin(APIManager):
    """Реализует ``POST /core/api/settings/getUserRights`` (``Settings_GetUserRights``)."""

    async def user_rights(self: "UserRightsMixin") -> ToolSecurityRights:
        """Возвращает уровень прав ТЕКУЩЕГО пользователя на изменение настроек.

        Read-only POST: доменного тела нет, но IPS требует тело, поэтому отправляется
        пустой объект ``{}``. Права определяются по сессии (текущий пользователь),
        параметров метод не принимает. Ответ — голая enum-строка; значение единичное,
        не битовая маска.

        Когда применять: для гейтинга операций редактирования настроек — например,
        разрешать правку публичных настроек только при ``EDIT_PUBLIC_SETTINGS`` или
        ``ALL``. Группу инструментов (а не права на настройки) даёт :meth:`user_group`.

        Returns:
            Член :class:`~aioips.schemas.settings.ToolSecurityRights` (``none`` /
            ``editPublicSettings`` / ``editPersonalSettings`` /
            ``overridePersonalSettings`` / ``all``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.settings import ToolSecurityRights

            async with IPSClient(config=config) as ips:
                rights = await ips.user_rights()
                can_edit_public = rights in (
                    ToolSecurityRights.EDIT_PUBLIC_SETTINGS,
                    ToolSecurityRights.ALL,
                )

        Notes:
            operationId ``Settings_GetUserRights``; путь
            ``POST /core/api/settings/getUserRights`` (тело ``{}``).
        """
        payload: dict[str, Any] = {}
        data = await self._request("post", "/core/api/settings/getUserRights", json=payload)
        return ToolSecurityRights(data)
