"""Метод проверки доступа текущего пользователя к коллекции предметных областей."""

from ...core import APIManager
from ...schemas.security import SecurityCheckAccess


class CheckSubjectAreasSecurityAccessMixin(APIManager):
    """Реализует ``POST /core/api/security/subjectAreas/checkAccess``.

    operationId ``Security_CheckSubjectAreaCollectionSecurityAccess``.
    """

    async def check_subject_areas_security_access(
        self: "CheckSubjectAreasSecurityAccessMixin",
        check: SecurityCheckAccess,
    ) -> bool:
        """Проверяет доступ текущего пользователя к коллекции предметных областей.

        READ-проверка прав (ничего не меняет): есть ли у текущего пользователя право
        ``check.action_type`` на уровне коллекции предметных областей (subject areas).

        Когда применять: проверить возможность операции над списком предметных областей до
        её выполнения, без чтения полного снимка прав (:meth:`subject_areas_security`).

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
                allowed = await ips.check_subject_areas_security_access(
                    SecurityCheckAccess(action_type="read")
                )

        Notes:
            operationId ``Security_CheckSubjectAreaCollectionSecurityAccess``; путь
            ``POST /core/api/security/subjectAreas/checkAccess`` (``CheckAccessDto``).
            Связанный read-снимок: :meth:`subject_areas_security`.
        """
        body = check.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request("post", "/core/api/security/subjectAreas/checkAccess", json=body)
        return bool(data) if data is not None else False
