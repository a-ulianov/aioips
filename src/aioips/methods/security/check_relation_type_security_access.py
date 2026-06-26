"""Метод проверки доступа текущего пользователя к конкретному типу связи."""

from ...core import APIManager
from ...schemas.security import SecurityCheckAccess


class CheckRelationTypeSecurityAccessMixin(APIManager):
    """Реализует ``POST /core/api/security/relationTypes/{relationTypeId}/checkAccess``.

    operationId ``Security_CheckRelationTypeSecurityAccess``.
    """

    async def check_relation_type_security_access(
        self: "CheckRelationTypeSecurityAccessMixin",
        relation_type_id: int,
        check: SecurityCheckAccess,
    ) -> bool:
        """Проверяет доступ текущего пользователя к конкретному типу связи.

        READ-проверка прав (ничего не меняет): есть ли у текущего пользователя право
        ``check.action_type`` на тип связи ``relation_type_id`` (например, право создавать
        связи этого типа). Для всей коллекции типов связей используйте
        :meth:`check_relation_types_security_access`.

        Когда применять: до создания/удаления связи заданного типа — убедиться, что
        пользователь вправе её выполнить, без чтения полного снимка прав
        (:meth:`relation_type_security`).

        Args:
            relation_type_id: Идентификатор типа связи (цель защиты).
            check: Параметры проверки (:class:`SecurityCheckAccess`): ``action_type`` —
                проверяемое право (``ActionType``); ``default_access`` — что вернуть, если
                права ещё не назначались (``None`` — взять дефолт цели); ``throw_ac_exception``
                — при ``True`` сервер бросит 403 вместо ответа ``False``.

        Returns:
            ``True``, если право есть; ``False`` — если нет (и ``throw_ac_exception`` —
            ``False``). При пустом теле ответа возвращается ``False`` (fail-closed).

        Raises:
            IPSError: При ошибочном ответе сервера; в т.ч. 403, если ``throw_ac_exception``
                — ``True`` и прав нет; 404, если тип связи не найден.

        Example:
            from aioips.schemas.security import SecurityCheckAccess

            async with IPSClient(config=config) as ips:
                allowed = await ips.check_relation_type_security_access(
                    12, SecurityCheckAccess(action_type="addLink")
                )

        Notes:
            operationId ``Security_CheckRelationTypeSecurityAccess``; путь
            ``POST /core/api/security/relationTypes/{relationTypeId}/checkAccess``
            (``CheckAccessDto``). Связанный read-снимок: :meth:`relation_type_security`.
        """
        body = check.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request(
            "post", f"/core/api/security/relationTypes/{relation_type_id}/checkAccess", json=body
        )
        return bool(data) if data is not None else False
