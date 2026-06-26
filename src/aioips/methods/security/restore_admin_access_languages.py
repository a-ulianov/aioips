"""Метод восстановления доступа администратора к правам цели безопасности (мутация)."""

from ...core import APIManager


class RestoreAdminAccessLanguagesMixin(APIManager):
    """Реализует восстановление доступа администратора (``restoreAdminAccess``).

    Путь ``POST``:
    ``.../security/languages/restoreAdminAccess``
    operationId ``Security_RestoreAdminAccessLanguageCollectionSecurity``.
    """

    async def restore_admin_access_languages(
        self: "RestoreAdminAccessLanguagesMixin",
        *,
        confirm: bool = False,
    ) -> None:
        """Восстанавливает доступ администратора к правам коллекции языков (МУТАЦИЯ).

        ВОССТАНОВЛЕНИЕ доступа администратора (грант, НЕ отзыв): возвращает текущему
        пользователю-администратору гарантированный доступ к настройке прав указанной цели защиты,
        если он был случайно потерян (например, администратор сам себе запретил доступ и
        заблокировался). Сервер заново выдаёт администратору полные права на эту цель; чужие права
        при этом не отзываются. Применяйте как «аварийную кнопку» разблокировки управления
        безопасностью цели.

        Когда применять: после ошибочной настройки прав, из-за которой администратор утратил
        возможность редактировать безопасность коллекции языков. Парный read для проверки текущего
        снимка прав — :meth:`languages_security`.

        Защита: мутация защищена ``confirm`` — без ``confirm=True`` поднимается :class:`ValueError`
        ещё ДО обращения к серверу (запрос не выполняется). Тела у запроса нет: отправляется пустой
        JSON-объект ``{}`` (иначе сервер ответит 415).

        Args:
            confirm: Подтверждение мутирующей операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера (в т.ч. 403 при недостатке прав).

        Example:
            async with IPSClient(config=config) as ips:
                await ips.restore_admin_access_languages(confirm=True)

        Notes:
            operationId ``Security_RestoreAdminAccessLanguageCollectionSecurity``. Запрос без тела
            (``json={}``).
            Путь ``POST``:
            ``.../security/languages/restoreAdminAccess``
            Парный read — :meth:`languages_security`.
        """
        if confirm is not True:
            raise ValueError(
                "restore_admin_access_languages меняет права доступа; передайте confirm=True",
            )
        await self._request(
            "post",
            "/core/api/security/languages/restoreAdminAccess",
            json={},
        )
        return None
