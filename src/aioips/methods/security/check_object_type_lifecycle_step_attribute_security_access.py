"""Метод проверки доступа к атрибуту на шаге схемы ЖЦ для типа объекта."""

from ...core import APIManager
from ...schemas.security import SecurityCheckAccess


class CheckObjectTypeLifecycleStepAttributeSecurityAccessMixin(APIManager):
    """Реализует POST ``.../lifecycleSchemeSteps/{...}/attributes/{attributeId}/checkAccess``.

    operationId ``Security_CheckObjectTypeLifecycleSchemeStepSecurityAccessForAttribute``.
    """

    async def check_object_type_lifecycle_step_attribute_security_access(
        self: "CheckObjectTypeLifecycleStepAttributeSecurityAccessMixin",
        object_type_id: int,
        lifecycle_scheme_step_id: int,
        attribute_id: int,
        check: SecurityCheckAccess,
    ) -> bool:
        """Проверяет доступ к атрибуту на конкретном шаге схемы ЖЦ для типа объекта.

        READ-проверка прав (ничего не меняет): есть ли у текущего пользователя право
        ``check.action_type`` на атрибут ``attribute_id`` в контексте конкретного шага
        схемы жизненного цикла (``lifecycle_scheme_step_id``) для типа объекта
        (``object_type_id``). Самая узкая проверка: право на атрибут зависит и от типа, и
        от текущего шага ЖЦ (на разных шагах атрибут может быть редактируем или нет).

        Когда применять: при построении формы редактирования — определить, можно ли
        читать/менять конкретный атрибут на текущем шаге ЖЦ объекта данного типа. Для шага
        в целом (без привязки к атрибуту) используйте
        :meth:`check_object_type_lifecycle_step_security_access`.

        Args:
            object_type_id: Идентификатор типа объекта (контекст).
            lifecycle_scheme_step_id: Идентификатор шага схемы жизненного цикла (контекст).
            attribute_id: Идентификатор типа атрибута (цель защиты).
            check: Параметры проверки (:class:`SecurityCheckAccess`): ``action_type`` —
                проверяемое право (``ActionType``, напр. ``edit``); ``default_access`` —
                что вернуть, если права ещё не назначались (``None`` — взять дефолт цели);
                ``throw_ac_exception`` — при ``True`` сервер бросит 403 вместо ответа ``False``.

        Returns:
            ``True``, если право есть; ``False`` — если нет (и ``throw_ac_exception`` —
            ``False``). При пустом теле ответа возвращается ``False`` (fail-closed).

        Raises:
            IPSError: При ошибочном ответе сервера; в т.ч. 403, если ``throw_ac_exception``
                — ``True`` и прав нет; 404, если тип, шаг или атрибут не найдены.

        Example:
            from aioips.schemas.security import SecurityCheckAccess

            async with IPSClient(config=config) as ips:
                allowed = await (
                    ips.check_object_type_lifecycle_step_attribute_security_access(
                        1031, 5, 1029, SecurityCheckAccess(action_type="edit")
                    )
                )

        Notes:
            operationId
            ``Security_CheckObjectTypeLifecycleSchemeStepSecurityAccessForAttribute``;
            путь ``POST /core/api/security/objectTypes/{objectTypeId}/lifecycleSchemeSteps/
            {lifecycleSchemeStepId}/attributes/{attributeId}/checkAccess`` (``CheckAccessDto``).
        """
        body = check.model_dump(mode="json", by_alias=True, exclude_none=True)
        path = (
            f"/core/api/security/objectTypes/{object_type_id}"
            f"/lifecycleSchemeSteps/{lifecycle_scheme_step_id}"
            f"/attributes/{attribute_id}/checkAccess"
        )
        data = await self._request("post", path, json=body)
        return bool(data) if data is not None else False
