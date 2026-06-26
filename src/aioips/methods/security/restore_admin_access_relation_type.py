"""Метод восстановления доступа администратора к правам цели безопасности (мутация)."""

from ...core import APIManager


class RestoreAdminAccessRelationTypeMixin(APIManager):
    """Реализует восстановление доступа администратора (``restoreAdminAccess``).

    Путь ``POST``:
    ``.../security/relationTypes/{relationTypeId}/restoreAdminAccess``
    operationId ``Security_RestoreAdminAccessRelationTypeSecurity``.
    """

    async def restore_admin_access_relation_type(
        self: "RestoreAdminAccessRelationTypeMixin",
        relation_type_id: int,
        *,
        confirm: bool = False,
    ) -> None:
        """Восстанавливает доступ администратора к правам конкретного типа связи (МУТАЦИЯ).

        ВОССТАНОВЛЕНИЕ доступа администратора (грант, НЕ отзыв): возвращает текущему
        пользователю-администратору гарантированный доступ к настройке прав указанной цели защиты,
        если он был случайно потерян (например, администратор сам себе запретил доступ и
        заблокировался). Сервер заново выдаёт администратору полные права на эту цель; чужие права
        при этом не отзываются. Применяйте как «аварийную кнопку» разблокировки управления
        безопасностью цели.

        Когда применять: после ошибочной настройки прав, из-за которой администратор утратил
        возможность редактировать безопасность конкретного типа связи. Парный read для проверки
        текущего снимка прав — :meth:`relation_type_security`.

        Защита: мутация защищена ``confirm`` — без ``confirm=True`` поднимается :class:`ValueError`
        ещё ДО обращения к серверу (запрос не выполняется). Тела у запроса нет: отправляется пустой
        JSON-объект ``{}`` (иначе сервер ответит 415).

        Args:
            relation_type_id: Идентификатор ТИПА связи (метаданное «тип связи»).
            confirm: Подтверждение мутирующей операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера (в т.ч. 403 при недостатке прав; 404, если цель
            не найдена).

        Example:
            async with IPSClient(config=config) as ips:
                await ips.restore_admin_access_relation_type(1, confirm=True)

        Notes:
            operationId ``Security_RestoreAdminAccessRelationTypeSecurity``. Запрос без тела
            (``json={}``).
            Путь ``POST``:
            ``.../security/relationTypes/{relationTypeId}/restoreAdminAccess``
            Парный read — :meth:`relation_type_security`.
        """
        if confirm is not True:
            raise ValueError(
                "restore_admin_access_relation_type меняет права доступа; передайте confirm=True",
            )
        await self._request(
            "post",
            f"/core/api/security/relationTypes/{relation_type_id}/restoreAdminAccess",
            json={},
        )
        return None
