"""Метод получения id типов атрибутов, входящих в группу (по GUID группы)."""

from urllib.parse import quote

from ...core import APIManager


class AttributesInGroupIdsByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributesInGroup/byGuid/{guid}/ids``."""

    async def attributes_in_group_ids_by_guid(
        self: "AttributesInGroupIdsByGuidMixin",
        guid: str,
    ) -> list[int]:
        """Возвращает id типов атрибутов, входящих в группу (по GUID группы).

        Версия :meth:`attributes_in_group_ids` с адресацией группы по переносимому GUID
        вместо локального ``id``. Раскрывает СОСТАВ группы (входящие типы атрибутов) и
        отдаёт их числовые ``id`` текущей среды. Ответ сервера — плоский массив целых,
        без обёртки ``...NullableResultDto``.

        Когда применять: когда группа известна по стабильному GUID, а нужны числовые
        ``id`` её типов атрибутов. Перечень GUID состава —
        :meth:`attributes_in_group_guids_by_guid`.

        Args:
            guid: GUID группы атрибутов (стабильный идентификатор в id-пространстве
                ГРУПП атрибутов), строка вида ``cad001c5-306c-11d8-b4e9-00304f19f545``;
                кодируется в URL.

        Returns:
            Список ``id`` типов атрибутов (id-пространство ТИПОВ атрибутов), входящих в
            группу. Пустой список — группа пуста или не существует.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ids = await ips.attributes_in_group_ids_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            operationId ``Metadata_GetAttributesInGroupByGuid``; путь
            ``GET /core/api/metadata/attributesInGroup/byGuid/{guid}/ids`` (ответ —
            массив ``int``). Связанные методы: :meth:`attributes_in_group_ids`,
            :meth:`attributes_in_group_guids_by_guid`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/attributesInGroup/byGuid/{encoded_guid}/ids"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
