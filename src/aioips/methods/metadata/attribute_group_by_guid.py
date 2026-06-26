"""Метод получения группы атрибутов по GUID."""

from urllib.parse import quote

from ...core import APIManager
from ...schemas.metadata import AttributeGroup


class AttributeGroupByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributeGroups/byGuid/{guid}``."""

    async def attribute_group_by_guid(
        self: "AttributeGroupByGuidMixin",
        guid: str,
    ) -> AttributeGroup | None:
        """Возвращает описание группы атрибутов по её GUID.

        Версия :meth:`attribute_group` с адресацией по переносимому GUID: GUID группы
        стабилен между установками IPS, в отличие от числового ``id``. Метод даёт
        метаданные группы; её СОСТАВ читается методами
        :meth:`attributes_in_group_ids_by_guid` / :meth:`attributes_in_group_guids_by_guid`.
        Ответ обёрнут в ``...NullableResultDto``; обёртка разворачивается здесь, наружу
        отдаётся либо схема, либо ``None``.

        Когда применять: когда конфигурация хранит стабильный GUID группы, а нужно её
        метаописание. Перевод «GUID → id» — :meth:`attribute_group_id_by_guid`.

        Args:
            guid: GUID группы атрибутов (стабильный идентификатор в id-пространстве
                ГРУПП атрибутов), строка вида ``cad001c5-306c-11d8-b4e9-00304f19f545``;
                кодируется в URL.

        Returns:
            Группа атрибутов по схеме :class:`AttributeGroup` либо ``None``, если группа
            с таким GUID не найдена (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                group = await ips.attribute_group_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            operationId ``Metadata_GetAttributeGroupByGuid``; путь
            ``GET /core/api/metadata/attributeGroups/byGuid/{guid}``. Связанные методы:
            :meth:`attribute_group`, :meth:`attribute_group_id_by_guid`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/attributeGroups/byGuid/{encoded_guid}"
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        return AttributeGroup.model_validate(entity) if entity is not None else None
