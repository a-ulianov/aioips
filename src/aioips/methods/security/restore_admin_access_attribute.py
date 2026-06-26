"""Метод восстановления доступа администратора к правам цели безопасности (мутация)."""

from ...core import APIManager


class RestoreAdminAccessAttributeMixin(APIManager):
    """Реализует восстановление доступа администратора (``restoreAdminAccess``).

    Путь ``POST``:
    ``.../security/attributes/{attributeId}/restoreAdminAccess``
    operationId ``Security_RestoreAdminAccessAttributeSecurity``.
    """

    async def restore_admin_access_attribute(
        self: "RestoreAdminAccessAttributeMixin",
        attribute_id: int,
        *,
        confirm: bool = False,
    ) -> None:
        """Восстанавливает доступ администратора к правам конкретного атрибута (МУТАЦИЯ).

        ВОССТАНОВЛЕНИЕ доступа администратора (грант, НЕ отзыв): возвращает текущему
        пользователю-администратору гарантированный доступ к настройке прав указанной цели защиты,
        если он был случайно потерян (например, администратор сам себе запретил доступ и
        заблокировался). Сервер заново выдаёт администратору полные права на эту цель; чужие права
        при этом не отзываются. Применяйте как «аварийную кнопку» разблокировки управления
        безопасностью цели.

        Когда применять: после ошибочной настройки прав, из-за которой администратор утратил
        возможность редактировать безопасность конкретного атрибута. Парный read для проверки
        текущего снимка прав — :meth:`attribute_security`.

        Защита: мутация защищена ``confirm`` — без ``confirm=True`` поднимается :class:`ValueError`
        ещё ДО обращения к серверу (запрос не выполняется). Тела у запроса нет: отправляется пустой
        JSON-объект ``{}`` (иначе сервер ответит 415).

        Args:
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
                await ips.restore_admin_access_attribute(1, confirm=True)

        Notes:
            operationId ``Security_RestoreAdminAccessAttributeSecurity``. Запрос без тела
            (``json={}``).
            Путь ``POST``:
            ``.../security/attributes/{attributeId}/restoreAdminAccess``
            Парный read — :meth:`attribute_security`.
        """
        if confirm is not True:
            raise ValueError(
                "restore_admin_access_attribute меняет права доступа; передайте confirm=True",
            )
        await self._request(
            "post",
            f"/core/api/security/attributes/{attribute_id}/restoreAdminAccess",
            json={},
        )
        return None
