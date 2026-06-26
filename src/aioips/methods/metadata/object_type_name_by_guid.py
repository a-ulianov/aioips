"""Метод получения имени типа объекта по GUID."""

from urllib.parse import quote

from ...core import APIManager


class ObjectTypeNameByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/objectTypes/byGuid/{guid}/name``."""

    async def object_type_name_by_guid(
        self: "ObjectTypeNameByGuidMixin",
        guid: str,
    ) -> str:
        """Возвращает системное имя типа объекта по его GUID.

        Системное имя (``objectTypeName``) — короткий идентификатор типа в метаданных
        (например ``"Document"``), не локализованное отображаемое имя экземпляра. Ключ
        здесь — переносимый GUID, стабильный между базами данных. Ответ сервера — голая
        строка, без обёртки ``...NullableResultDto``.

        Когда применять: тот же результат, что у :meth:`object_type_name`, но по
        переносимому GUID — для кода, работающего с несколькими инсталляциями IPS, где
        числовой ``id`` различается.

        Args:
            guid: Глобальный идентификатор типа объекта (строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Кодируется в URL.

        Returns:
            Системное имя типа объекта строкой; пустая строка, если сервер вернул
            ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                name = await ips.object_type_name_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(name)  # "Document"

        Notes:
            operationId ``Metadata_GetObjectTypeNameByGuid``; путь
            ``GET /core/api/metadata/objectTypes/byGuid/{guid}/name``.
            Связанный метод по числовому id — :meth:`object_type_name`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/objectTypes/byGuid/{encoded_guid}/name"
        data = await self._request("get", path)
        return "" if data is None else str(data)
