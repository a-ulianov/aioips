"""Метод получения триангуляционной сетки (mesh) детали для 3D-просмотрщика."""

from typing import Any

from ...core import APIManager
from ...schemas.imviewer import Mesh


class ImViewerMeshMixin(APIManager):
    """Реализует ``GET /core/api/imviewer/mesh/{objectId}/{blobId}`` (``ImViewer_GetMesh``)."""

    async def imviewer_mesh(
        self: "ImViewerMeshMixin",
        object_id: int,
        blob_id: int,
        *,
        config_name: str | None = None,
    ) -> Mesh:
        """Возвращает триангуляционную сетку (mesh) детали для 3D-просмотра модели.

        Загружает геометрию одной детали (part) из файлового blob модели в виде,
        пригодном для рендеринга в 3D-просмотрщике ImViewer: метаданные, информация о
        конфигурации и набор геометрических тел (триангуляция). Применять, когда тип
        объекта в blob — деталь; для сборок используйте :meth:`imviewer_assembly`. Если
        тип заранее неизвестен, сначала вызовите :meth:`imviewer_object_info` и выберите
        метод по полю ``type`` (``"part"`` → этот метод).

        Id-пространство (критично): ``object_id`` — это идентификатор ОБЪЕКТА
        (``F_OBJECT_ID``), а ``blob_id`` — идентификатор файлового blob, то есть
        значение файлового атрибута (``ftFile``) этого объекта, ссылающегося на CAD-файл
        во внешнем vault. Это два РАЗНЫХ id-пространства, не путать их между собой.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / ``F_OBJECT_ID``), общий для
                всех версий. Не идентификатор версии и не blob.
            blob_id: Идентификатор файлового blob (значение файлового атрибута ``ftFile``
                объекта) с геометрией CAD-модели.
            config_name: Имя конфигурации модели. Если задано — передаётся в query
                ``configName`` (выбор варианта исполнения/конфигурации). ``None`` (по
                умолчанию) — параметр не передаётся, используется конфигурация по умолчанию.

        Returns:
            Сетка детали по схеме :class:`Mesh`. Поля ``metadata``, ``config_info`` и
            ``bodies`` — непрозрачные структуры просмотрщика (крупные геометрические
            данные для рендера, не предназначены для разбора по полям).

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если объект/blob не
                найден или blob не является деталью).

        Example:
            async with IPSClient(config=config) as ips:
                mesh = await ips.imviewer_mesh(102550, 778899)
                bodies_count = len(mesh.bodies)

        Notes:
            ``operationId``: ``ImViewer_GetMesh``; путь
            ``GET /core/api/imviewer/mesh/{objectId}/{blobId}``. См. также
            :meth:`imviewer_assembly`, :meth:`imviewer_object_info`.
        """
        params: dict[str, Any] = {}
        if config_name is not None:
            params["configName"] = config_name
        path = f"/core/api/imviewer/mesh/{object_id}/{blob_id}"
        data = await self._request("get", path, params=params)
        return Mesh.model_validate(data)
