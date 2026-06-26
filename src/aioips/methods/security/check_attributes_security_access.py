"""Метод проверки доступа текущего пользователя к коллекции атрибутов."""

from ...core import APIManager
from ...schemas.security import SecurityCheckAccess


class CheckAttributesSecurityAccessMixin(APIManager):
    """Реализует ``POST /core/api/security/attributes/checkAccess``.

    operationId ``Security_CheckAttributeCollectionSecurityAccess``.
    """

    async def check_attributes_security_access(
        self: "CheckAttributesSecurityAccessMixin",
        check: SecurityCheckAccess,
    ) -> bool:
        """Проверяет доступ текущего пользователя к коллекции атрибутов.

        READ-проверка прав (ничего не меняет): есть ли у текущего пользователя право
        ``check.action_type`` на уровне всей коллекции атрибутов (не на отдельный атрибут).
        Для конкретного атрибута используйте :meth:`check_attribute_security_access`.

        Когда применять: проверить возможность операции над списком атрибутов до её
        выполнения, без чтения полного снимка прав (:meth:`attributes_collection_security`).

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
                allowed = await ips.check_attributes_security_access(
                    SecurityCheckAccess(action_type="read")
                )

        Notes:
            operationId ``Security_CheckAttributeCollectionSecurityAccess``; путь
            ``POST /core/api/security/attributes/checkAccess`` (``CheckAccessDto``).
            Связанный read-снимок: :meth:`attributes_collection_security`.
        """
        body = check.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request("post", "/core/api/security/attributes/checkAccess", json=body)
        return bool(data) if data is not None else False
