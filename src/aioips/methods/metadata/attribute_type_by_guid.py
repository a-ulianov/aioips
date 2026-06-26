"""Метод получения типа атрибута по GUID."""

from uuid import UUID

from ...core import APIManager
from ...schemas.metadata import AttributeType


class AttributeTypeByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributeTypes/byGuid/{guid}``."""

    async def attribute_type_by_guid(
        self: "AttributeTypeByGuidMixin",
        guid: UUID | str,
    ) -> AttributeType | None:
        """Возвращает описание типа атрибута по его глобальному идентификатору (GUID).

        GUID типа атрибута стабилен между базами данных, поэтому удобен как переносимый
        ключ метаданных. Тип атрибута задаёт тип данных характеристики (``FieldTypes``),
        режим множественности и вычисляемости значений. Ответ сервера обёрнут в
        ``...NullableResultDto`` (``{entity, isEntityPresent}``); обёртка
        разворачивается здесь, наружу отдаётся либо схема, либо ``None``.

        Когда применять: тот же результат, что у :meth:`attribute_type`, но ключ —
        переносимый GUID (когда числовой ``id`` между базами различается). Полезно для
        кода, работающего с несколькими инсталляциями IPS.

        Args:
            guid: Глобальный идентификатор типа атрибута (``UUID`` или строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Подставляется в URL как есть.

        Returns:
            Тип атрибута по схеме :class:`AttributeType` либо ``None``, если тип атрибута
            с таким GUID не найден (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                attr = await ips.attribute_type_by_guid("cad001c5-306c-11d8-b4e9-00304f19f545")
                if attr is not None:
                    print(attr.id, attr.name)

        Notes:
            operationId ``Metadata_GetAttributeTypeByGuid``; путь
            ``GET /core/api/metadata/attributeTypes/byGuid/{guid}``.
        """
        data = await self._request("get", f"/core/api/metadata/attributeTypes/byGuid/{guid}")
        entity = data.get("entity") if isinstance(data, dict) else None
        return AttributeType.model_validate(entity) if entity is not None else None
