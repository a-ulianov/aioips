"""Метод чтения прав доступа на коллекцию уровней ЖЦ."""

from ...core import APIManager
from ...schemas.security import Security


class LifecycleLevelsSecurityMixin(APIManager):
    """Реализует ``GET /core/api/security/lifecycleLevels``.

    operationId ``Security_GetLifecycleLevelCollectionSecurity``.
    """

    async def lifecycle_levels_security(self: "LifecycleLevelsSecurityMixin") -> Security:
        """Возвращает права доступа на КОЛЛЕКЦИЮ уровней ЖЦ (метаданное в целом).

        Read-only снимок безопасности на набор уровней жизненного цикла: какие субъекты
        (пользователи, группы, роли) и какие действия (``ActionType``, например создание
        нового уровня ЖЦ) могут выполнять над коллекцией уровней ЖЦ как метаданным. Это
        уровень выше отдельного уровня ЖЦ. Метод только читает права, не изменяет их.

        Когда применять: проверить, кто вправе администрировать/создавать уровни
        жизненного цикла. Для прав на ОДИН уровень используйте
        :meth:`lifecycle_level_security`, для схем ЖЦ — :meth:`lifecycle_schemes_security`.

        Returns:
            Снимок прав по схеме :class:`Security`: ``targets`` (субъекты), ``actions``
            (контролируемые действия), ``permissions`` (связки субъект × действие × вид
            доступа), ``durations``, ``conditions``. Пустые списки означают отсутствие
            соответствующих настроек.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                sec = await ips.lifecycle_levels_security()
                for perm in sec.permissions:
                    print(perm.target_id, perm.action_id, perm.access_type)

        Notes:
            operationId ``Security_GetLifecycleLevelCollectionSecurity``; путь
            ``GET /core/api/security/lifecycleLevels`` (``SecurityDto``).
        """
        data = await self._request("get", "/core/api/security/lifecycleLevels")
        return Security.model_validate(data)
