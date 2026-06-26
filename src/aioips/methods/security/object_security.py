"""Метод чтения прав доступа на версию объекта."""

from ...core import APIManager
from ...schemas.security import Security


class ObjectSecurityMixin(APIManager):
    """Реализует ``GET /core/api/security/objects/{objectVersionId}``.

    operationId ``Security_GetObjectSecurity``.
    """

    async def object_security(self: "ObjectSecurityMixin", object_version_id: int) -> Security:
        """Возвращает права доступа на конкретную ВЕРСИЮ объекта (кто что может).

        Read-only снимок безопасности объекта: какие субъекты (пользователи, группы,
        роли) и какие действия (``ActionType``: чтение, изменение, удаление, печать и
        т.п.) разрешены/запрещены на данной версии объекта, с конкретными правами,
        сроками и условиями. Метод только читает права, не изменяет их.

        Когда применять: аудит доступа, отображение «кто что может» по объекту, проверка
        унаследованных и явных прав. Для прав на ТИП объекта (а не экземпляр) используйте
        :meth:`object_type_security`, для атрибута — :meth:`attribute_security`.

        Предусловие по id-пространству (критично): аргумент — это идентификатор ВЕРСИИ
        объекта (``id`` / F_ID, ``objectVersionId``), а НЕ идентификатор объекта
        (``objectID`` / F_OBJECT_ID). Права привязаны к версии. См. объектной модели IPS.

        Args:
            object_version_id: Идентификатор ВЕРСИИ объекта (``objectVersionId`` /
                ``id`` / F_ID). Не идентификатор объекта (``objectID``).

        Returns:
            Снимок прав по схеме :class:`Security`: ``targets`` (субъекты),
            ``actions`` (контролируемые действия), ``permissions`` (связки
            субъект × действие × вид доступа), ``durations``, ``conditions``. Пустые
            списки означают отсутствие соответствующих настроек.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если версия не найдена).

        Example:
            async with IPSClient(config=config) as ips:
                sec = await ips.object_security(204931)  # 204931 = id версии объекта
                for perm in sec.permissions:
                    print(perm.target_id, perm.action_id, perm.access_type)

        Notes:
            operationId ``Security_GetObjectSecurity``; путь
            ``GET /core/api/security/objects/{objectVersionId}`` (``SecurityDto``).
        """
        data = await self._request("get", f"/core/api/security/objects/{object_version_id}")
        return Security.model_validate(data)
