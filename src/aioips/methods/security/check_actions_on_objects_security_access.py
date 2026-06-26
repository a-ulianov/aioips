"""Метод проверки доступа текущего пользователя к операциям над объектами."""

from ...core import APIManager
from ...schemas.security import SecurityCheckAccess


class CheckActionsOnObjectsSecurityAccessMixin(APIManager):
    """Реализует ``POST /core/api/security/actionOnObjects/checkAccess``.

    operationId ``Security_CheckActionsOnObjectsSecurityAccess``.
    """

    async def check_actions_on_objects_security_access(
        self: "CheckActionsOnObjectsSecurityAccessMixin",
        check: SecurityCheckAccess,
    ) -> bool:
        """Проверяет доступ текущего пользователя к категории «операции над объектами».

        READ-проверка прав (ничего не меняет): есть ли у пользователя, чьим токеном
        авторизован клиент, право ``check.action_type`` на общую категорию «действия над
        объектами» (массовые/служебные операции). Это проверка на уровне категории, а не
        конкретного объекта; для конкретной версии объекта используйте
        :meth:`check_object_security_access`.

        Когда применять: до показа кнопки/запуска операции — убедиться, что у пользователя
        есть нужное право, без обращения к полному снимку прав
        (:meth:`actions_on_objects_security`).

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
                allowed = await ips.check_actions_on_objects_security_access(
                    SecurityCheckAccess(action_type="read")
                )

        Notes:
            operationId ``Security_CheckActionsOnObjectsSecurityAccess``; путь
            ``POST /core/api/security/actionOnObjects/checkAccess`` (``CheckAccessDto``).
            Связанный read-снимок: :meth:`actions_on_objects_security`.
        """
        body = check.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request(
            "post", "/core/api/security/actionOnObjects/checkAccess", json=body
        )
        return bool(data) if data is not None else False
