"""Метод чтения прав доступа на коллекцию типов объектов."""

from ...core import APIManager
from ...schemas.security import Security


class ObjectTypesSecurityMixin(APIManager):
    """Реализует ``GET /core/api/security/objectTypes``.

    operationId ``Security_GetObjectTypeCollectionSecurity``.
    """

    async def object_types_security(self: "ObjectTypesSecurityMixin") -> Security:
        """Возвращает права доступа на КОЛЛЕКЦИЮ типов объектов (метаданное в целом).

        Read-only снимок безопасности на саму коллекцию типов объектов: кто и какие
        действия (``ActionType``, например создание нового ТИПА объекта) может выполнять
        над набором типов как метаданным. Это уровень выше отдельного типа. Метод только
        читает права.

        Когда применять: проверить, кто вправе администрировать/создавать типы объектов.
        Для прав на ОДИН тип используйте :meth:`object_type_security`, для прав на
        экземпляр — :meth:`object_security`.

        Returns:
            Снимок прав по схеме :class:`Security` (``targets`` / ``actions`` /
            ``permissions`` / ``durations`` / ``conditions``). Пустые списки означают
            отсутствие соответствующих настроек.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                sec = await ips.object_types_security()
                allowed = {p.target_id for p in sec.permissions if p.access_type == "grant"}
                print(allowed)

        Notes:
            operationId ``Security_GetObjectTypeCollectionSecurity``; путь
            ``GET /core/api/security/objectTypes`` (``SecurityDto``).
        """
        data = await self._request("get", "/core/api/security/objectTypes")
        return Security.model_validate(data)
