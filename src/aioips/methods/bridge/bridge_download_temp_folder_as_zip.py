"""Метод подготовки временной папки к скачиванию ZIP через IPS Bridge (мутация)."""

from typing import Any

from ...core import APIManager


class BridgeDownloadTempFolderAsZipMixin(APIManager):
    """Реализует ``POST /core/api/Bridge/Files/DownloadTempFolderAsZip``.

    ``operationId``: ``Bridge_DownloadTempFile``.
    """

    async def bridge_download_temp_folder_as_zip(
        self: "BridgeDownloadTempFolderAsZipMixin",
        *,
        file_path: str | None = None,
        confirm: bool = False,
    ) -> str:
        """Готовит временную папку к скачиванию как ZIP и возвращает путь (МУТАЦИЯ).

        IPS Bridge — серверный помощник десктоп-клиента; он оперирует временными
        файлами сессии. Метод формирует на сервере ZIP для указанного пути и
        возвращает путь готового файла. Применяйте после
        :meth:`bridge_pack_directory_as_zip`, чтобы получить ссылку на скачивание.

        Обратимость: операция создаёт временный артефакт; уберите его парным
        :meth:`bridge_delete_temp_stored_item` по возвращённому пути.

        Защита: создаёт файл на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            file_path: Серверный путь папки/файла-источника. ``None`` — параметр
                не передаётся.
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            Серверный путь подготовленного ZIP (``str``). Пустая строка ``""``,
            если сервер вернул ``null``.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                zip_path = await ips.bridge_download_temp_folder_as_zip(
                    file_path="/tmp/ips/sess1", confirm=True,
                )

        Notes:
            ``operationId``: ``Bridge_DownloadTempFile``; путь
            ``POST /core/api/Bridge/Files/DownloadTempFolderAsZip``. Ключ query —
            ``filePath``.
        """
        if confirm is not True:
            raise ValueError(
                "bridge_download_temp_folder_as_zip создаёт ZIP на сервере; передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if file_path is not None:
            params["filePath"] = file_path
        data = await self._request(
            "post",
            "/core/api/Bridge/Files/DownloadTempFolderAsZip",
            params=params,
            json={},
        )
        return "" if data is None else str(data)
