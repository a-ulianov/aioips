"""Метод проверки доступа к атрибуту на шаге схемы ЖЦ типа объекта (checkAccess)."""

from ...core import APIManager
from ...schemas.security import SecurityCheckAccess


class CheckObjectTypeLifecycleSchemeStepAccessForAttributeMixin(APIManager):
    """Реализует проверку доступа к атрибуту на шаге схемы ЖЦ (``checkAccess``).

    Путь ``POST``:
    ``.../security/objectTypes/{objectTypeId}/lifecycleSchemeSteps``
    ``/{lifecycleSchemeStepId}/attributes/{attributeId}/checkAccess``
    operationId ``Security_CheckObjectTypeLifecycleSchemeStepSecurityAccessForAttribute``.
    """

    async def check_object_type_lifecycle_scheme_step_access_for_attribute(
        self: "CheckObjectTypeLifecycleSchemeStepAccessForAttributeMixin",
        object_type_id: int,
        lifecycle_scheme_step_id: int,
        attribute_id: int,
        check: SecurityCheckAccess,
    ) -> bool:
        """Проверяет доступ к АТРИБУТУ типа объекта на конкретном шаге схемы ЖЦ.

        READ-проверка прав (ничего не меняет): есть ли у текущего пользователя право
        ``check.action_type`` (например, ``read`` / ``edit``) на атрибут ``attribute_id``
        объектов типа ``object_type_id``, когда они находятся на шаге ЖЦ
        ``lifecycle_scheme_step_id``. Самый узкий, контекстно-зависимый слой полевой защиты:
        атрибут может быть редактируемым на одном шаге ЖЦ и защищён на другом.

        Когда применять: до показа поля атрибута редактируемым/скрытым в карточке объекта на
        конкретном шаге ЖЦ. Полный read-снимок этих прав даёт
        :meth:`object_type_lifecycle_step_attribute_security`. Для проверки доступа к шагу в
        целом (а не к отдельному атрибуту) используйте
        :meth:`check_update_object_type_lifecycle_scheme_step_access`.

        Args:
            object_type_id: Идентификатор ТИПА объекта (метаданное «тип объекта»), не
                объекта/версии.
            lifecycle_scheme_step_id: Идентификатор ШАГА схемы ЖЦ
                (``lifecycleSchemeStepId``), не схемы и не уровня.
            attribute_id: Идентификатор АТРИБУТА (метаданное «атрибут»), не значения атрибута.
            check: Параметры проверки (:class:`SecurityCheckAccess`): ``action_type`` —
                проверяемое право (``ActionType``); ``default_access`` — что вернуть, если
                права ещё не назначались (``None`` — взять дефолт цели); ``throw_ac_exception``
                — при ``True`` сервер бросит 403 вместо ответа ``False``.

        Returns:
            ``True``, если право есть; ``False`` — если нет (и ``throw_ac_exception`` —
            ``False``). При пустом/``null`` теле ответа возвращается ``False`` (fail-closed).

        Raises:
            IPSError: При ошибочном ответе сервера; в т.ч. 403, если ``throw_ac_exception``
                — ``True`` и прав нет; 404, если тип, шаг или атрибут не найден.

        Example:
            from aioips.schemas.security import SecurityCheckAccess

            async with IPSClient(config=config) as ips:
                allowed = await ips.check_object_type_lifecycle_scheme_step_access_for_attribute(
                    1031, 5, 1029, SecurityCheckAccess(action_type="edit")
                )

        Notes:
            operationId
            ``Security_CheckObjectTypeLifecycleSchemeStepSecurityAccessForAttribute``;
            тело — ``CheckAccessDto``. Путь ``POST``:
            ``.../security/objectTypes/{objectTypeId}/lifecycleSchemeSteps``
            ``/{lifecycleSchemeStepId}/attributes/{attributeId}/checkAccess``.
            Связанный read-снимок: :meth:`object_type_lifecycle_step_attribute_security`.
        """
        body = check.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request(
            "post",
            f"/core/api/security/objectTypes/{object_type_id}/lifecycleSchemeSteps"
            f"/{lifecycle_scheme_step_id}/attributes/{attribute_id}/checkAccess",
            json=body,
        )
        return bool(data) if data is not None else False
