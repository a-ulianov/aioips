"""Метод чтения прав доступа на схему ЖЦ."""

from ...core import APIManager
from ...schemas.security import Security


class LifecycleSchemeSecurityMixin(APIManager):
    """Реализует ``GET /core/api/security/lifecycleSchemes/{lifecycleSchemeId}``.

    operationId ``Security_GetLifecycleSchemeSecurity``.
    """

    async def lifecycle_scheme_security(
        self: "LifecycleSchemeSecurityMixin", lifecycle_scheme_id: int
    ) -> Security:
        """Возвращает права доступа на СХЕМУ ЖЦ (кто что может с данной схемой ЖЦ).

        Read-only снимок безопасности конкретной схемы жизненного цикла: какие субъекты
        (пользователи, группы, роли) и какие действия (``ActionType``) разрешены/запрещены
        для данной схемы ЖЦ. Управляет тем, кто вправе применять/администрировать данную
        схему жизненного цикла. Метод только читает права, не изменяет их.

        Когда применять: аудит доступа к конкретной схеме ЖЦ. Для прав на ВСЕ схемы сразу
        используйте :meth:`lifecycle_schemes_security`; права на отдельный шаг схемы для
        типа объекта — :meth:`object_type_lifecycle_step_security`.

        Args:
            lifecycle_scheme_id: Идентификатор СХЕМЫ ЖЦ (метаданное «схема жизненного
                цикла»), а не идентификатор шага или уровня ЖЦ.

        Returns:
            Снимок прав по схеме :class:`Security`: ``targets`` (субъекты), ``actions``
            (контролируемые действия), ``permissions`` (связки субъект × действие × вид
            доступа), ``durations``, ``conditions``. Пустые списки означают отсутствие
            соответствующих настроек.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если схема не найдена).

        Example:
            async with IPSClient(config=config) as ips:
                sec = await ips.lifecycle_scheme_security(15)  # 15 = id схемы ЖЦ
                for perm in sec.permissions:
                    print(perm.target_id, perm.action_id, perm.access_type)

        Notes:
            operationId ``Security_GetLifecycleSchemeSecurity``; путь
            ``GET /core/api/security/lifecycleSchemes/{lifecycleSchemeId}`` (``SecurityDto``).
        """
        data = await self._request(
            "get", f"/core/api/security/lifecycleSchemes/{lifecycle_scheme_id}"
        )
        return Security.model_validate(data)
