"""Метод восстановления доступа администратора к правам цели безопасности (мутация)."""

from ...core import APIManager


class RestoreAdminAccessObjectMixin(APIManager):
    """Реализует восстановление доступа администратора (``restoreAdminAccess``).

    Путь ``POST``:
    ``.../security/objects/{objectVersionId}/restoreAdminAccess``
    operationId ``Security_RestoreAdminAccessObjectSecurity``.
    """

    async def restore_admin_access_object(
        self: "RestoreAdminAccessObjectMixin",
        object_version_id: int,
        *,
        confirm: bool = False,
    ) -> None:
        """Восстанавливает доступ администратора к правам конкретного объекта (версии) (МУТАЦИЯ).

        ВОССТАНОВЛЕНИЕ доступа администратора (грант, НЕ отзыв): возвращает текущему
        пользователю-администратору гарантированный доступ к настройке прав указанной цели защиты,
        если он был случайно потерян (например, администратор сам себе запретил доступ и
        заблокировался). Сервер заново выдаёт администратору полные права на эту цель; чужие права
        при этом не отзываются. Применяйте как «аварийную кнопку» разблокировки управления
        безопасностью цели.

        Когда применять: после ошибочной настройки прав, из-за которой администратор утратил
        возможность редактировать безопасность конкретного объекта (версии). Парный read для
        проверки текущего снимка прав — :meth:`object_security`.

        Защита: мутация защищена ``confirm`` — без ``confirm=True`` поднимается :class:`ValueError`
        ещё ДО обращения к серверу (запрос не выполняется). Тела у запроса нет: отправляется пустой
        JSON-объект ``{}`` (иначе сервер ответит 415).

        Args:
            object_version_id: Идентификатор ВЕРСИИ объекта (``objectVersionId`` = ``id`` версии).
            confirm: Подтверждение мутирующей операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера (в т.ч. 403 при недостатке прав; 404, если цель
            не найдена).

        Example:
            async with IPSClient(config=config) as ips:
                await ips.restore_admin_access_object(1, confirm=True)

        Notes:
            operationId ``Security_RestoreAdminAccessObjectSecurity``. Запрос без тела
            (``json={}``).
            Путь ``POST``:
            ``.../security/objects/{objectVersionId}/restoreAdminAccess``
            Парный read — :meth:`object_security`.
        """
        if confirm is not True:
            raise ValueError(
                "restore_admin_access_object меняет права доступа; передайте confirm=True",
            )
        await self._request(
            "post",
            f"/core/api/security/objects/{object_version_id}/restoreAdminAccess",
            json={},
        )
        return None
