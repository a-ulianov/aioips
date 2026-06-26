"""Метод чтения прав доступа на уровень ЖЦ."""

from ...core import APIManager
from ...schemas.security import Security


class LifecycleLevelSecurityMixin(APIManager):
    """Реализует ``GET /core/api/security/lifecycleLevels/{lifecycleLevelId}``.

    operationId ``Security_GetLifecycleLevelSecurity``.
    """

    async def lifecycle_level_security(
        self: "LifecycleLevelSecurityMixin", lifecycle_level_id: int
    ) -> Security:
        """Возвращает права доступа на УРОВЕНЬ ЖЦ (кто что может на данном уровне ЖЦ).

        Read-only снимок безопасности конкретного уровня жизненного цикла: какие субъекты
        (пользователи, группы, роли) и какие действия (``ActionType``) разрешены/запрещены
        на данном уровне ЖЦ. Управляет тем, кто вправе работать с объектами на этом уровне
        жизненного цикла. Метод только читает права, не изменяет их.

        Когда применять: аудит доступа к конкретному уровню ЖЦ. Для прав на ВСЕ уровни
        сразу используйте :meth:`lifecycle_levels_security`, для схемы ЖЦ —
        :meth:`lifecycle_scheme_security`.

        Args:
            lifecycle_level_id: Идентификатор УРОВНЯ ЖЦ (метаданное «уровень жизненного
                цикла»), а не идентификатор шага или схемы ЖЦ.

        Returns:
            Снимок прав по схеме :class:`Security`: ``targets`` (субъекты), ``actions``
            (контролируемые действия), ``permissions`` (связки субъект × действие × вид
            доступа), ``durations``, ``conditions``. Пустые списки означают отсутствие
            соответствующих настроек.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если уровень не найден).

        Example:
            async with IPSClient(config=config) as ips:
                sec = await ips.lifecycle_level_security(3)  # 3 = id уровня ЖЦ
                for perm in sec.permissions:
                    print(perm.target_id, perm.action_id, perm.access_type)

        Notes:
            operationId ``Security_GetLifecycleLevelSecurity``; путь
            ``GET /core/api/security/lifecycleLevels/{lifecycleLevelId}`` (``SecurityDto``).
        """
        data = await self._request(
            "get", f"/core/api/security/lifecycleLevels/{lifecycle_level_id}"
        )
        return Security.model_validate(data)
