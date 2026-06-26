"""Метод чтения прав доступа на тип связи."""

from ...core import APIManager
from ...schemas.security import Security


class RelationTypeSecurityMixin(APIManager):
    """Реализует ``GET /core/api/security/relationTypes/{relationTypeId}``.

    operationId ``Security_GetRelationTypeSecurity``.
    """

    async def relation_type_security(
        self: "RelationTypeSecurityMixin", relation_type_id: int
    ) -> Security:
        """Возвращает права доступа на ТИП связи (кто что может с данным типом связи).

        Read-only снимок безопасности конкретного типа связи между объектами: какие
        субъекты (пользователи, группы, роли) и какие действия (``ActionType``: создание/
        удаление связей данного типа) разрешены/запрещены. Управляет тем, кто вправе
        связывать объекты этим типом связи. Метод только читает права, не изменяет их.

        Когда применять: аудит доступа к конкретному типу связи. Для прав на ВСЕ типы
        связей сразу используйте :meth:`relation_types_security`.

        Args:
            relation_type_id: Идентификатор ТИПА связи (метаданное «тип связи»), а не
                идентификатор конкретной связи (``RelationID``, нестабилен — см.
                [[ips-object-model]]).

        Returns:
            Снимок прав по схеме :class:`Security`: ``targets`` (субъекты), ``actions``
            (контролируемые действия), ``permissions`` (связки субъект × действие × вид
            доступа), ``durations``, ``conditions``. Пустые списки означают отсутствие
            соответствующих настроек.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если тип связи не найден).

        Example:
            async with IPSClient(config=config) as ips:
                sec = await ips.relation_type_security(7)  # 7 = id типа связи
                for perm in sec.permissions:
                    print(perm.target_id, perm.action_id, perm.access_type)

        Notes:
            operationId ``Security_GetRelationTypeSecurity``; путь
            ``GET /core/api/security/relationTypes/{relationTypeId}`` (``SecurityDto``).
        """
        data = await self._request("get", f"/core/api/security/relationTypes/{relation_type_id}")
        return Security.model_validate(data)
