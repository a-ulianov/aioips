"""Метод поиска и загрузки библиотеки (DLL) через IPS Bridge."""

from typing import Any

from ...core import APIManager


class BridgeDownloadLibraryMixin(APIManager):
    """Реализует ``GET /core/api/Bridge/Download/Library``.

    operationId ``Bridge_TryFindAndDownloadDll``.
    """

    async def bridge_download_library(
        self: "BridgeDownloadLibraryMixin",
        library_name: str,
    ) -> dict[str, Any]:
        """Находит и отдаёт библиотеку (DLL) для десктоп-клиента через IPS Bridge.

        IPS Bridge — серверный помощник десктоп-клиента; метод пытается найти на
        сервере запрошенную сборку и вернуть её описание-обёртку (имя файла и
        содержимое в base64). Применяйте, когда клиенту требуется подгрузить
        отсутствующую DLL (плагин/зависимость). Операция идемпотентна.

        В отличие от :meth:`bridge_download_app`, ответ — JSON-объект
        ``FileResponseDTO`` (метаданные + содержимое), а не «сырые» байты.

        Args:
            library_name: Имя искомой библиотеки/сборки (передаётся в query как
                ``libraryName``). Обязательный параметр.

        Returns:
            Словарь ``FileResponseDTO`` «как есть» (имя файла и содержимое файла,
            обычно в base64). Пустой словарь — сервер вернул пустой ответ.

        Raises:
            IPSNotFoundError: Если библиотека не найдена.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                dto = await ips.bridge_download_library("Intermech.Pdf.dll")
                print(dto.get("fileName"))

        Notes:
            operationId ``Bridge_TryFindAndDownloadDll``; путь
            ``GET /core/api/Bridge/Download/Library``; ключ query — ``libraryName``.
            Ответ — ``FileResponseDTO`` (JSON). Связанные методы:
            :meth:`bridge_download_app`,
            :meth:`bridge_download_integrated_app_plugin`.
        """
        params: dict[str, Any] = {"libraryName": library_name}
        data = await self._request(
            "get",
            "/core/api/Bridge/Download/Library",
            params=params,
        )
        return data if isinstance(data, dict) else {}
