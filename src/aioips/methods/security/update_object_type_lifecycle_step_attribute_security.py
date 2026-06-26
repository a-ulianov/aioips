"""Метод записи прав на атрибут на шаге схемы ЖЦ типа объекта (мутация)."""

from typing import Any

from ...core import APIManager
from ...schemas.security import Security


class UpdateObjectTypeLifecycleSchemeStepSecurityForAttributeMixin(APIManager):
    """Реализует запись прав на атрибут на шаге схемы ЖЦ типа объекта.

    Путь ``POST``:
    ``.../security/objectTypes/{objectTypeId}/lifecycleSchemeSteps``
    ``/{lifecycleSchemeStepId}/attributes/{attributeId}``
    operationId ``Security_UpdateObjectTypeLifecycleSchemeStepSecurityForAttribute``.
    """

    async def update_object_type_lifecycle_scheme_step_security_for_attribute(
        self: "UpdateObjectTypeLifecycleSchemeStepSecurityForAttributeMixin",
        object_type_id: int,
        lifecycle_scheme_step_id: int,
        attribute_id: int,
        body: Security | dict[str, Any],
        *,
        confirm: bool = False,
    ) -> None:
        """Записывает права на АТРИБУТ типа объекта на конкретном шаге схемы ЖЦ (МУТАЦИЯ).

        УСТАНОВКА прав (перезапись): задаёт, кто может видеть/менять атрибут ``attribute_id``
        объектов типа ``object_type_id`` на шаге ЖЦ ``lifecycle_scheme_step_id``. Самый
        узкий слой полевой защиты. Это опасная операция — меняет реальные права доступа, а
        не читает их. Парная запись к read-методу
        :meth:`object_type_lifecycle_step_attribute_security`.

        Когда применять: чтобы сделать атрибут редактируемым/защищённым на конкретном шаге
        ЖЦ для конкретного типа. Перед мутацией право можно проверить методом
        :meth:`check_object_type_lifecycle_scheme_step_access_for_attribute`.

        Обратимость: операция ОБРАТИМА по схеме write-same-back. Перед записью прочитайте
        текущее состояние парным :meth:`object_type_lifecycle_step_attribute_security` и
        сохраните его; для отката запишите тот же снимок обратно. Тест отката: прочитать →
        записать тот же объект обратно — состояние не меняется.

        Защита: мутация защищена ``confirm`` — без ``confirm=True`` поднимается
        :class:`ValueError` ещё ДО обращения к серверу (запрос не выполняется).

        Args:
            object_type_id: Идентификатор ТИПА объекта (метаданное «тип объекта»), не
                объекта/версии.
            lifecycle_scheme_step_id: Идентификатор ШАГА схемы ЖЦ
                (``lifecycleSchemeStepId``), не схемы и не уровня.
            attribute_id: Идентификатор АТРИБУТА (метаданное «атрибут»), не значения атрибута.
            body: Снимок прав (:class:`Security` или эквивалентный ``dict``,
                ``SecurityDto``). Для round-trip передавайте «сырой» результат
                :meth:`object_type_lifecycle_step_attribute_security`. Модель сериализуется
                ``by_alias`` + ``exclude_none``; ``dict`` уходит как есть.
            confirm: Подтверждение мутирующей операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера (в т.ч. 403 при недостатке прав; 404,
                если тип, шаг или атрибут не найден).

        Example:
            async with IPSClient(config=config) as ips:
                current = await ips.object_type_lifecycle_step_attribute_security(1031, 5, 1029)
                await ips.update_object_type_lifecycle_scheme_step_security_for_attribute(
                    1031, 5, 1029, current, confirm=True
                )

        Notes:
            operationId
            ``Security_UpdateObjectTypeLifecycleSchemeStepSecurityForAttribute``; тело —
            ``SecurityDto``. Путь ``POST``:
            ``.../security/objectTypes/{objectTypeId}/lifecycleSchemeSteps``
            ``/{lifecycleSchemeStepId}/attributes/{attributeId}``.
            Парный read — :meth:`object_type_lifecycle_step_attribute_security`.
        """
        if confirm is not True:
            raise ValueError(
                "update_object_type_lifecycle_scheme_step_security_for_attribute "
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
            f"/{lifecycle_scheme_step_id}/attributes/{attribute_id}",
            json=payload,
        )
        return None
