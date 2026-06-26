"""Метод проверки доступа текущего пользователя к конкретному уровню ЖЦ."""

from ...core import APIManager
from ...schemas.security import SecurityCheckAccess


class CheckLifecycleLevelSecurityAccessMixin(APIManager):
    """Реализует ``POST /core/api/security/lifecycleLevels/{lifecycleLevelId}/checkAccess``.

    operationId ``Security_CheckLifecycleLevelSecurityAccess``.
    """

    async def check_lifecycle_level_security_access(
        self: "CheckLifecycleLevelSecurityAccessMixin",
        lifecycle_level_id: int,
        check: SecurityCheckAccess,
    ) -> bool:
        """Проверяет доступ текущего пользователя к конкретному уровню жизненного цикла.

        READ-проверка прав (ничего не меняет): есть ли у текущего пользователя право
        ``check.action_type`` на уровень ЖЦ ``lifecycle_level_id``. Для всей коллекции
        уровней используйте :meth:`check_lifecycle_levels_security_access`.

        Когда применять: проверить возможность операции над конкретным уровнем ЖЦ до её
        выполнения, без чтения полного снимка прав (:meth:`lifecycle_level_security`).

        Args:
            lifecycle_level_id: Идентификатор уровня жизненного цикла (цель защиты).
            check: Параметры проверки (:class:`SecurityCheckAccess`): ``action_type`` —
                проверяемое право (``ActionType``); ``default_access`` — что вернуть, если
                права ещё не назначались (``None`` — взять дефолт цели); ``throw_ac_exception``
                — при ``True`` сервер бросит 403 вместо ответа ``False``.

        Returns:
            ``True``, если право есть; ``False`` — если нет (и ``throw_ac_exception`` —
            ``False``). При пустом теле ответа возвращается ``False`` (fail-closed).

        Raises:
            IPSError: При ошибочном ответе сервера; в т.ч. 403, если ``throw_ac_exception``
                — ``True`` и прав нет; 404, если уровень не найден.

        Example:
            from aioips.schemas.security import SecurityCheckAccess

            async with IPSClient(config=config) as ips:
                allowed = await ips.check_lifecycle_level_security_access(
                    3, SecurityCheckAccess(action_type="read")
                )

        Notes:
            operationId ``Security_CheckLifecycleLevelSecurityAccess``; путь
            ``POST /core/api/security/lifecycleLevels/{lifecycleLevelId}/checkAccess``
            (``CheckAccessDto``). Связанный read-снимок: :meth:`lifecycle_level_security`.
        """
        body = check.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request(
            "post",
            f"/core/api/security/lifecycleLevels/{lifecycle_level_id}/checkAccess",
            json=body,
        )
        return bool(data) if data is not None else False
