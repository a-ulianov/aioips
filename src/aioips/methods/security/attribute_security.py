"""Метод чтения прав доступа на атрибут."""

from ...core import APIManager
from ...schemas.security import Security


class AttributeSecurityMixin(APIManager):
    """Реализует ``GET /core/api/security/attributes/{attributeId}``.

    operationId ``Security_GetAttributeSecurity``.
    """

    async def attribute_security(self: "AttributeSecurityMixin", attribute_id: int) -> Security:
        """Возвращает права доступа на АТРИБУТ (кто может читать/изменять атрибут).

        Read-only снимок безопасности атрибута: какие субъекты (пользователи, группы,
        роли) и какие действия (``ActionType``: чтение, изменение значения) разрешены/
        запрещены для данного атрибута. Позволяет реализовать построчно-полевую защиту
        (например, скрыть/защитить от записи отдельный атрибут). Метод только читает права.

        Когда применять: аудит доступа к конкретному атрибуту, проверка кто может видеть
        или менять его значение. Для прав на объект/тип используйте
        :meth:`object_security` / :meth:`object_type_security`.

        Args:
            attribute_id: Идентификатор АТРИБУТА (метаданное «атрибут»), а не значения
                атрибута в объекте.

        Returns:
            Снимок прав по схеме :class:`Security` (``targets`` / ``actions`` /
            ``permissions`` / ``durations`` / ``conditions``). Пустые списки означают
            отсутствие соответствующих настроек.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если атрибут не найден).

        Example:
            async with IPSClient(config=config) as ips:
                sec = await ips.attribute_security(1029)  # 1029 = id атрибута
                for perm in sec.permissions:
                    print(perm.target_id, perm.action_id, perm.access_type)

        Notes:
            operationId ``Security_GetAttributeSecurity``; путь
            ``GET /core/api/security/attributes/{attributeId}`` (``SecurityDto``).
        """
        data = await self._request("get", f"/core/api/security/attributes/{attribute_id}")
        return Security.model_validate(data)
