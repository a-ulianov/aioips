"""Метод чтения прав доступа на шаг схемы ЖЦ для типа объекта."""

from ...core import APIManager
from ...schemas.security import Security


class ObjectTypeLifecycleStepSecurityMixin(APIManager):
    """Реализует чтение прав на шаг схемы ЖЦ типа объекта.

    Путь ``GET /core/api/security/objectTypes/{objectTypeId}/lifecycleSchemeSteps/
    {lifecycleSchemeStepId}``; operationId
    ``Security_GetObjectTypeLifecycleSchemeStepSecurity``.
    """

    async def object_type_lifecycle_step_security(
        self: "ObjectTypeLifecycleStepSecurityMixin",
        object_type_id: int,
        lifecycle_scheme_step_id: int,
    ) -> Security:
        """Возвращает права доступа на ШАГ схемы ЖЦ конкретного типа объекта.

        Read-only снимок безопасности для пары «тип объекта × шаг схемы жизненного цикла»:
        какие субъекты (пользователи, группы, роли) и какие действия (``ActionType``)
        разрешены/запрещены для объектов данного типа, когда они находятся на данном шаге
        ЖЦ. Это контекстно-зависимые права: один и тот же объект на разных шагах ЖЦ может
        иметь разный доступ. Метод только читает права, не изменяет их.

        Когда применять: аудит того, кто что может делать с объектами типа на конкретном
        шаге ЖЦ (например, утверждать на шаге «На согласовании»). Для прав на атрибут в
        этом же контексте используйте :meth:`object_type_lifecycle_step_attribute_security`,
        для прав на тип безотносительно шага — :meth:`object_type_security`.

        Args:
            object_type_id: Идентификатор ТИПА объекта (метаданное «тип объекта»), а не
                идентификатор объекта или версии.
            lifecycle_scheme_step_id: Идентификатор ШАГА схемы ЖЦ (``lifecycleSchemeStepId``),
                а не идентификатор схемы или уровня ЖЦ.

        Returns:
            Снимок прав по схеме :class:`Security`: ``targets`` (субъекты), ``actions``
            (контролируемые действия), ``permissions`` (связки субъект × действие × вид
            доступа), ``durations``, ``conditions``. Пустые списки означают отсутствие
            соответствующих настроек.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если тип или шаг не найден).

        Example:
            async with IPSClient(config=config) as ips:
                sec = await ips.object_type_lifecycle_step_security(1031, 5)
                for perm in sec.permissions:
                    print(perm.target_id, perm.action_id, perm.access_type)

        Notes:
            operationId ``Security_GetObjectTypeLifecycleSchemeStepSecurity``; путь
            ``GET /core/api/security/objectTypes/{objectTypeId}/lifecycleSchemeSteps/
            {lifecycleSchemeStepId}`` (``SecurityDto``).
        """
        data = await self._request(
            "get",
            f"/core/api/security/objectTypes/{object_type_id}"
            f"/lifecycleSchemeSteps/{lifecycle_scheme_step_id}",
        )
        return Security.model_validate(data)
