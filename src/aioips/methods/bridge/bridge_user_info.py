"""Метод чтения сведений о пользователе IPS Bridge."""

from ...core import APIManager
from ...schemas.bridge import BridgeUser


class BridgeUserInfoMixin(APIManager):
    """Реализует ``GET /core/api/Bridge/UserInfo`` (``Bridge_GetUserInfo``)."""

    async def bridge_user_info(self: "BridgeUserInfoMixin") -> BridgeUser:
        """Возвращает сведения о текущем пользователе IPS Bridge.

        Отдаёт пользователя, от имени которого работает клиентский мост: его
        идентификатор, отображаемое имя, логин и идентификатор базы данных.
        Применяйте, чтобы определить активного пользователя моста (например, для
        подстановки в действия запуска, аудита или диагностики). Предусловий нет.

        Returns:
            Пользователь по схеме :class:`BridgeUser`. Обязательно заполнено поле
            ``id``; имя, логин и ``database_id`` могут быть ``None``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                user = await ips.bridge_user_info()
                print(user.id, user.login_name)

        Notes:
            ``operationId``: ``Bridge_GetUserInfo``; путь
            ``GET /core/api/Bridge/UserInfo``.
        """
        data = await self._request("get", "/core/api/Bridge/UserInfo")
        return BridgeUser.model_validate(data)
