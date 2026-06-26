"""Метод проверки доступа текущего пользователя к конкретному типу объекта."""

from ...core import APIManager
from ...schemas.security import SecurityCheckAccess


class CheckObjectTypeSecurityAccessMixin(APIManager):
    """Реализует ``POST /core/api/security/objectTypes/{objectTypeId}/checkAccess``.

    operationId ``Security_CheckObjectTypeSecurityAccess``.
    """

    async def check_object_type_security_access(
        self: "CheckObjectTypeSecurityAccessMixin",
        object_type_id: int,
        check: SecurityCheckAccess,
    ) -> bool:
        """Проверяет доступ текущего пользователя к конкретному типу объекта.

        READ-проверка прав (ничего не меняет): есть ли у текущего пользователя право
        ``check.action_type`` на тип объекта ``object_type_id`` (например, право создавать
        объекты этого типа). Это проверка на уровне ТИПА, а не конкретного экземпляра; для
        версии объекта используйте :meth:`check_object_security_access`. Для всей коллекции
        типов используйте :meth:`check_object_types_security_access`.

        Когда применять: до показа кнопки «Создать» или иной операции по типу — убедиться,
        что пользователь вправе её выполнить, без чтения полного снимка прав
        (:meth:`object_type_security`).

        Args:
            object_type_id: Идентификатор типа объекта (цель защиты).
            check: Параметры проверки (:class:`SecurityCheckAccess`): ``action_type`` —
                проверяемое право (``ActionType``); ``default_access`` — что вернуть, если
                права ещё не назначались (``None`` — взять дефолт цели); ``throw_ac_exception``
                — при ``True`` сервер бросит 403 вместо ответа ``False``.

        Returns:
            ``True``, если право есть; ``False`` — если нет (и ``throw_ac_exception`` —
            ``False``). При пустом теле ответа возвращается ``False`` (fail-closed).

        Raises:
            IPSError: При ошибочном ответе сервера; в т.ч. 403, если ``throw_ac_exception``
                — ``True`` и прав нет; 404, если тип не найден.

        Example:
            from aioips.schemas.security import SecurityCheckAccess

            async with IPSClient(config=config) as ips:
                allowed = await ips.check_object_type_security_access(
                    1031, SecurityCheckAccess(action_type="create")
                )

        Notes:
            operationId ``Security_CheckObjectTypeSecurityAccess``; путь
            ``POST /core/api/security/objectTypes/{objectTypeId}/checkAccess``
            (``CheckAccessDto``). Связанный read-снимок: :meth:`object_type_security`.
        """
        body = check.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request(
            "post", f"/core/api/security/objectTypes/{object_type_id}/checkAccess", json=body
        )
        return bool(data) if data is not None else False
