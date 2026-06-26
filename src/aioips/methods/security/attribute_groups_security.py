"""Метод чтения прав доступа на коллекцию групп атрибутов."""

from ...core import APIManager
from ...schemas.security import Security


class AttributeGroupsSecurityMixin(APIManager):
    """Реализует ``GET /core/api/security/attributeGroups``.

    operationId ``Security_GetAttributeGroupCollectionSecurity``.
    """

    async def attribute_groups_security(self: "AttributeGroupsSecurityMixin") -> Security:
        """Возвращает права доступа на КОЛЛЕКЦИЮ групп атрибутов (метаданное в целом).

        Read-only снимок безопасности на набор групп атрибутов: какие субъекты
        (пользователи, группы, роли) и какие действия (``ActionType``, например создание
        новой группы атрибутов) могут выполнять над коллекцией групп атрибутов как
        метаданным. Это уровень выше отдельной группы. Метод только читает права.

        Когда применять: проверить, кто вправе администрировать/создавать группы
        атрибутов. Для прав на ОДНУ группу используйте :meth:`attribute_group_security`,
        для коллекции атрибутов — :meth:`attributes_collection_security`.

        Returns:
            Снимок прав по схеме :class:`Security`: ``targets`` (субъекты), ``actions``
            (контролируемые действия), ``permissions`` (связки субъект × действие × вид
            доступа), ``durations``, ``conditions``. Пустые списки означают отсутствие
            соответствующих настроек.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                sec = await ips.attribute_groups_security()
                for perm in sec.permissions:
                    print(perm.target_id, perm.action_id, perm.access_type)

        Notes:
            operationId ``Security_GetAttributeGroupCollectionSecurity``; путь
            ``GET /core/api/security/attributeGroups`` (``SecurityDto``).
        """
        data = await self._request("get", "/core/api/security/attributeGroups")
        return Security.model_validate(data)
