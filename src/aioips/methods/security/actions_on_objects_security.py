"""Метод чтения прав доступа на действия над объектами."""

from ...core import APIManager
from ...schemas.security import Security


class ActionsOnObjectsSecurityMixin(APIManager):
    """Реализует ``GET /core/api/security/actionOnObjects``.

    operationId ``Security_GetActionsOnObjectsSecurity``.
    """

    async def actions_on_objects_security(
        self: "ActionsOnObjectsSecurityMixin",
    ) -> Security:
        """Возвращает глобальные права на ДЕЙСТВИЯ над объектами (системный уровень).

        Read-only снимок безопасности для общесистемных действий над объектами: кто
        (пользователи, группы, роли) и какие действия (``ActionType``) вправе выполнять
        над объектами безотносительно конкретного типа или экземпляра. Это глобальный
        слой прав, дополняющий права на тип и на экземпляр. Метод только читает права.

        Когда применять: аудит общесистемной политики действий над объектами, понимание
        прав «по умолчанию» поверх типовых и объектных. Для прав на конкретный тип/объект
        используйте :meth:`object_type_security` / :meth:`object_security`.

        Returns:
            Снимок прав по схеме :class:`Security` (``targets`` / ``actions`` /
            ``permissions`` / ``durations`` / ``conditions``). Пустые списки означают
            отсутствие соответствующих настроек.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                sec = await ips.actions_on_objects_security()
                for action in sec.actions:
                    print(action.action_id, action.action_category_id)

        Notes:
            operationId ``Security_GetActionsOnObjectsSecurity``; путь
            ``GET /core/api/security/actionOnObjects`` (``SecurityDto``).
        """
        data = await self._request("get", "/core/api/security/actionOnObjects")
        return Security.model_validate(data)
