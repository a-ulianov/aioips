"""Метод чтения прав доступа на группу атрибутов."""

from ...core import APIManager
from ...schemas.security import Security


class AttributeGroupSecurityMixin(APIManager):
    """Реализует ``GET /core/api/security/attributeGroups/{attributeGroupId}``.

    operationId ``Security_GetAttributeGroupSecurity``.
    """

    async def attribute_group_security(
        self: "AttributeGroupSecurityMixin", attribute_group_id: int
    ) -> Security:
        """Возвращает права доступа на ГРУППУ атрибутов (кто что может с группой).

        Read-only снимок безопасности конкретной группы атрибутов: какие субъекты
        (пользователи, группы, роли) и какие действия (``ActionType``) разрешены/запрещены
        для данной группы атрибутов. Позволяет защитить от чтения/изменения целую
        смысловую группу атрибутов разом. Метод только читает права, не изменяет их.

        Когда применять: аудит доступа к конкретной группе атрибутов. Для прав на ВСЕ
        группы сразу используйте :meth:`attribute_groups_security`, для одного атрибута —
        :meth:`attribute_security`.

        Args:
            attribute_group_id: Идентификатор ГРУППЫ атрибутов (метаданное «группа
                атрибутов»), а не идентификатор атрибута или его значения.

        Returns:
            Снимок прав по схеме :class:`Security`: ``targets`` (субъекты), ``actions``
            (контролируемые действия), ``permissions`` (связки субъект × действие × вид
            доступа), ``durations``, ``conditions``. Пустые списки означают отсутствие
            соответствующих настроек.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если группа не найдена).

        Example:
            async with IPSClient(config=config) as ips:
                sec = await ips.attribute_group_security(42)  # 42 = id группы атрибутов
                for perm in sec.permissions:
                    print(perm.target_id, perm.action_id, perm.access_type)

        Notes:
            operationId ``Security_GetAttributeGroupSecurity``; путь
            ``GET /core/api/security/attributeGroups/{attributeGroupId}`` (``SecurityDto``).
        """
        data = await self._request(
            "get", f"/core/api/security/attributeGroups/{attribute_group_id}"
        )
        return Security.model_validate(data)
