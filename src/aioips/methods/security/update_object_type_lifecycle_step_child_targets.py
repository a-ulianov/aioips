"""Метод обновления прав дочерних целей безопасности шага схемы ЖЦ типа объекта (мутация)."""

from typing import Any

from ...core import APIManager
from ...schemas.security import Security


class UpdateObjectTypeLifecycleSchemeStepChildTargetsMixin(APIManager):
    """Реализует обновление прав дочерних целей шага схемы ЖЦ типа объекта.

    Путь ``POST``:
    ``.../security/objectTypes/{objectTypeId}/lifecycleSchemeSteps``
    ``/{lifecycleSchemeStepId}/childTargets``
    operationId ``Security_UpdateObjectTypeLifecycleSchemeStepSecurityChildTargets``.
    """

    async def update_object_type_lifecycle_scheme_step_child_targets(
        self: "UpdateObjectTypeLifecycleSchemeStepChildTargetsMixin",
        object_type_id: int,
        lifecycle_scheme_step_id: int,
        body: Security | dict[str, Any],
        *,
        confirm: bool = False,
    ) -> None:
        """Записывает права ДОЧЕРНИХ целей для ШАГА схемы ЖЦ типа объекта (МУТАЦИЯ).

        УСТАНОВКА прав (перезапись): распространяет/обновляет настройки безопасности для
        дочерних целей (наследников) на шаге ЖЦ ``lifecycle_scheme_step_id`` типа
        ``object_type_id``. Это опасная операция — меняет реальные права доступа, а не
        читает их. Тело — снимок прав :class:`Security` (``SecurityDto``).

        Когда применять: чтобы выровнять права наследуемых целей в узком контексте «тип
        объекта × шаг ЖЦ». Полный read-снимок прав шага —
        :meth:`object_type_lifecycle_step_security`.

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
            body: Снимок прав (:class:`Security` или эквивалентный ``dict``,
                ``SecurityDto``). Для round-trip передавайте «сырой» результат
                :meth:`object_type_lifecycle_step_security`. Модель сериализуется
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
                await ips.update_object_type_lifecycle_scheme_step_child_targets(
                    1031, 5, current, confirm=True
                )

        Notes:
            operationId
            ``Security_UpdateObjectTypeLifecycleSchemeStepSecurityChildTargets``; тело —
            ``SecurityDto``. Путь ``POST``:
            ``.../security/objectTypes/{objectTypeId}/lifecycleSchemeSteps``
            ``/{lifecycleSchemeStepId}/childTargets``.
            Парный read — :meth:`object_type_lifecycle_step_security`.
        """
        if confirm is not True:
            raise ValueError(
                "update_object_type_lifecycle_scheme_step_child_targets "
                "меняет права доступа; передайте confirm=True",
            )
        payload = (
            body.model_dump(mode="json", by_alias=True, exclude_none=True)
            if isinstance(body, Security)
            else body
        )
        await self._request(
            "post",
            f"/core/api/security/objectTypes/{object_type_id}/lifecycleSchemeSteps"
            f"/{lifecycle_scheme_step_id}/childTargets",
            json=payload,
        )
        return None
