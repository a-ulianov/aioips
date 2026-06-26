"""Метод чтения прав доступа на коллекцию типов связей."""

from ...core import APIManager
from ...schemas.security import Security


class RelationTypesSecurityMixin(APIManager):
    """Реализует ``GET /core/api/security/relationTypes``.

    operationId ``Security_GetRelationTypeCollectionSecurity``.
    """

    async def relation_types_security(self: "RelationTypesSecurityMixin") -> Security:
        """Возвращает права доступа на КОЛЛЕКЦИЮ типов связей (метаданное в целом).

        Read-only снимок безопасности на набор типов связей между объектами: какие
        субъекты (пользователи, группы, роли) и какие действия (``ActionType``, например
        создание нового типа связи) могут выполнять над коллекцией типов связей как
        метаданным. Это уровень выше отдельного типа связи. Метод только читает права.

        Когда применять: проверить, кто вправе администрировать/создавать типы связей. Для
        прав на ОДИН тип связи используйте :meth:`relation_type_security`.

        Returns:
            Снимок прав по схеме :class:`Security`: ``targets`` (субъекты), ``actions``
            (контролируемые действия), ``permissions`` (связки субъект × действие × вид
            доступа), ``durations``, ``conditions``. Пустые списки означают отсутствие
            соответствующих настроек.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                sec = await ips.relation_types_security()
                for perm in sec.permissions:
                    print(perm.target_id, perm.action_id, perm.access_type)

        Notes:
            operationId ``Security_GetRelationTypeCollectionSecurity``; путь
            ``GET /core/api/security/relationTypes`` (``SecurityDto``).
        """
        data = await self._request("get", "/core/api/security/relationTypes")
        return Security.model_validate(data)
