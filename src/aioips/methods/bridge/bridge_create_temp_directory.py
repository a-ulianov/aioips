"""Метод создания временного каталога сессии IPS Bridge (мутация)."""

from ...core import APIManager


class BridgeCreateTempDirectoryMixin(APIManager):
    """Реализует ``POST /core/api/Bridge/Files/CreateTempDirectory``.

    ``operationId``: ``Bridge_CreateTempDirectory``.
    """

    async def bridge_create_temp_directory(
        self: "BridgeCreateTempDirectoryMixin",
        *,
        confirm: bool = False,
    ) -> str:
        """Создаёт временный каталог в хранилище сессии IPS Bridge (МУТАЦИЯ).

        IPS Bridge — серверный помощник десктоп-клиента; он умеет создавать в
        рамках сессии временные каталоги/файлы. Метод создаёт новый временный
        каталог и возвращает его серверный путь. Применяйте перед чанковой
        загрузкой файлов или упаковкой содержимого в ZIP.

        Обратимость: операция ОБРАТИМА — созданный каталог удаляется парным
        :meth:`bridge_delete_temp_stored_item` (передайте полученный путь).

        Защита: создаёт ресурс на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            Серверный путь созданного каталога (``str``). Пустая строка ``""``,
            если сервер вернул ``null``.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                path = await ips.bridge_create_temp_directory(confirm=True)
                await ips.bridge_delete_temp_stored_item(path=path, confirm=True)

        Notes:
            ``operationId``: ``Bridge_CreateTempDirectory``; путь
            ``POST /core/api/Bridge/Files/CreateTempDirectory``. Тело не
            передаётся (``{}`` против 415).
        """
        if confirm is not True:
            raise ValueError(
                "bridge_create_temp_directory создаёт каталог на сервере; передайте confirm=True",
            )
        data = await self._request("post", "/core/api/Bridge/Files/CreateTempDirectory", json={})
        return "" if data is None else str(data)
