"""Метод получения имени экземпляра по умолчанию для типа объекта по GUID."""

from urllib.parse import quote

from ...core import APIManager


class ObjectTypeObjectNameByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/objectTypes/byGuid/{guid}/objectName``."""

    async def object_type_object_name_by_guid(
        self: "ObjectTypeObjectNameByGuidMixin",
        guid: str,
    ) -> str:
        """Возвращает имя экземпляра по умолчанию для типа объекта по его GUID.

        Имя экземпляра (``objectName``) — отображаемое (как правило локализованное) имя
        объектов данного типа (например ``"Документ"``), в отличие от системного имени
        типа (:meth:`object_type_name_by_guid`, например ``"Document"``). Ключ здесь —
        переносимый GUID, стабильный между базами данных. Ответ сервера — голая строка,
        без обёртки ``...NullableResultDto``.

        Когда применять: тот же результат, что у :meth:`object_type_object_name`, но по
        переносимому GUID — для кода, работающего с несколькими инсталляциями IPS, где
        числовой ``id`` различается.

        Args:
            guid: Глобальный идентификатор типа объекта (строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Кодируется в URL.

        Returns:
            Отображаемое имя экземпляра типа объекта строкой; пустая строка, если
            сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                name = await ips.object_type_object_name_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(name)  # "Документ"

        Notes:
            operationId ``Metadata_GetObjectNameByGuid``; путь
            ``GET /core/api/metadata/objectTypes/byGuid/{guid}/objectName``.
            Связанный метод по числовому id — :meth:`object_type_object_name`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/objectTypes/byGuid/{encoded_guid}/objectName"
        data = await self._request("get", path)
        return "" if data is None else str(data)
