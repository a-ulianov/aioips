"""Метод чтения прав доступа на коллекцию схем ЖЦ."""

from ...core import APIManager
from ...schemas.security import Security


class LifecycleSchemesSecurityMixin(APIManager):
    """Реализует ``GET /core/api/security/lifecycleSchemes``.

    operationId ``Security_GetLifecycleSchemeCollectionSecurity``.
    """

    async def lifecycle_schemes_security(self: "LifecycleSchemesSecurityMixin") -> Security:
        """Возвращает права доступа на КОЛЛЕКЦИЮ схем ЖЦ (метаданное в целом).

        Read-only снимок безопасности на набор схем жизненного цикла: какие субъекты
        (пользователи, группы, роли) и какие действия (``ActionType``, например создание
        новой схемы ЖЦ) могут выполнять над коллекцией схем ЖЦ как метаданным. Это уровень
        выше отдельной схемы. Метод только читает права, не изменяет их.

        Когда применять: проверить, кто вправе администрировать/создавать схемы
        жизненного цикла. Для прав на ОДНУ схему используйте
        :meth:`lifecycle_scheme_security`, для уровней ЖЦ —
        :meth:`lifecycle_levels_security`.

        Returns:
            Снимок прав по схеме :class:`Security`: ``targets`` (субъекты), ``actions``
            (контролируемые действия), ``permissions`` (связки субъект × действие × вид
            доступа), ``durations``, ``conditions``. Пустые списки означают отсутствие
            соответствующих настроек.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                sec = await ips.lifecycle_schemes_security()
                for perm in sec.permissions:
                    print(perm.target_id, perm.action_id, perm.access_type)

        Notes:
            operationId ``Security_GetLifecycleSchemeCollectionSecurity``; путь
            ``GET /core/api/security/lifecycleSchemes`` (``SecurityDto``).
        """
        data = await self._request("get", "/core/api/security/lifecycleSchemes")
        return Security.model_validate(data)
