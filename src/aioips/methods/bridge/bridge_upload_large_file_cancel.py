"""Метод отмены чанковой загрузки файла через IPS Bridge (мутация)."""

from typing import Any

from ...core import APIManager


class BridgeUploadLargeFileCancelMixin(APIManager):
    """Реализует ``DELETE /core/api/Bridge/Files/UploadLargeFileCancel``.

    ``operationId``: ``Bridge_UploadLargeFileCancel``.
    """

    async def bridge_upload_large_file_cancel(
        self: "BridgeUploadLargeFileCancelMixin",
        *,
        request_guid: str | None = None,
        confirm: bool = False,
    ) -> None:
        """Отменяет открытую сессию чанковой загрузки файла (МУТАЦИЯ).

        IPS Bridge — серверный помощник десктоп-клиента; крупные файлы он
        принимает по частям. Метод отменяет незавершённую загрузку по её GUID,
        освобождая частично принятые данные. Парная отмена к
        :meth:`bridge_upload_large_file_request`.

        Обратимость: операция НЕОБРАТИМА — отменённую сессию нельзя возобновить
        (это сам механизм отката незавершённой загрузки).

        Защита: меняет состояние на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            request_guid: GUID сессии загрузки. ``None`` — параметр не передаётся.
            confirm: Подтверждение отмены. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие
            ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.bridge_upload_large_file_cancel(
                    request_guid=guid, confirm=True,
                )

        Notes:
            ``operationId``: ``Bridge_UploadLargeFileCancel``; путь
            ``DELETE /core/api/Bridge/Files/UploadLargeFileCancel``. Ключ query —
            ``requestGuid``.
        """
        if confirm is not True:
            raise ValueError(
                "bridge_upload_large_file_cancel отменяет загрузку на сервере; "
                "передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if request_guid is not None:
            params["requestGuid"] = request_guid
        await self._request("delete", "/core/api/Bridge/Files/UploadLargeFileCancel", params=params)
        return None
