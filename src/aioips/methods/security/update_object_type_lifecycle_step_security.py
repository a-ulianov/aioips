"""Метод записи прав доступа на шаг схемы ЖЦ типа объекта (мутация)."""

from typing import Any

from ...core import APIManager
from ...schemas.security import Security


class UpdateObjectTypeLifecycleSchemeStepSecurityMixin(APIManager):
    """Реализует запись прав на шаг схемы ЖЦ типа объекта.

    Путь ``POST``:
    ``.../security/objectTypes/{objectTypeId}/lifecycleSchemeSteps``
    ``/{lifecycleSchemeStepId}``
    operationId ``Security_UpdateObjectTypeLifecycleSchemeStepSecurity``.
    """

    async def update_object_type_lifecycle_scheme_step_security(
        self: "UpdateObjectTypeLifecycleSchemeStepSecurityMixin",
        object_type_id: int,
        lifecycle_scheme_step_id: int,
        body: Security | dict[str, Any],
        *,
        confirm: bool = False,
    ) -> None:
        """Записывает права доступа на ШАГ схемы ЖЦ типа объекта (МУТАЦИЯ).

        УСТАНОВКА прав (перезапись): задаёт, кто и какие действия может выполнять с
        объектами типа ``object_type_id`` на шаге ЖЦ ``lifecycle_scheme_step_id``. Это
        опасная операция — меняет реальные права доступа, а не читает их. Парная запись к
        read-методу :meth:`object_type_lifecycle_step_security`.

        Тело: на стороне сервера это ``SecurityWithChildsSettingsDto`` — расширение снимка
        прав полем ``isNeedToApplyToChilds`` (применять ли настройки к дочерним шагам).
        :class:`Security` этого поля НЕ содержит, поэтому: для простой записи передавайте
        :class:`Security`; чтобы задать ``isNeedToApplyToChilds`` — передавайте ``dict`` с
        этим ключом (плюс ``targets`` / ``actions`` / ``permissions`` / ``durations`` /
        ``conditions`` / ``isConditionsEnabled``).

        Когда применять: чтобы настроить безопасность объектов типа на конкретном шаге ЖЦ.
        Перед мутацией стоит проверить право методом
        :meth:`check_update_object_type_lifecycle_scheme_step_access`.

        Обратимость: операция ОБРАТИМА по схеме write-same-back. Перед записью прочитайте
        текущее состояние парным :meth:`object_type_lifecycle_step_security` и сохраните
        его; для отката запишите тот же снимок обратно. Тест отката: прочитать → записать
        тот же объект обратно — состояние не меняется.

        Защита: мутация защищена ``confirm`` — без ``confirm=True`` поднимается
        :class:`ValueError` ещё ДО обращения к серверу (запрос не выполняется).

        Args:
            object_type_id: Идентификатор ТИПА объекта (метаданное «тип объекта»), не
                объекта/версии.
            lifecycle_scheme_step_id: Идентификатор ШАГА схемы ЖЦ
                (``lifecycleSchemeStepId``), не схемы и не уровня.
            body: Снимок прав (:class:`Security` или ``dict`` по
                ``SecurityWithChildsSettingsDto``). Для round-trip передавайте «сырой»
                результат :meth:`object_type_lifecycle_step_security`. Модель сериализуется
                ``by_alias`` + ``exclude_none``; ``dict`` уходит как есть.
            confirm: Подтверждение мутирующей операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера (в т.ч. 403 при недостатке прав; 404,
                если тип или шаг не найден).

        Example:
            async with IPSClient(config=config) as ips:
                current = await ips.object_type_lifecycle_step_security(1031, 5)  # бэкап
                await ips.update_object_type_lifecycle_scheme_step_security(
                    1031, 5, current, confirm=True
                )

        Notes:
            operationId ``Security_UpdateObjectTypeLifecycleSchemeStepSecurity``; тело —
            ``SecurityWithChildsSettingsDto``. Путь ``POST``:
            ``.../security/objectTypes/{objectTypeId}/lifecycleSchemeSteps``
            ``/{lifecycleSchemeStepId}``.
            Парный read — :meth:`object_type_lifecycle_step_security`.
        """
        if confirm is not True:
            raise ValueError(
                "update_object_type_lifecycle_scheme_step_security меняет права доступа; "
                "передайте confirm=True",
            )
        payload = (
            body.model_dump(mode="json", by_alias=True, exclude_none=True)
            if isinstance(body, Security)
            else body
        )
        await self._request(
            "post",
            f"/core/api/security/objectTypes/{object_type_id}/lifecycleSchemeSteps"
            f"/{lifecycle_scheme_step_id}",
            json=payload,
        )
        return None
