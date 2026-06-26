"""Метод восстановления доступа администратора к правам цели безопасности (мутация)."""

from ...core import APIManager


class RestoreAdminAccessLifecycleSchemeMixin(APIManager):
    """Реализует восстановление доступа администратора (``restoreAdminAccess``).

    Путь ``POST``:
    ``.../security/lifecycleSchemes/{lifecycleSchemeId}/restoreAdminAccess``
    operationId ``Security_RestoreAdminAccessLifecycleSchemeSecurity``.
    """

    async def restore_admin_access_lifecycle_scheme(
        self: "RestoreAdminAccessLifecycleSchemeMixin",
        lifecycle_scheme_id: int,
        *,
        confirm: bool = False,
    ) -> None:
        """Восстанавливает доступ администратора к правам конкретной схемы ЖЦ (МУТАЦИЯ).

        ВОССТАНОВЛЕНИЕ доступа администратора (грант, НЕ отзыв): возвращает текущему
        пользователю-администратору гарантированный доступ к настройке прав указанной цели защиты,
        если он был случайно потерян (например, администратор сам себе запретил доступ и
        заблокировался). Сервер заново выдаёт администратору полные права на эту цель; чужие права
        при этом не отзываются. Применяйте как «аварийную кнопку» разблокировки управления
        безопасностью цели.

        Когда применять: после ошибочной настройки прав, из-за которой администратор утратил
        возможность редактировать безопасность конкретной схемы ЖЦ. Парный read для проверки
        текущего снимка прав — :meth:`lifecycle_scheme_security`.

        Защита: мутация защищена ``confirm`` — без ``confirm=True`` поднимается :class:`ValueError`
        ещё ДО обращения к серверу (запрос не выполняется). Тела у запроса нет: отправляется пустой
        JSON-объект ``{}`` (иначе сервер ответит 415).

        Args:
            lifecycle_scheme_id: Идентификатор СХЕМЫ ЖЦ (``lifecycleSchemeId``), не шага и не
                уровня.
            confirm: Подтверждение мутирующей операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера (в т.ч. 403 при недостатке прав; 404, если цель
            не найдена).

        Example:
            async with IPSClient(config=config) as ips:
                await ips.restore_admin_access_lifecycle_scheme(1, confirm=True)

        Notes:
            operationId ``Security_RestoreAdminAccessLifecycleSchemeSecurity``. Запрос без тела
            (``json={}``).
            Путь ``POST``:
            ``.../security/lifecycleSchemes/{lifecycleSchemeId}/restoreAdminAccess``
            Парный read — :meth:`lifecycle_scheme_security`.
        """
        if confirm is not True:
            raise ValueError(
                "restore_admin_access_lifecycle_scheme меняет права доступа; "
                "передайте confirm=True",
            )
        await self._request(
            "post",
            f"/core/api/security/lifecycleSchemes/{lifecycle_scheme_id}/restoreAdminAccess",
            json={},
        )
        return None
