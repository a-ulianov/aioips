"""Метод чтения прав доступа на систему в целом."""

from ...core import APIManager
from ...schemas.security import Security


class SystemSecurityMixin(APIManager):
    """Реализует ``GET /core/api/security/system``.

    operationId ``Security_GetSystemSecurity``.
    """

    async def system_security(self: "SystemSecurityMixin") -> Security:
        """Возвращает права доступа на СИСТЕМУ в целом (общесистемная политика).

        Read-only снимок безопасности верхнего уровня: какие субъекты (пользователи,
        группы, роли) и какие действия (``ActionType``) разрешены/запрещены на уровне
        всей системы IPS — администрирование, общесистемные операции. Это самый общий
        слой прав, поверх которого действуют права на разделы, типы и объекты. Метод
        только читает права, не изменяет их.

        Когда применять: аудит общесистемной политики доступа, проверка кто имеет
        административные полномочия. Для прав на конкретный тип/объект/атрибут используйте
        :meth:`object_type_security` / :meth:`object_security` / :meth:`attribute_security`.

        Returns:
            Снимок прав по схеме :class:`Security`: ``targets`` (субъекты), ``actions``
            (контролируемые действия), ``permissions`` (связки субъект × действие × вид
            доступа), ``durations``, ``conditions``. Пустые списки означают отсутствие
            соответствующих настроек.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                sec = await ips.system_security()
                for perm in sec.permissions:
                    print(perm.target_id, perm.action_id, perm.access_type)

        Notes:
            operationId ``Security_GetSystemSecurity``; путь
            ``GET /core/api/security/system`` (``SecurityDto``).
        """
        data = await self._request("get", "/core/api/security/system")
        return Security.model_validate(data)
