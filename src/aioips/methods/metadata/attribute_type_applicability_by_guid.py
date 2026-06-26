"""Метод получения применимости типа атрибута по GUID."""

from urllib.parse import quote

from ...core import APIManager
from ...schemas.metadata import AttributeTypeApplicability


class AttributeTypeApplicabilityByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributeTypeApplicability/byGuid/{guid}``."""

    async def attribute_type_applicability_by_guid(
        self: "AttributeTypeApplicabilityByGuidMixin",
        guid: str,
    ) -> AttributeTypeApplicability:
        """Возвращает категорию применимости типа атрибута по его GUID.

        Версия :meth:`attribute_type_applicability` с адресацией по переносимому GUID
        типа атрибута. Сообщает, к чему задействован тип атрибута: к объектам
        (``objectType``), к связям (``relationType``) или ни к чему (``none``). В swagger
        ответ — голый строковый enum ``IMSAttributeTypeApplicability``, возвращаемый
        НАПРЯМУЮ (без обёртки); строка валидируется в :class:`AttributeTypeApplicability`,
        значение доступно через ``.root``.

        Когда применять: когда тип атрибута известен по стабильному GUID, а нужен
        контекст его использования. Булев предикат — :meth:`attribute_is_in_use_by_guid`.

        Args:
            guid: GUID типа атрибута (стабильный идентификатор в id-пространстве ТИПОВ
                атрибутов), строка вида ``cad001c5-306c-11d8-b4e9-00304f19f545``;
                кодируется в URL.

        Returns:
            Применимость по схеме :class:`AttributeTypeApplicability`; конкретное значение
            (``none`` / ``objectType`` / ``relationType``) — в атрибуте ``root``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                applicability = await ips.attribute_type_applicability_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(applicability.root)

        Notes:
            operationId ``Metadata_GetAttributeTypeApplicabilityByGuid``; путь
            ``GET /core/api/metadata/attributeTypeApplicability/byGuid/{guid}`` (ответ —
            голый строковый enum). Связанные методы: :meth:`attribute_type_applicability`,
            :meth:`attribute_is_in_use_by_guid`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/attributeTypeApplicability/byGuid/{encoded_guid}"
        data = await self._request("get", path)
        return AttributeTypeApplicability.model_validate(data)
