"""Метод чтения прав доступа на атрибут на шаге схемы ЖЦ для типа объекта."""

from ...core import APIManager
from ...schemas.security import Security


class ObjectTypeLifecycleStepAttributeSecurityMixin(APIManager):
    """Реализует чтение прав на атрибут на шаге схемы ЖЦ типа объекта.

    Путь ``GET /core/api/security/objectTypes/{objectTypeId}/lifecycleSchemeSteps/
    {lifecycleSchemeStepId}/attributes/{attributeId}``; operationId
    ``Security_GetObjectTypeLifecycleSchemeStepSecurityForAttribute``.
    """

    async def object_type_lifecycle_step_attribute_security(
        self: "ObjectTypeLifecycleStepAttributeSecurityMixin",
        object_type_id: int,
        lifecycle_scheme_step_id: int,
        attribute_id: int,
    ) -> Security:
        """Возвращает права на АТРИБУТ типа объекта на конкретном шаге схемы ЖЦ.

        Read-only снимок безопасности для тройки «тип объекта × шаг схемы ЖЦ × атрибут»:
        какие субъекты (пользователи, группы, роли) и какие действия (``ActionType``:
        чтение, изменение значения) разрешены/запрещены для данного атрибута объектов
        этого типа, когда они находятся на данном шаге ЖЦ. Самый узкий, контекстно-
        зависимый слой полевой защиты: атрибут может быть редактируемым на одном шаге ЖЦ и
        защищён от записи на другом. Метод только читает права, не изменяет их.

        Когда применять: аудит того, кто может видеть/менять конкретный атрибут на
        конкретном шаге ЖЦ типа объекта. Для прав на весь шаг (а не отдельный атрибут)
        используйте :meth:`object_type_lifecycle_step_security`, для прав на атрибут
        безотносительно ЖЦ — :meth:`attribute_security`.

        Args:
            object_type_id: Идентификатор ТИПА объекта (метаданное «тип объекта»), а не
                идентификатор объекта или версии.
            lifecycle_scheme_step_id: Идентификатор ШАГА схемы ЖЦ (``lifecycleSchemeStepId``),
                а не идентификатор схемы или уровня ЖЦ.
            attribute_id: Идентификатор АТРИБУТА (метаданное «атрибут»), а не значения
                атрибута в объекте.

        Returns:
            Снимок прав по схеме :class:`Security`: ``targets`` (субъекты), ``actions``
            (контролируемые действия), ``permissions`` (связки субъект × действие × вид
            доступа), ``durations``, ``conditions``. Пустые списки означают отсутствие
            соответствующих настроек.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если тип, шаг или атрибут
                не найден).

        Example:
            async with IPSClient(config=config) as ips:
                sec = await ips.object_type_lifecycle_step_attribute_security(1031, 5, 1029)
                for perm in sec.permissions:
                    print(perm.target_id, perm.action_id, perm.access_type)

        Notes:
            operationId ``Security_GetObjectTypeLifecycleSchemeStepSecurityForAttribute``;
            путь ``GET /core/api/security/objectTypes/{objectTypeId}/lifecycleSchemeSteps/
            {lifecycleSchemeStepId}/attributes/{attributeId}`` (``SecurityDto``).
        """
        data = await self._request(
            "get",
            f"/core/api/security/objectTypes/{object_type_id}"
            f"/lifecycleSchemeSteps/{lifecycle_scheme_step_id}"
            f"/attributes/{attribute_id}",
        )
        return Security.model_validate(data)
