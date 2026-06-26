"""Метод распаковки ZIP-файла во временном хранилище IPS Bridge (мутация)."""

from typing import Any

from ...core import APIManager


class BridgeExtractZipFileMixin(APIManager):
    """Реализует ``POST /core/api/Bridge/Files/ExtractZipFile``.

    ``operationId``: ``Bridge_ExtractZipFile``.
    """

    async def bridge_extract_zip_file(
        self: "BridgeExtractZipFileMixin",
        *,
        file_path: str | None = None,
        confirm: bool = False,
    ) -> str:
        """Распаковывает ZIP-файл во временном хранилище сессии (МУТАЦИЯ).

        IPS Bridge — серверный помощник десктоп-клиента; он оперирует временными
        файлами сессии. Метод распаковывает указанный ZIP и возвращает путь
        каталога с извлечённым содержимым. Обратная операция к
        :meth:`bridge_pack_directory_as_zip`.

        Обратимость: операция создаёт каталог с файлами; уберите его парным
        :meth:`bridge_delete_temp_stored_item` по возвращённому пути.

        Защита: создаёт файлы на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            file_path: Серверный путь распаковываемого ZIP. ``None`` — параметр
                не передаётся.
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            Серверный путь каталога с извлечённым содержимым (``str``). Пустая
            строка ``""``, если сервер вернул ``null``.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                out_dir = await ips.bridge_extract_zip_file(
                    file_path="/tmp/ips/sess1/data.zip", confirm=True,
                )

        Notes:
            ``operationId``: ``Bridge_ExtractZipFile``; путь
            ``POST /core/api/Bridge/Files/ExtractZipFile``. Ключ query —
            ``filePath``.
        """
        if confirm is not True:
            raise ValueError(
                "bridge_extract_zip_file распаковывает файлы на сервере; передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if file_path is not None:
            params["filePath"] = file_path
        data = await self._request(
            "post", "/core/api/Bridge/Files/ExtractZipFile", params=params, json={}
        )
        return "" if data is None else str(data)
