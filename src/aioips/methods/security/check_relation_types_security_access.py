"""Метод проверки доступа текущего пользователя к коллекции типов связей."""

from ...core import APIManager
from ...schemas.security import SecurityCheckAccess


class CheckRelationTypesSecurityAccessMixin(APIManager):
    """Реализует ``POST /core/api/security/relationTypes/checkAccess``.

    operationId ``Security_CheckRelationTypeCollectionSecurityAccess``.
    """

    async def check_relation_types_security_access(
        self: "CheckRelationTypesSecurityAccessMixin",
        check: SecurityCheckAccess,
    ) -> bool:
        """Проверяет доступ текущего пользователя к коллекции типов связей.

        READ-проверка прав (ничего не меняет): есть ли у текущего пользователя право
        ``check.action_type`` на уровне всей коллекции типов связей. Для конкретного типа
        связи используйте :meth:`check_relation_type_security_access`.

        Когда применять: проверить возможность операции над списком типов связей до её
        выполнения, без чтения полного снимка прав (:meth:`relation_types_security`).

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
                allowed = await ips.check_relation_types_security_access(
                    SecurityCheckAccess(action_type="read")
                )

        Notes:
            operationId ``Security_CheckRelationTypeCollectionSecurityAccess``; путь
            ``POST /core/api/security/relationTypes/checkAccess`` (``CheckAccessDto``).
            Связанный read-снимок: :meth:`relation_types_security`.
        """
        body = check.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request(
            "post", "/core/api/security/relationTypes/checkAccess", json=body
        )
        return bool(data) if data is not None else False
