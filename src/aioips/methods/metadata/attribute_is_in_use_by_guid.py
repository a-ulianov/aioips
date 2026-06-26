"""Метод проверки использования типа атрибута по GUID."""

from urllib.parse import quote

from ...core import APIManager


class AttributeIsInUseByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributeTypeApplicability/byGuid/{guid}/inUse``."""

    async def attribute_is_in_use_by_guid(
        self: "AttributeIsInUseByGuidMixin",
        guid: str,
    ) -> bool:
        """Проверяет, используется ли тип атрибута где-либо (по GUID).

        Версия :meth:`attribute_is_in_use` с адресацией по переносимому GUID типа
        атрибута. ``True`` означает, что тип задействован у объектов или связей
        (применимость не ``none``). Ответ сервера — голое булево значение, без обёртки
        ``...NullableResultDto``.

        Когда применять: как быстрый фильтр перед удалением/изменением типа атрибута,
        известного по стабильному GUID. Точная категория —
        :meth:`attribute_type_applicability_by_guid`.

        Args:
            guid: GUID типа атрибута (стабильный идентификатор в id-пространстве ТИПОВ
                атрибутов), строка вида ``cad001c5-306c-11d8-b4e9-00304f19f545``;
                кодируется в URL.

        Returns:
            ``True`` — тип атрибута используется (применим к объектам или связям);
            ``False`` — не используется нигде.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                in_use = await ips.attribute_is_in_use_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            operationId ``Metadata_IsAttributeInUseByGuid``; путь
            ``GET /core/api/metadata/attributeTypeApplicability/byGuid/{guid}/inUse``
            (ответ — ``boolean``). Связанные методы: :meth:`attribute_is_in_use`,
            :meth:`attribute_type_applicability_by_guid`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/attributeTypeApplicability/byGuid/{encoded_guid}/inUse"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
