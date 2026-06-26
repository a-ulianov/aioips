"""Метод получения настройки атрибута для типа объекта по GUID."""

from uuid import UUID

from ...core import APIManager
from ...schemas.metadata import AttributeForObjectType


class AttributeForObjectTypeByGuidsMixin(APIManager):
    """Реализует ``GET attributeForObjectType/byGuid/{objectTypeGuid}/{attributeTypeGuid}``."""

    async def attribute_for_object_type_by_guids(
        self: "AttributeForObjectTypeByGuidsMixin",
        object_type_guid: UUID | str,
        attribute_type_guid: UUID | str,
    ) -> AttributeForObjectType | None:
        """Возвращает настройку применения атрибута к типу объекта по паре GUID.

        Тот же результат, что у :meth:`attribute_for_object_type`, но ключи —
        переносимые между базами GUID типа объекта и типа атрибута (когда числовые
        ``id`` между инсталляциями различаются). Отдаёт индивидуальные настройки пары
        «тип объекта × тип атрибута»: обязательность/видимость, вычисляемость, формулу,
        ограничение ссылки. Ответ сервера обёрнут в ``...NullableResultDto``
        (``{entity, isEntityPresent}``); обёртка разворачивается здесь, наружу
        отдаётся либо схема, либо ``None``.

        Когда применять: для кода, работающего с несколькими инсталляциями IPS, где
        идентификация ведётся по GUID.

        Args:
            object_type_guid: GUID типа объекта (``UUID`` или строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Подставляется в URL как есть.
            attribute_type_guid: GUID типа атрибута (``UUID`` или строка).

        Returns:
            Настройка по схеме :class:`AttributeForObjectType` либо ``None``, если
            атрибут к данному типу объекта не привязан (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                binding = await ips.attribute_for_object_type_by_guids(
                    "11111111-1111-1111-1111-111111111111",
                    "cad001c5-306c-11d8-b4e9-00304f19f545",
                )
                if binding is not None:
                    print(binding.required)

        Notes:
            operationId ``Metadata_GetAttributeForObjectTypeByGuids``; путь ``GET
            /core/api/metadata/attributeForObjectType/byGuid/{objectTypeGuid}/{attributeTypeGuid}``.
            Связанный метод по числовым id — :meth:`attribute_for_object_type`.
        """
        path = (
            "/core/api/metadata/attributeForObjectType/byGuid/"
            f"{object_type_guid}/{attribute_type_guid}"
        )
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        return AttributeForObjectType.model_validate(entity) if entity is not None else None
