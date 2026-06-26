"""Метод удаления временного элемента хранилища IPS Bridge (мутация)."""

from typing import Any

from ...core import APIManager


class BridgeDeleteTempStoredItemMixin(APIManager):
    """Реализует ``DELETE /core/api/Bridge/Files/DeleteTempStoredItem``.

    ``operationId``: ``Bridge_DeleteTempStoredItem``.
    """

    async def bridge_delete_temp_stored_item(
        self: "BridgeDeleteTempStoredItemMixin",
        *,
        path: str | None = None,
        confirm: bool = False,
    ) -> None:
        """Удаляет временный файл или каталог из хранилища сессии (МУТАЦИЯ).

        IPS Bridge — серверный помощник десктоп-клиента; во время сессии он
        создаёт временные файлы и каталоги. Метод удаляет такой элемент по его
        серверному пути. Парная очистка к :meth:`bridge_create_temp_directory`,
        :meth:`bridge_pack_directory_as_zip` и методам загрузки файлов.

        Обратимость: операция НЕОБРАТИМА — удалённый временный элемент
        восстановить нельзя (это сам механизм отката для созданных временных
        ресурсов, а не операция с откатом).

        Защита: удаление защищено ``confirm`` — без ``confirm=True`` поднимается
        :class:`ValueError` ещё ДО обращения к серверу (запрос не выполняется).

        Args:
            path: Серверный путь удаляемого элемента. ``None`` — параметр не
                передаётся.
            confirm: Подтверждение удаления. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие
            ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера (404, если путь не найден).

        Example:
            async with IPSClient(config=config) as ips:
                await ips.bridge_delete_temp_stored_item(
                    path="/tmp/ips/sess1", confirm=True,
                )

        Notes:
            ``operationId``: ``Bridge_DeleteTempStoredItem``; путь
            ``DELETE /core/api/Bridge/Files/DeleteTempStoredItem``. Ключ query —
            ``path``.
        """
        if confirm is not True:
            raise ValueError(
                "bridge_delete_temp_stored_item удаляет элемент хранилища; передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if path is not None:
            params["path"] = path
        await self._request("delete", "/core/api/Bridge/Files/DeleteTempStoredItem", params=params)
        return None
