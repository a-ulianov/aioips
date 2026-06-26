"""Метод упаковки временного каталога в ZIP через IPS Bridge (мутация)."""

from typing import Any

from ...core import APIManager
from ...schemas.bridge.file_info_dto import FileInfoDto


class BridgePackDirectoryAsZipMixin(APIManager):
    """Реализует ``POST /core/api/Bridge/Files/PackDirectoryAsZip``.

    ``operationId``: ``Bridge_PackTempDirectoryAsZip``.
    """

    async def bridge_pack_directory_as_zip(
        self: "BridgePackDirectoryAsZipMixin",
        *,
        dir_path: str | None = None,
        confirm: bool = False,
    ) -> FileInfoDto:
        """Упаковывает временный каталог в ZIP-файл (МУТАЦИЯ).

        IPS Bridge — серверный помощник десктоп-клиента; он оперирует временными
        файлами сессии. Метод упаковывает содержимое каталога в ZIP и возвращает
        путь и размер архива. Обратная операция к
        :meth:`bridge_extract_zip_file`; за подготовкой к скачиванию следует
        :meth:`bridge_download_temp_folder_as_zip`.

        Обратимость: операция создаёт ZIP-файл; уберите его парным
        :meth:`bridge_delete_temp_stored_item` по полю ``file_path`` результата.

        Защита: создаёт файл на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            dir_path: Серверный путь упаковываемого каталога. ``None`` — параметр
                не передаётся.
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            Сведения о созданном архиве по схеме :class:`FileInfoDto` с полями
            ``file_path`` (путь ZIP) и ``total_bytes`` (размер в байтах).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                info = await ips.bridge_pack_directory_as_zip(
                    dir_path="/tmp/ips/sess1", confirm=True,
                )
                print(info.file_path, info.total_bytes)

        Notes:
            ``operationId``: ``Bridge_PackTempDirectoryAsZip``; путь
            ``POST /core/api/Bridge/Files/PackDirectoryAsZip``. Ключ query —
            ``dirPath``.
        """
        if confirm is not True:
            raise ValueError(
                "bridge_pack_directory_as_zip создаёт ZIP на сервере; передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if dir_path is not None:
            params["dirPath"] = dir_path
        data = await self._request(
            "post", "/core/api/Bridge/Files/PackDirectoryAsZip", params=params, json={}
        )
        return FileInfoDto.model_validate(data)
