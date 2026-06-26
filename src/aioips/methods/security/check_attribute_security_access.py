"""Метод проверки доступа текущего пользователя к конкретному атрибуту."""

from ...core import APIManager
from ...schemas.security import SecurityCheckAccess


class CheckAttributeSecurityAccessMixin(APIManager):
    """Реализует ``POST /core/api/security/attributes/{attributeId}/checkAccess``.

    operationId ``Security_CheckAttributeSecurityAccess``.
    """

    async def check_attribute_security_access(
        self: "CheckAttributeSecurityAccessMixin",
        attribute_id: int,
        check: SecurityCheckAccess,
    ) -> bool:
        """Проверяет доступ текущего пользователя к конкретному атрибуту.

        READ-проверка прав (ничего не меняет): есть ли у текущего пользователя право
        ``check.action_type`` на атрибут ``attribute_id`` (например, право читать или
        изменять значение этого атрибута). Для всей коллекции атрибутов используйте
        :meth:`check_attributes_security_access`.

        Когда применять: до показа/редактирования значения атрибута — убедиться, что
        пользователь вправе выполнить действие, без чтения полного снимка прав
        (:meth:`attribute_security`).

        Args:
            attribute_id: Идентификатор типа атрибута (цель защиты).
            check: Параметры проверки (:class:`SecurityCheckAccess`): ``action_type`` —
                проверяемое право (``ActionType``); ``default_access`` — что вернуть, если
                права ещё не назначались (``None`` — взять дефолт цели); ``throw_ac_exception``
                — при ``True`` сервер бросит 403 вместо ответа ``False``.

        Returns:
            ``True``, если право есть; ``False`` — если нет (и ``throw_ac_exception`` —
            ``False``). При пустом теле ответа возвращается ``False`` (fail-closed).

        Raises:
            IPSError: При ошибочном ответе сервера; в т.ч. 403, если ``throw_ac_exception``
                — ``True`` и прав нет; 404, если атрибут не найден.

        Example:
            from aioips.schemas.security import SecurityCheckAccess

            async with IPSClient(config=config) as ips:
                allowed = await ips.check_attribute_security_access(
                    1029, SecurityCheckAccess(action_type="read")
                )

        Notes:
            operationId ``Security_CheckAttributeSecurityAccess``; путь
            ``POST /core/api/security/attributes/{attributeId}/checkAccess``
            (``CheckAccessDto``). Связанный read-снимок: :meth:`attribute_security`.
        """
        body = check.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request(
            "post", f"/core/api/security/attributes/{attribute_id}/checkAccess", json=body
        )
        return bool(data) if data is not None else False
