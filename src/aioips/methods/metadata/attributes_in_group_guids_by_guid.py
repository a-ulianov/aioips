"""Метод получения GUID типов атрибутов, входящих в группу (по GUID группы)."""

from urllib.parse import quote

from ...core import APIManager


class AttributesInGroupGuidsByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributesInGroup/byGuid/{guid}/guids``."""

    async def attributes_in_group_guids_by_guid(
        self: "AttributesInGroupGuidsByGuidMixin",
        guid: str,
    ) -> list[str]:
        """Возвращает GUID типов атрибутов, входящих в группу (по GUID группы).

        Полностью переносимый вариант: и группа адресуется по GUID, и состав отдаётся
        как GUID типов атрибутов. Удобен для сверки состава групп между установками IPS
        без привязки к локальным ``id``. Ответ сервера — массив строк, без обёртки
        ``...NullableResultDto``.

        Когда применять: для переносимого сравнения состава одноимённой группы между
        средами. Числовые id состава — :meth:`attributes_in_group_ids_by_guid`.

        Args:
            guid: GUID группы атрибутов (стабильный идентификатор в id-пространстве
                ГРУПП атрибутов), строка вида ``cad001c5-306c-11d8-b4e9-00304f19f545``;
                кодируется в URL.

        Returns:
            Список GUID типов атрибутов (строки в id-пространстве ТИПОВ атрибутов),
            входящих в группу. Пустой список — группа пуста или не существует.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guids = await ips.attributes_in_group_guids_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            operationId ``Metadata_GetAttributesInGroupGuidsByGuid``; путь
            ``GET /core/api/metadata/attributesInGroup/byGuid/{guid}/guids`` (ответ —
            массив строк). Связанные методы: :meth:`attributes_in_group_ids_by_guid`,
            :meth:`attributes_in_group_guids`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/attributesInGroup/byGuid/{encoded_guid}/guids"
        data = await self._request("get", path)
        return [str(item) for item in data] if data is not None else []
