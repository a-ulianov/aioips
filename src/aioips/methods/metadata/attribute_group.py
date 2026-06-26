"""Метод получения группы атрибутов по идентификатору."""

from ...core import APIManager
from ...schemas.metadata import AttributeGroup


class AttributeGroupMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributeGroups/{id}``."""

    async def attribute_group(
        self: "AttributeGroupMixin",
        attribute_group_id: int,
    ) -> AttributeGroup | None:
        """Возвращает описание группы атрибутов по её идентификатору.

        Группа атрибутов — узел иерархии, объединяющий типы атрибутов в логический
        набор. Метод даёт метаданные самой группы (имя, родитель, примечание); СОСТАВ
        группы (входящие типы атрибутов) читается отдельно методами
        :meth:`attributes_in_group_ids` / :meth:`attributes_in_group_guids`. Ответ
        сервера обёрнут в ``...NullableResultDto`` (``{entity, isEntityPresent}``);
        обёртка разворачивается здесь, наружу отдаётся либо схема, либо ``None``.

        Когда применять: чтобы по известному ``id`` группы получить её метаописание и
        положение в иерархии (поле ``parent_id``). Аналог по GUID —
        :meth:`attribute_group_by_guid`.

        Args:
            attribute_group_id: Идентификатор группы атрибутов (id-пространство ГРУПП
                атрибутов; не тип атрибута и не значение атрибута объекта).

        Returns:
            Группа атрибутов по схеме :class:`AttributeGroup` либо ``None``, если группа
            с таким идентификатором не найдена (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                group = await ips.attribute_group(42)
                if group is not None:
                    print(group.name, group.parent_id)

        Notes:
            operationId ``Metadata_GetAttributeGroupById``; путь
            ``GET /core/api/metadata/attributeGroups/{id}``. Связанные методы:
            :meth:`attribute_group_by_guid`, :meth:`attributes_in_group_ids`.
        """
        path = f"/core/api/metadata/attributeGroups/{attribute_group_id}"
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        return AttributeGroup.model_validate(entity) if entity is not None else None
