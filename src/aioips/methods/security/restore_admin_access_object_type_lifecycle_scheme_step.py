"""Метод восстановления доступа администратора к правам цели безопасности (мутация)."""

from ...core import APIManager


class RestoreAdminAccessObjectTypeLifecycleSchemeStepMixin(APIManager):
    """Реализует восстановление доступа администратора (``restoreAdminAccess``).

    Путь ``POST``:
    ``.../security/objectTypes/{objectTypeId}/lifecycleSchemeSteps/{lifecycleSchemeStepId}``
    ``restoreAdminAccess``
    operationId ``Security_RestoreAdminAccessObjectTypeLifecycleSchemeStepSecurity``.
    """

    async def restore_admin_access_object_type_lifecycle_scheme_step(
        self: "RestoreAdminAccessObjectTypeLifecycleSchemeStepMixin",
        object_type_id: int,
        lifecycle_scheme_step_id: int,
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
        возможность редактировать безопасность пары «тип объекта × шаг схемы ЖЦ». Парный read для
        проверки текущего снимка прав — :meth:`object_type_lifecycle_step_security`.

        Защита: мутация защищена ``confirm`` — без ``confirm=True`` поднимается :class:`ValueError`
        ещё ДО обращения к серверу (запрос не выполняется). Тела у запроса нет: отправляется пустой
        JSON-объект ``{}`` (иначе сервер ответит 415).

        Args:
            object_type_id: Идентификатор ТИПА объекта (метаданное «тип объекта»), не
                объекта/версии.
            lifecycle_scheme_step_id: Идентификатор ШАГА схемы ЖЦ (``lifecycleSchemeStepId``), не
                схемы/уровня.
            confirm: Подтверждение мутирующей операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера (в т.ч. 403 при недостатке прав; 404, если цель
            не найдена).

        Example:
            async with IPSClient(config=config) as ips:
                await ips.restore_admin_access_object_type_lifecycle_scheme_step(1, 2, confirm=True)

        Notes:
            operationId ``Security_RestoreAdminAccessObjectTypeLifecycleSchemeStepSecurity``. Запрос
            без тела (``json={}``).
            Путь ``POST``:
            ``.../security/objectTypes/{objectTypeId}/lifecycleSchemeSteps/{lifecycleSchemeStepId}``
            ``restoreAdminAccess``
            Парный read — :meth:`object_type_lifecycle_step_security`.
        """
        if confirm is not True:
            raise ValueError(
                "restore_admin_access_object_type_lifecycle_scheme_step меняет права доступа; "
                "передайте confirm=True",
            )
        await self._request(
            "post",
            f"/core/api/security/objectTypes/{object_type_id}"
            f"/lifecycleSchemeSteps/{lifecycle_scheme_step_id}"
            "/restoreAdminAccess",
            json={},
        )
        return None
