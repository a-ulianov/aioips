"""Метод получения данных сборки (assembly) для 3D-просмотрщика."""

from typing import Any

from ...core import APIManager
from ...schemas.imviewer import Assembly


class ImViewerAssemblyMixin(APIManager):
    """Метод ``GET /core/api/imviewer/assembly/{objectId}/{blobId}`` (``ImViewer_GetAssembly``)."""

    async def imviewer_assembly(
        self: "ImViewerAssemblyMixin",
        object_id: int,
        blob_id: int,
        *,
        config_name: str | None = None,
    ) -> Assembly:
        """Возвращает данные сборки (assembly) для 3D-просмотра модели.

        Загружает описание сборочной единицы (asm) из файлового blob модели для
        рендеринга в 3D-просмотрщике ImViewer: метаданные и информация о конфигурации
        сборки. Применять, когда тип объекта в blob — сборка; для отдельной детали
        используйте :meth:`imviewer_mesh`. Если тип заранее неизвестен, сначала вызовите
        :meth:`imviewer_object_info` и выберите метод по полю ``type`` (``"asm"`` → этот
        метод).

        Id-пространство (критично): ``object_id`` — это идентификатор ОБЪЕКТА
        (``F_OBJECT_ID``), а ``blob_id`` — идентификатор файлового blob, то есть значение
        файлового атрибута (``ftFile``) этого объекта, ссылающегося на CAD-файл во
        внешнем vault. Это два РАЗНЫХ id-пространства, не путать их между собой.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / ``F_OBJECT_ID``), общий для
                всех версий. Не идентификатор версии и не blob.
            blob_id: Идентификатор файлового blob (значение файлового атрибута ``ftFile``
                объекта) с геометрией CAD-модели.
            config_name: Имя конфигурации сборки. Если задано — передаётся в query
                ``configName`` (выбор варианта исполнения/конфигурации). ``None`` (по
                умолчанию) — параметр не передаётся, используется конфигурация по умолчанию.

        Returns:
            Данные сборки по схеме :class:`Assembly`. Поля ``metadata`` и ``config_info``
            — непрозрачные структуры просмотрщика (крупные вложенные данные для рендера,
            не предназначены для разбора по полям).

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если объект/blob не
                найден или blob не является сборкой).

        Example:
            async with IPSClient(config=config) as ips:
                asm = await ips.imviewer_assembly(102550, 778899, config_name="Default")
                meta = asm.metadata

        Notes:
            ``operationId``: ``ImViewer_GetAssembly``; путь
            ``GET /core/api/imviewer/assembly/{objectId}/{blobId}``. См. также
            :meth:`imviewer_mesh`, :meth:`imviewer_object_info`.
        """
        params: dict[str, Any] = {}
        if config_name is not None:
            params["configName"] = config_name
        path = f"/core/api/imviewer/assembly/{object_id}/{blob_id}"
        data = await self._request("get", path, params=params)
        return Assembly.model_validate(data)
