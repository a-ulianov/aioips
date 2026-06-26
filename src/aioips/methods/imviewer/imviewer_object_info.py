"""Метод получения краткой информации об объекте 3D-просмотрщика."""

from ...core import APIManager
from ...schemas.imviewer import ImViewerObjectInfo


class ImViewerObjectInfoMixin(APIManager):
    """Метод ``imviewer/objectInfo/{objectId}/{blobId}`` (``ImViewer_GetObjectInfo``)."""

    async def imviewer_object_info(
        self: "ImViewerObjectInfoMixin",
        object_id: int,
        blob_id: int,
    ) -> ImViewerObjectInfo:
        """Возвращает краткую информацию о 3D-объекте в blob (деталь или сборка).

        Лёгкий запрос-«заголовок»: до загрузки тяжёлой геометрии определяет тип объекта
        в файловом blob, чтобы выбрать корректный метод чтения. По полю ``type`` ответа:
        ``"part"`` → загружайте :meth:`imviewer_mesh`; ``"asm"`` →
        :meth:`imviewer_assembly`; ``"unknown"`` — тип не распознан. Применять как первый
        шаг при работе с 3D-данными неизвестного типа.

        Id-пространство (критично): ``object_id`` — это идентификатор ОБЪЕКТА
        (``F_OBJECT_ID``), а ``blob_id`` — идентификатор файлового blob, то есть значение
        файлового атрибута (``ftFile``) этого объекта, ссылающегося на CAD-файл во
        внешнем vault. Это два РАЗНЫХ id-пространства, не путать их между собой.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / ``F_OBJECT_ID``), общий для
                всех версий. Не идентификатор версии и не blob.
            blob_id: Идентификатор файлового blob (значение файлового атрибута ``ftFile``
                объекта) с геометрией CAD-модели.

        Returns:
            Информация по схеме :class:`ImViewerObjectInfo`. Поле ``type`` — тип объекта:
            ``"unknown"`` | ``"part"`` | ``"asm"`` (может быть ``None``).

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если объект/blob не найден).

        Example:
            async with IPSClient(config=config) as ips:
                info = await ips.imviewer_object_info(102550, 778899)
                if info.type == "part":
                    mesh = await ips.imviewer_mesh(102550, 778899)

        Notes:
            ``operationId``: ``ImViewer_GetObjectInfo``; путь
            ``GET /core/api/imviewer/objectInfo/{objectId}/{blobId}``. См. также
            :meth:`imviewer_mesh`, :meth:`imviewer_assembly`.
        """
        path = f"/core/api/imviewer/objectInfo/{object_id}/{blob_id}"
        data = await self._request("get", path)
        return ImViewerObjectInfo.model_validate(data)
