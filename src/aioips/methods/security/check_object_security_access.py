"""Метод проверки доступа текущего пользователя к версии объекта."""

from ...core import APIManager
from ...schemas.security import SecurityCheckAccess


class CheckObjectSecurityAccessMixin(APIManager):
    """Реализует ``POST /core/api/security/objects/{objectVersionId}/checkAccess``.

    operationId ``Security_CheckObjectSecurityAccess``.
    """

    async def check_object_security_access(
        self: "CheckObjectSecurityAccessMixin",
        object_version_id: int,
        check: SecurityCheckAccess,
    ) -> bool:
        """Проверяет доступ текущего пользователя к конкретной ВЕРСИИ объекта.

        READ-проверка прав (ничего не меняет): есть ли у текущего пользователя право
        ``check.action_type`` на конкретную версию объекта (например, право читать,
        изменять, удалять или печатать её). Самый частый кейс этого раздела.

        Предусловие по id-пространству (критично): аргумент — это идентификатор ВЕРСИИ
        объекта (``id`` / F_ID / ``objectVersionId``), а НЕ идентификатор объекта
        (``objectID`` / F_OBJECT_ID). Права привязаны к версии. См. объектной модели IPS.
        Для прав на ТИП объекта используйте :meth:`check_object_type_security_access`.

        Когда применять: до показа/запуска действия над объектом (открыть, редактировать,
        удалить) — убедиться, что пользователь вправе его выполнить, без чтения полного
        снимка прав (:meth:`object_security`).

        Args:
            object_version_id: Идентификатор ВЕРСИИ объекта (``objectVersionId`` / ``id`` /
                F_ID). Не идентификатор объекта (``objectID``).
            check: Параметры проверки (:class:`SecurityCheckAccess`): ``action_type`` —
                проверяемое право (``ActionType``); ``default_access`` — что вернуть, если
                права ещё не назначались (``None`` — взять дефолт цели); ``throw_ac_exception``
                — при ``True`` сервер бросит 403 вместо ответа ``False``.

        Returns:
            ``True``, если право есть; ``False`` — если нет (и ``throw_ac_exception`` —
            ``False``). При пустом теле ответа возвращается ``False`` (fail-closed).

        Raises:
            IPSError: При ошибочном ответе сервера; в т.ч. 403, если ``throw_ac_exception``
                — ``True`` и прав нет; 404, если версия не найдена.

        Example:
            from aioips.schemas.security import SecurityCheckAccess

            async with IPSClient(config=config) as ips:
                can_edit = await ips.check_object_security_access(
                    204931, SecurityCheckAccess(action_type="edit")
                )  # 204931 = id версии объекта

        Notes:
            operationId ``Security_CheckObjectSecurityAccess``; путь
            ``POST /core/api/security/objects/{objectVersionId}/checkAccess``
            (``CheckAccessDto``). Связанный read-снимок: :meth:`object_security`.
        """
        body = check.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request(
            "post", f"/core/api/security/objects/{object_version_id}/checkAccess", json=body
        )
        return bool(data) if data is not None else False
