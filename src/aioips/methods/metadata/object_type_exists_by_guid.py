"""Метод проверки существования типа объекта по GUID."""

from urllib.parse import quote

from ...core import APIManager


class ObjectTypeExistsByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/objectTypes/byGuid/{guid}/exists``."""

    async def object_type_exists_by_guid(
        self: "ObjectTypeExistsByGuidMixin",
        guid: str,
    ) -> bool:
        """Проверяет, существует ли тип объекта с указанным GUID.

        Дешёвый булев аксессор по переносимому ключу метаданных: GUID типа объекта
        стабилен между базами данных, поэтому удобен, когда числовой ``id`` между
        инсталляциями различается. Ответ сервера — голое булево значение, без обёртки
        ``...NullableResultDto``.

        Когда применять: как предварительный фильтр перед :meth:`object_type_by_guid`
        для кода, работающего с несколькими инсталляциями IPS. Аналог по числовому id —
        :meth:`object_type_exists`.

        Args:
            guid: Глобальный идентификатор типа объекта (строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Кодируется в URL.

        Returns:
            ``True`` — тип объекта с таким GUID существует; ``False`` — нет (в том числе
            если сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guid = "cad001c5-306c-11d8-b4e9-00304f19f545"
                if await ips.object_type_exists_by_guid(guid):
                    object_type = await ips.object_type_by_guid(guid)

        Notes:
            operationId ``Metadata_ExistsObjectTypeByGuid``; путь
            ``GET /core/api/metadata/objectTypes/byGuid/{guid}/exists`` (ответ —
            ``boolean``). Связанные методы: :meth:`object_type_by_guid`,
            :meth:`object_type_exists`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/objectTypes/byGuid/{encoded_guid}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
