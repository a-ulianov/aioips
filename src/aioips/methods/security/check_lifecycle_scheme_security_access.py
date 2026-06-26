"""Метод проверки доступа текущего пользователя к конкретной схеме ЖЦ."""

from ...core import APIManager
from ...schemas.security import SecurityCheckAccess


class CheckLifecycleSchemeSecurityAccessMixin(APIManager):
    """Реализует ``POST /core/api/security/lifecycleSchemes/{lifecycleSchemeId}/checkAccess``.

    operationId ``Security_CheckLifecycleSchemeSecurityAccess``.
    """

    async def check_lifecycle_scheme_security_access(
        self: "CheckLifecycleSchemeSecurityAccessMixin",
        lifecycle_scheme_id: int,
        check: SecurityCheckAccess,
    ) -> bool:
        """Проверяет доступ текущего пользователя к конкретной схеме жизненного цикла.

        READ-проверка прав (ничего не меняет): есть ли у текущего пользователя право
        ``check.action_type`` на схему ЖЦ ``lifecycle_scheme_id``. Для всей коллекции схем
        используйте :meth:`check_lifecycle_schemes_security_access`.

        Когда применять: проверить возможность операции над конкретной схемой ЖЦ до её
        выполнения, без чтения полного снимка прав (:meth:`lifecycle_scheme_security`).

        Args:
            lifecycle_scheme_id: Идентификатор схемы жизненного цикла (цель защиты).
            check: Параметры проверки (:class:`SecurityCheckAccess`): ``action_type`` —
                проверяемое право (``ActionType``); ``default_access`` — что вернуть, если
                права ещё не назначались (``None`` — взять дефолт цели); ``throw_ac_exception``
                — при ``True`` сервер бросит 403 вместо ответа ``False``.

        Returns:
            ``True``, если право есть; ``False`` — если нет (и ``throw_ac_exception`` —
            ``False``). При пустом теле ответа возвращается ``False`` (fail-closed).

        Raises:
            IPSError: При ошибочном ответе сервера; в т.ч. 403, если ``throw_ac_exception``
                — ``True`` и прав нет; 404, если схема не найдена.

        Example:
            from aioips.schemas.security import SecurityCheckAccess

            async with IPSClient(config=config) as ips:
                allowed = await ips.check_lifecycle_scheme_security_access(
                    7, SecurityCheckAccess(action_type="read")
                )

        Notes:
            operationId ``Security_CheckLifecycleSchemeSecurityAccess``; путь
            ``POST /core/api/security/lifecycleSchemes/{lifecycleSchemeId}/checkAccess``
            (``CheckAccessDto``). Связанный read-снимок: :meth:`lifecycle_scheme_security`.
        """
        body = check.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request(
            "post",
            f"/core/api/security/lifecycleSchemes/{lifecycle_scheme_id}/checkAccess",
            json=body,
        )
        return bool(data) if data is not None else False
