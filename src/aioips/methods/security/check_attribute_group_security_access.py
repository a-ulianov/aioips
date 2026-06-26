"""Метод проверки доступа текущего пользователя к конкретной группе атрибутов."""

from ...core import APIManager
from ...schemas.security import SecurityCheckAccess


class CheckAttributeGroupSecurityAccessMixin(APIManager):
    """Реализует ``POST /core/api/security/attributeGroups/{attributeGroupId}/checkAccess``.

    operationId ``Security_CheckAttributeGroupSecurityAccess``.
    """

    async def check_attribute_group_security_access(
        self: "CheckAttributeGroupSecurityAccessMixin",
        attribute_group_id: int,
        check: SecurityCheckAccess,
    ) -> bool:
        """Проверяет доступ текущего пользователя к конкретной группе атрибутов.

        READ-проверка прав (ничего не меняет): есть ли у текущего пользователя право
        ``check.action_type`` на группу атрибутов ``attribute_group_id``. Для всей коллекции
        групп используйте :meth:`check_attribute_groups_security_access`.

        Когда применять: проверить возможность операции над конкретной группой атрибутов
        до её выполнения, без чтения полного снимка прав (:meth:`attribute_group_security`).

        Args:
            attribute_group_id: Идентификатор группы атрибутов (цель защиты).
            check: Параметры проверки (:class:`SecurityCheckAccess`): ``action_type`` —
                проверяемое право (``ActionType``); ``default_access`` — что вернуть, если
                права ещё не назначались (``None`` — взять дефолт цели); ``throw_ac_exception``
                — при ``True`` сервер бросит 403 вместо ответа ``False``.

        Returns:
            ``True``, если право есть; ``False`` — если нет (и ``throw_ac_exception`` —
            ``False``). При пустом теле ответа возвращается ``False`` (fail-closed).

        Raises:
            IPSError: При ошибочном ответе сервера; в т.ч. 403, если ``throw_ac_exception``
                — ``True`` и прав нет; 404, если группа не найдена.

        Example:
            from aioips.schemas.security import SecurityCheckAccess

            async with IPSClient(config=config) as ips:
                allowed = await ips.check_attribute_group_security_access(
                    42, SecurityCheckAccess(action_type="read")
                )

        Notes:
            operationId ``Security_CheckAttributeGroupSecurityAccess``; путь
            ``POST /core/api/security/attributeGroups/{attributeGroupId}/checkAccess``
            (``CheckAccessDto``). Связанный read-снимок: :meth:`attribute_group_security`.
        """
        body = check.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request(
            "post",
            f"/core/api/security/attributeGroups/{attribute_group_id}/checkAccess",
            json=body,
        )
        return bool(data) if data is not None else False
