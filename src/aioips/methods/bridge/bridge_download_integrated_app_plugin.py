"""Метод поиска и загрузки плагина встроенного приложения через IPS Bridge."""

from typing import Any

from ...core import APIManager


class BridgeDownloadIntegratedAppPluginMixin(APIManager):
    """Реализует ``GET /core/api/Bridge/Download/IntegratedAppPlugin``.

    operationId ``Bridge_TryFindAndDownloadPlugin``.
    """

    async def bridge_download_integrated_app_plugin(
        self: "BridgeDownloadIntegratedAppPluginMixin",
        plugin_name: str,
        *,
        with_file: bool | None = None,
    ) -> dict[str, Any]:
        """Находит и отдаёт плагин встроенного приложения через IPS Bridge.

        IPS Bridge — серверный помощник десктоп-клиента; метод ищет на сервере
        плагин интегрированного приложения и возвращает его описание-обёртку.
        Применяйте, когда клиенту нужно подгрузить плагин (опционально вместе с
        файлом сборки). Операция идемпотентна и не мутирует сервер.

        Ответ — JSON-объект (метаданные плагина и, при ``with_file=True``, его
        содержимое), а не «сырые» байты.

        Args:
            plugin_name: Имя искомого плагина (передаётся в query как
                ``pluginName``). Обязательный параметр.
            with_file: Прикладывать ли содержимое файла плагина. ``True`` —
                вернуть с файлом, ``False`` — только метаданные, ``None`` —
                параметр ``withFile`` в query не передаётся (поведение по
                умолчанию на стороне сервера).

        Returns:
            Словарь-описание плагина «как есть» (имя/метаданные и, при
            ``with_file=True``, содержимое файла). Пустой словарь — сервер
            вернул пустой ответ.

        Raises:
            IPSNotFoundError: Если плагин не найден.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                dto = await ips.bridge_download_integrated_app_plugin(
                    "PdfViewer", with_file=True,
                )
                print(dto.get("pluginName"))

        Notes:
            operationId ``Bridge_TryFindAndDownloadPlugin``; путь
            ``GET /core/api/Bridge/Download/IntegratedAppPlugin``; ключи query —
            ``pluginName`` (обязателен) и ``withFile`` (опционален). Ответ — JSON.
            Связанные методы: :meth:`bridge_download_library`,
            :meth:`bridge_download_app`.
        """
        params: dict[str, Any] = {"pluginName": plugin_name}
        if with_file is not None:
            # aiohttp/yarl не принимает bool в query — сериализуем в "true"/"false".
            params["withFile"] = str(with_file).lower()
        data = await self._request(
            "get",
            "/core/api/Bridge/Download/IntegratedAppPlugin",
            params=params,
        )
        return data if isinstance(data, dict) else {}
