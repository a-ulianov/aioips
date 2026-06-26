"""Метод восстановления доступа администратора к правам цели безопасности (мутация)."""

from ...core import APIManager


class RestoreObjectTypeLifecycleSchemeStepForAttributeMixin(APIManager):
    """Реализует восстановление доступа администратора (``restoreAdminAccess``).

    Путь ``POST``:
    ``.../security/objectTypes/{objectTypeId}/lifecycleSchemeSteps/{lifecycleSchemeStepId}``
    ``attributes/{attributeId}/restoreAdminAccess``
    operationId ``Security_RestoreObjectTypeLifecycleSchemeStepSecurityForAttribute``.
    """

    async def restore_object_type_lifecycle_scheme_step_for_attribute(
        self: "RestoreObjectTypeLifecycleSchemeStepForAttributeMixin",
        object_type_id: int,
        lifecycle_scheme_step_id: int,
        attribute_id: int,
        *,
        confirm: bool = False,
    ) -> None:
        """Восстанавливает доступ администратора к правам цели безопасности (МУТАЦИЯ).

        ВОССТАНОВЛЕНИЕ доступа администратора (грант, НЕ отзыв): возвращает текущему
        пользователю-администратору гарантированный доступ к настройке прав указанной цели защиты,
        если он был случайно потерян (например, администратор сам себе запретил доступ и
        заблокировался). Сервер заново выдаёт администратору полные права на эту цель; чужие права
        при этом не отзываются. Применяйте как «аварийную кнопку» разблокировки управления
        безопасностью цели.

        Когда применять: после ошибочной настройки прав, из-за которой администратор утратил
        возможность редактировать безопасность тройки «тип объекта × шаг схемы ЖЦ × атрибут». Парный
        read для проверки текущего снимка прав —
        :meth:`object_type_lifecycle_step_attribute_security`.

        Защита: мутация защищена ``confirm`` — без ``confirm=True`` поднимается :class:`ValueError`
        ещё ДО обращения к серверу (запрос не выполняется). Тела у запроса нет: отправляется пустой
        JSON-объект ``{}`` (иначе сервер ответит 415).

        Args:
            object_type_id: Идентификатор ТИПА объекта (метаданное «тип объекта»), не
                объекта/версии.
            lifecycle_scheme_step_id: Идентификатор ШАГА схемы ЖЦ (``lifecycleSchemeStepId``), не
                схемы/уровня.
            attribute_id: Идентификатор АТРИБУТА (метаданное «атрибут»), не значения атрибута.
            confirm: Подтверждение мутирующей операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера (в т.ч. 403 при недостатке прав; 404, если цель
            не найдена).

        Example:
            async with IPSClient(config=config) as ips:
                await ips.restore_object_type_lifecycle_scheme_step_for_attribute(
                    1, 2, 3, confirm=True
                )

        Notes:
            operationId ``Security_RestoreObjectTypeLifecycleSchemeStepSecurityForAttribute``.
            Запрос без тела (``json={}``).
            Путь ``POST``:
            ``.../security/objectTypes/{objectTypeId}/lifecycleSchemeSteps/{lifecycleSchemeStepId}``
            ``attributes/{attributeId}/restoreAdminAccess``
            Парный read — :meth:`object_type_lifecycle_step_attribute_security`.
        """
        if confirm is not True:
            raise ValueError(
                "restore_object_type_lifecycle_scheme_step_for_attribute меняет права доступа; "
                "передайте confirm=True",
            )
        await self._request(
            "post",
            f"/core/api/security/objectTypes/{object_type_id}"
            f"/lifecycleSchemeSteps/{lifecycle_scheme_step_id}/attributes"
            f"/{attribute_id}/restoreAdminAccess",
            json={},
        )
        return None
