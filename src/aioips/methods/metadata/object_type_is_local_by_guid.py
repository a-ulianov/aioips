"""Метод проверки локальности типа объекта по GUID."""

from urllib.parse import quote

from ...core import APIManager


class ObjectTypeIsLocalByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/objectTypes/byGuid/{guid}/isLocal``."""

    async def object_type_is_local_by_guid(
        self: "ObjectTypeIsLocalByGuidMixin",
        guid: str,
    ) -> bool:
        """Проверяет, является ли тип объекта локальным, по его GUID.

        Локальный тип объекта определён только в данной инсталляции IPS (не входит в
        общую/тиражируемую часть метаданных). Ключ здесь — переносимый GUID, стабильный
        между базами данных. Ответ сервера — голое булево значение, без обёртки
        ``...NullableResultDto``.

        Когда применять: тот же результат, что у :meth:`object_type_is_local`, но по
        переносимому GUID — для кода, работающего с несколькими инсталляциями IPS, где
        числовой ``id`` различается.

        Args:
            guid: Глобальный идентификатор типа объекта (строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Кодируется в URL.

        Returns:
            ``True`` — тип локальный для текущей базы; ``False`` — нет (в том числе если
            сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guid = "cad001c5-306c-11d8-b4e9-00304f19f545"
                if await ips.object_type_is_local_by_guid(guid):
                    print("Локальный тип")

        Notes:
            operationId ``Metadata_IsLocalObjectTypeByGuid``; путь
            ``GET /core/api/metadata/objectTypes/byGuid/{guid}/isLocal`` (ответ —
            ``boolean``). Аналог по числовому id — :meth:`object_type_is_local`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/objectTypes/byGuid/{encoded_guid}/isLocal"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
