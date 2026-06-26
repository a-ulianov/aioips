"""Метод проверки доступа к настройке прав шага схемы ЖЦ типа объекта (checkAccess)."""

from ...core import APIManager
from ...schemas.security import SecurityCheckAccess


class CheckUpdateObjectTypeLifecycleSchemeStepAccessMixin(APIManager):
    """Реализует проверку доступа к настройке прав шага схемы ЖЦ (``checkAccess``).

    Путь ``POST``:
    ``.../security/objectTypes/{objectTypeId}/lifecycleSchemeSteps``
    ``/{lifecycleSchemeStepId}/checkAccess``
    operationId ``Security_CheckUpdateObjectTypeLifecycleSchemeStepSecurityAccess``.
    """

    async def check_update_object_type_lifecycle_scheme_step_access(
        self: "CheckUpdateObjectTypeLifecycleSchemeStepAccessMixin",
        object_type_id: int,
        lifecycle_scheme_step_id: int,
        check: SecurityCheckAccess,
    ) -> bool:
        """Проверяет доступ к ШАГУ схемы ЖЦ типа объекта (право настраивать его права).

        READ-проверка прав (ничего не меняет): есть ли у текущего пользователя право
        ``check.action_type`` для пары «тип объекта ``object_type_id`` × шаг ЖЦ
        ``lifecycle_scheme_step_id``» — в частности, право изменять настройки безопасности
        этого шага (``setAccess``). Это контекстно-зависимая проверка на уровне шага ЖЦ
        целиком, а не отдельного атрибута.

        Когда применять: до показа кнопки «Настроить права» для шага ЖЦ или перед попыткой
        мутации :meth:`update_object_type_lifecycle_scheme_step_security` — убедиться, что
        пользователь вправе менять эти настройки. Для проверки права на отдельный атрибут
        на этом шаге — :meth:`check_object_type_lifecycle_scheme_step_access_for_attribute`.
        Полный read-снимок прав шага — :meth:`object_type_lifecycle_step_security`.

        Args:
            object_type_id: Идентификатор ТИПА объекта (метаданное «тип объекта»), не
                объекта/версии.
            lifecycle_scheme_step_id: Идентификатор ШАГА схемы ЖЦ
                (``lifecycleSchemeStepId``), не схемы и не уровня.
            check: Параметры проверки (:class:`SecurityCheckAccess`): ``action_type`` —
                проверяемое право (``ActionType``, напр. ``setAccess``); ``default_access`` —
                что вернуть, если права ещё не назначались (``None`` — взять дефолт цели);
                ``throw_ac_exception`` — при ``True`` сервер бросит 403 вместо ответа ``False``.

        Returns:
            ``True``, если право есть; ``False`` — если нет (и ``throw_ac_exception`` —
            ``False``). При пустом/``null`` теле ответа возвращается ``False`` (fail-closed).

        Raises:
            IPSError: При ошибочном ответе сервера; в т.ч. 403, если ``throw_ac_exception``
                — ``True`` и прав нет; 404, если тип или шаг не найден.

        Example:
            from aioips.schemas.security import SecurityCheckAccess

            async with IPSClient(config=config) as ips:
                allowed = await ips.check_update_object_type_lifecycle_scheme_step_access(
                    1031, 5, SecurityCheckAccess(action_type="setAccess")
                )

        Notes:
            operationId ``Security_CheckUpdateObjectTypeLifecycleSchemeStepSecurityAccess``;
            тело — ``CheckAccessDto``. Путь ``POST``:
            ``.../security/objectTypes/{objectTypeId}/lifecycleSchemeSteps``
            ``/{lifecycleSchemeStepId}/checkAccess``.
            Парная мутация: :meth:`update_object_type_lifecycle_scheme_step_security`.
        """
        body = check.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request(
            "post",
            f"/core/api/security/objectTypes/{object_type_id}/lifecycleSchemeSteps"
            f"/{lifecycle_scheme_step_id}/checkAccess",
            json=body,
        )
        return bool(data) if data is not None else False
