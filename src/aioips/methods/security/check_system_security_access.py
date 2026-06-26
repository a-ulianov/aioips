"""Метод проверки доступа текущего пользователя к системе в целом."""

from ...core import APIManager
from ...schemas.security import SecurityCheckAccess


class CheckSystemSecurityAccessMixin(APIManager):
    """Реализует ``POST /core/api/security/system/checkAccess``.

    operationId ``Security_CheckSystemSecurityAccess``.
    """

    async def check_system_security_access(
        self: "CheckSystemSecurityAccessMixin",
        check: SecurityCheckAccess,
    ) -> bool:
        """Проверяет доступ текущего пользователя к системе в целом (общесистемное право).

        READ-проверка прав (ничего не меняет): есть ли у текущего пользователя право
        ``check.action_type`` на уровне всей системы IPS — общесистемные/административные
        полномочия. Это самый общий слой прав, поверх которого действуют права на типы,
        атрибуты и объекты.

        Когда применять: проверить, обладает ли пользователь административным/общесистемным
        правом (например, ``login``, ``setAccess``), без чтения полного снимка прав
        (:meth:`system_security`). Для прав на конкретный тип/объект/атрибут используйте
        :meth:`check_object_type_security_access` / :meth:`check_object_security_access` /
        :meth:`check_attribute_security_access`.

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
                is_admin = await ips.check_system_security_access(
                    SecurityCheckAccess(action_type="setAccess")
                )

        Notes:
            operationId ``Security_CheckSystemSecurityAccess``; путь
            ``POST /core/api/security/system/checkAccess`` (``CheckAccessDto``).
            Связанный read-снимок: :meth:`system_security`.
        """
        body = check.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request("post", "/core/api/security/system/checkAccess", json=body)
        return bool(data) if data is not None else False
