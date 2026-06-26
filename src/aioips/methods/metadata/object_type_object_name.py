"""Метод получения имени экземпляра по умолчанию для типа объекта по идентификатору."""

from ...core import APIManager


class ObjectTypeObjectNameMixin(APIManager):
    """Реализует ``GET /core/api/metadata/objectTypes/{id}/objectName``."""

    async def object_type_object_name(
        self: "ObjectTypeObjectNameMixin",
        object_type_id: int,
    ) -> str:
        """Возвращает имя экземпляра по умолчанию для типа объекта по идентификатору.

        Имя экземпляра (``objectName``) — отображаемое (как правило локализованное) имя
        объектов данного типа (например ``"Документ"``), в отличие от системного имени
        типа (:meth:`object_type_name`, например ``"Document"``). Метод отдаёт только
        это имя, не загружая полное описание типа. Ответ сервера — голая строка, без
        обёртки ``...NullableResultDto``.

        Когда применять: для пользовательского отображения названия типа в интерфейсе,
        когда нужно лишь имя, а не вся схема :meth:`object_type`. Аналог по GUID —
        :meth:`object_type_object_name_by_guid`.

        Args:
            object_type_id: Идентификатор типа объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID``).

        Returns:
            Отображаемое имя экземпляра типа объекта строкой; пустая строка, если
            сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                name = await ips.object_type_object_name(1742)
                print(name)  # "Документ"

        Notes:
            operationId ``Metadata_GetObjectNameById``; путь
            ``GET /core/api/metadata/objectTypes/{id}/objectName``.
            Связанные методы: :meth:`object_type_object_name_by_guid`,
            :meth:`object_type_name` (системное имя типа).
        """
        path = f"/core/api/metadata/objectTypes/{object_type_id}/objectName"
        data = await self._request("get", path)
        return "" if data is None else str(data)
