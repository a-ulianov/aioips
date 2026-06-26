"""Метод чтения прав доступа на тип объекта."""

from ...core import APIManager
from ...schemas.security import Security


class ObjectTypeSecurityMixin(APIManager):
    """Реализует ``GET /core/api/security/objectTypes/{objectTypeId}``.

    operationId ``Security_GetObjectTypeSecurity``.
    """

    async def object_type_security(
        self: "ObjectTypeSecurityMixin", object_type_id: int
    ) -> Security:
        """Возвращает права доступа на ТИП объекта (кто что может с объектами типа).

        Read-only снимок безопасности типа объекта: какие субъекты (пользователи,
        группы, роли) и какие действия (``ActionType``) разрешены/запрещены для типа в
        целом (например, право создавать объекты данного типа). Эти права действуют как
        настройки по умолчанию для экземпляров типа. Метод только читает права.

        Когда применять: аудит прав на уровне типа, проверка кто может создавать/читать
        объекты типа. Для прав на конкретный ЭКЗЕМПЛЯР (версию объекта) используйте
        :meth:`object_security`, для всех типов сразу — :meth:`object_types_security`.

        Args:
            object_type_id: Идентификатор ТИПА объекта (метаданное «тип объекта»), а не
                идентификатор объекта или его версии.

        Returns:
            Снимок прав по схеме :class:`Security` (``targets`` / ``actions`` /
            ``permissions`` / ``durations`` / ``conditions``). Пустые списки означают
            отсутствие соответствующих настроек.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если тип не найден).

        Example:
            async with IPSClient(config=config) as ips:
                sec = await ips.object_type_security(1031)  # 1031 = id типа объекта
                for action in sec.actions:
                    print(action.action_id, action.is_allow_by_default)

        Notes:
            operationId ``Security_GetObjectTypeSecurity``; путь
            ``GET /core/api/security/objectTypes/{objectTypeId}`` (``SecurityDto``).
        """
        data = await self._request("get", f"/core/api/security/objectTypes/{object_type_id}")
        return Security.model_validate(data)
