"""Метод проверки доступа текущего пользователя к коллекции схем ЖЦ."""

from ...core import APIManager
from ...schemas.security import SecurityCheckAccess


class CheckLifecycleSchemesSecurityAccessMixin(APIManager):
    """Реализует ``POST /core/api/security/lifecycleSchemes/checkAccess``.

    operationId ``Security_CheckLifecycleSchemeCollectionSecurityAccess``.
    """

    async def check_lifecycle_schemes_security_access(
        self: "CheckLifecycleSchemesSecurityAccessMixin",
        check: SecurityCheckAccess,
    ) -> bool:
        """Проверяет доступ текущего пользователя к коллекции схем жизненного цикла.

        READ-проверка прав (ничего не меняет): есть ли у текущего пользователя право
        ``check.action_type`` на уровне всей коллекции схем ЖЦ. Для конкретной схемы
        используйте :meth:`check_lifecycle_scheme_security_access`.

        Когда применять: проверить возможность операции над списком схем ЖЦ до её
        выполнения, без чтения полного снимка прав (:meth:`lifecycle_schemes_security`).

        Args:
            check: Параметры проверки (:class:`SecurityCheckAccess`): ``action_type`` —
                проверяемое право (``ActionType``); ``default_access`` — что вернуть, если
                права ещё не назначались (``None`` — взять дефолт цели); ``throw_ac_exception``
                — при ``True`` сервер бросит 403 вместо ответа ``False``.

        Returns:
            ``True``, если право есть; ``False`` — если нет (и ``throw_ac_exception`` —
            ``False``). При пустом теле ответа возвращается ``False`` (fail-closed).

        Raises:
            IPSError: При ошибочном ответе сервера; в т.ч. 403, если ``throw_ac_exception``
                — ``True`` и прав нет.

        Example:
            from aioips.schemas.security import SecurityCheckAccess

            async with IPSClient(config=config) as ips:
                allowed = await ips.check_lifecycle_schemes_security_access(
                    SecurityCheckAccess(action_type="read")
                )

        Notes:
            operationId ``Security_CheckLifecycleSchemeCollectionSecurityAccess``; путь
            ``POST /core/api/security/lifecycleSchemes/checkAccess`` (``CheckAccessDto``).
            Связанный read-снимок: :meth:`lifecycle_schemes_security`.
        """
        body = check.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request(
            "post", "/core/api/security/lifecycleSchemes/checkAccess", json=body
        )
        return bool(data) if data is not None else False
