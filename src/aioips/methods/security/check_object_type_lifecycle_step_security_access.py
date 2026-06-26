"""Метод проверки доступа текущего пользователя к шагу схемы ЖЦ для типа объекта."""

from ...core import APIManager
from ...schemas.security import SecurityCheckAccess


class CheckObjectTypeLifecycleStepSecurityAccessMixin(APIManager):
    """Реализует POST ``.../objectTypes/{objectTypeId}/lifecycleSchemeSteps/{...}/checkAccess``.

    operationId ``Security_CheckUpdateObjectTypeLifecycleSchemeStepSecurityAccess``.
    """

    async def check_object_type_lifecycle_step_security_access(
        self: "CheckObjectTypeLifecycleStepSecurityAccessMixin",
        object_type_id: int,
        lifecycle_scheme_step_id: int,
        check: SecurityCheckAccess,
    ) -> bool:
        """Проверяет доступ текущего пользователя к шагу схемы ЖЦ для типа объекта.

        READ-проверка прав (ничего не меняет): есть ли у текущего пользователя право
        ``check.action_type`` на конкретный шаг схемы жизненного цикла
        (``lifecycle_scheme_step_id``) в контексте типа объекта (``object_type_id``).
        Например, право выполнить переход/действие на данном шаге ЖЦ для объектов этого типа.

        Когда применять: до показа кнопки перехода ЖЦ или операции, привязанной к шагу
        схемы, — убедиться, что пользователь вправе её выполнить. Для проверки доступа к
        конкретному АТРИБУТУ на этом шаге используйте
        :meth:`check_object_type_lifecycle_step_attribute_security_access`.

        Args:
            object_type_id: Идентификатор типа объекта (контекст шага ЖЦ).
            lifecycle_scheme_step_id: Идентификатор шага схемы жизненного цикла (цель защиты).
            check: Параметры проверки (:class:`SecurityCheckAccess`): ``action_type`` —
                проверяемое право (``ActionType``); ``default_access`` — что вернуть, если
                права ещё не назначались (``None`` — взять дефолт цели); ``throw_ac_exception``
                — при ``True`` сервер бросит 403 вместо ответа ``False``.

        Returns:
            ``True``, если право есть; ``False`` — если нет (и ``throw_ac_exception`` —
            ``False``). При пустом теле ответа возвращается ``False`` (fail-closed).

        Raises:
            IPSError: При ошибочном ответе сервера; в т.ч. 403, если ``throw_ac_exception``
                — ``True`` и прав нет; 404, если тип или шаг не найдены.

        Example:
            from aioips.schemas.security import SecurityCheckAccess

            async with IPSClient(config=config) as ips:
                allowed = await ips.check_object_type_lifecycle_step_security_access(
                    1031, 5, SecurityCheckAccess(action_type="nextLCStep")
                )

        Notes:
            operationId ``Security_CheckUpdateObjectTypeLifecycleSchemeStepSecurityAccess``;
            путь ``POST /core/api/security/objectTypes/{objectTypeId}/lifecycleSchemeSteps/
            {lifecycleSchemeStepId}/checkAccess`` (``CheckAccessDto``). Связанный метод:
            :meth:`check_object_type_lifecycle_step_attribute_security_access`.
        """
        body = check.model_dump(mode="json", by_alias=True, exclude_none=True)
        path = (
            f"/core/api/security/objectTypes/{object_type_id}"
            f"/lifecycleSchemeSteps/{lifecycle_scheme_step_id}/checkAccess"
        )
        data = await self._request("post", path, json=body)
        return bool(data) if data is not None else False
