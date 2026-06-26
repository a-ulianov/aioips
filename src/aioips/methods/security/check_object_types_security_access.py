"""Метод проверки доступа текущего пользователя к коллекции типов объектов."""

from ...core import APIManager
from ...schemas.security import SecurityCheckAccess


class CheckObjectTypesSecurityAccessMixin(APIManager):
    """Реализует ``POST /core/api/security/objectTypes/checkAccess``.

    operationId ``Security_CheckObjectTypeCollectionSecurityAccess``.
    """

    async def check_object_types_security_access(
        self: "CheckObjectTypesSecurityAccessMixin",
        check: SecurityCheckAccess,
    ) -> bool:
        """Проверяет доступ текущего пользователя к коллекции типов объектов.

        READ-проверка прав (ничего не меняет): есть ли у текущего пользователя право
        ``check.action_type`` на уровне всей коллекции типов объектов. Для конкретного
        типа используйте :meth:`check_object_type_security_access`.

        Когда применять: проверить возможность операции над списком типов объектов до её
        выполнения, без чтения полного снимка прав (:meth:`object_types_security`).

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
                allowed = await ips.check_object_types_security_access(
                    SecurityCheckAccess(action_type="create")
                )

        Notes:
            operationId ``Security_CheckObjectTypeCollectionSecurityAccess``; путь
            ``POST /core/api/security/objectTypes/checkAccess`` (``CheckAccessDto``).
            Связанный read-снимок: :meth:`object_types_security`.
        """
        body = check.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request("post", "/core/api/security/objectTypes/checkAccess", json=body)
        return bool(data) if data is not None else False
