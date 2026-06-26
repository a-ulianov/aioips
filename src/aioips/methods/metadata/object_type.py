"""Метод получения типа объекта по идентификатору."""

from ...core import APIManager
from ...schemas.metadata import ObjectType


class ObjectTypeMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/objectTypes/{id}``."""

    async def object_type(
        self: "ObjectTypeMixin",
        object_type_id: int,
    ) -> ObjectType | None:
        """Возвращает описание типа объекта по его идентификатору.

        Тип объекта — это класс сущностей предметной области (документ, изделие,
        архив и т.п.); его идентификатор задаёт «пространство типов объектов» и служит
        ключом во многих запросах. Ответ сервера обёрнут в ``...NullableResultDto``
        (``{entity, isEntityPresent}``); обёртка разворачивается здесь, наружу отдаётся
        либо схема, либо ``None``.

        Когда применять: чтобы по известному ``id`` типа получить его полное
        метаописание (имя, режим версионирования, атрибут заголовка и т.д.). ``id``
        берётся из :meth:`object_types`, :meth:`object_type_id_by_name` или из поля
        ``ObjectDto.object_type``. Аналог по GUID — :meth:`object_type_by_guid`.

        Args:
            object_type_id: Идентификатор типа объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID`` конкретного
                объекта или его версии).

        Returns:
            Тип объекта по схеме :class:`ObjectType` либо ``None``, если тип с таким
            идентификатором не найден (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                object_type = await ips.object_type(1742)
                if object_type is not None:
                    print(object_type.object_name, object_type.versions_mode)

        Notes:
            operationId ``Metadata_GetObjectTypeById``; путь
            ``GET /core/api/metadata/objectTypes/{id}``.
            Связанные методы: :meth:`object_types`, :meth:`object_type_by_guid`,
            :meth:`object_type_life_cycle_steps`.
        """
        data = await self._request("get", f"/core/api/metadata/objectTypes/{object_type_id}")
        entity = data.get("entity") if isinstance(data, dict) else None
        return ObjectType.model_validate(entity) if entity is not None else None
