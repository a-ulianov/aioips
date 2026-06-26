"""Метод получения настройки атрибута для типа связи по GUID."""

from uuid import UUID

from ...core import APIManager
from ...schemas.metadata import AttributeForRelationType


class AttributeForRelationTypeByGuidsMixin(APIManager):
    """Реализует ``GET attributeForRelationType/byGuid/{relationTypeGuid}/{attributeTypeGuid}``."""

    async def attribute_for_relation_type_by_guids(
        self: "AttributeForRelationTypeByGuidsMixin",
        relation_type_guid: UUID | str,
        attribute_type_guid: UUID | str,
    ) -> AttributeForRelationType | None:
        """Возвращает настройку применения атрибута к типу связи по паре GUID.

        Тот же результат, что у :meth:`attribute_for_relation_type`, но ключи —
        переносимые между базами GUID типа связи и типа атрибута (когда числовые ``id``
        между инсталляциями различаются). Отдаёт индивидуальные настройки пары «тип
        связи × тип атрибута»: обязательность/видимость, вычисляемость, формулу,
        ограничение ссылки. Ответ сервера обёрнут в ``...NullableResultDto``
        (``{entity, isEntityPresent}``); обёртка разворачивается здесь, наружу
        отдаётся либо схема, либо ``None``.

        Когда применять: для кода, работающего с несколькими инсталляциями IPS, где
        идентификация ведётся по GUID.

        Args:
            relation_type_guid: GUID типа связи (``UUID`` или строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Подставляется в URL как есть.
            attribute_type_guid: GUID типа атрибута (``UUID`` или строка).

        Returns:
            Настройка по схеме :class:`AttributeForRelationType` либо ``None``, если
            атрибут к данному типу связи не привязан (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                binding = await ips.attribute_for_relation_type_by_guids(
                    "22222222-2222-2222-2222-222222222222",
                    "cad001c5-306c-11d8-b4e9-00304f19f545",
                )
                if binding is not None:
                    print(binding.required)

        Notes:
            operationId ``Metadata_GetAttributeForRelationTypeByGuids``; путь ``GET /core/api
            /metadata/attributeForRelationType/byGuid/{relationTypeGuid}/{attributeTypeGuid}``.
            Связанный метод по числовым id — :meth:`attribute_for_relation_type`.
        """
        path = (
            "/core/api/metadata/attributeForRelationType/byGuid/"
            f"{relation_type_guid}/{attribute_type_guid}"
        )
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        return AttributeForRelationType.model_validate(entity) if entity is not None else None
