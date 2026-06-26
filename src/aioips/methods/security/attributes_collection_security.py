"""Метод чтения прав доступа на коллекцию атрибутов."""

from ...core import APIManager
from ...schemas.security import Security


class AttributesCollectionSecurityMixin(APIManager):
    """Реализует ``GET /core/api/security/attributes``.

    operationId ``Security_GetAttributeCollectionSecurity``.
    """

    async def attributes_collection_security(
        self: "AttributesCollectionSecurityMixin",
    ) -> Security:
        """Возвращает права доступа на КОЛЛЕКЦИЮ атрибутов (метаданное в целом).

        Read-only снимок безопасности на набор атрибутов (типов атрибутов): какие субъекты
        (пользователи, группы, роли) и какие действия (``ActionType``, например создание
        нового атрибута) могут выполнять над коллекцией атрибутов как метаданным. Это
        уровень выше отдельного атрибута. Метод только читает права, не изменяет их.

        Когда применять: проверить, кто вправе администрировать/создавать атрибуты. Для
        прав на ОДИН атрибут используйте :meth:`attribute_security`, для групп атрибутов —
        :meth:`attribute_groups_security`.

        Returns:
            Снимок прав по схеме :class:`Security`: ``targets`` (субъекты), ``actions``
            (контролируемые действия), ``permissions`` (связки субъект × действие × вид
            доступа), ``durations``, ``conditions``. Пустые списки означают отсутствие
            соответствующих настроек.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                sec = await ips.attributes_collection_security()
                for perm in sec.permissions:
                    print(perm.target_id, perm.action_id, perm.access_type)

        Notes:
            operationId ``Security_GetAttributeCollectionSecurity``; путь
            ``GET /core/api/security/attributes`` (``SecurityDto``).
        """
        data = await self._request("get", "/core/api/security/attributes")
        return Security.model_validate(data)
