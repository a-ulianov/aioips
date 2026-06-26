"""Метод получения определения типа объекта по идентификатору."""

from ...core import APIManager
from ...schemas.object_types import ObjectTypeDefinition


class ObjectTypeDefinitionMixin(APIManager):
    """Реализует метод ``GET /core/api/objectTypes/{objectTypeId}``."""

    async def object_type_definition(
        self: "ObjectTypeDefinitionMixin",
        object_type_id: int,
    ) -> ObjectTypeDefinition | None:
        """Возвращает определение типа объекта (``ObjectTypeDto``) по идентификатору.

        Отдаёт полное определение ТИПА из контроллера ``objectTypes``: идентичность,
        режим версионирования, наследование схемы ЖЦ, атрибут заголовка, родительский
        тип, опции. Ответ сервера обёрнут в ``ObjectTypeDtoNullableResultDto``
        (``{entity, isEntityPresent}``); обёртка разворачивается здесь, наружу отдаётся
        либо схема, либо ``None``.

        Отличие от раздела ``metadata``: тот возвращает ``ImsObjectTypeDto`` — машинное
        описание метамодели; здесь — ``ObjectTypeDto``, определение типа в рабочем
        контроллере объектов этого типа (рядом с методами перечисления экземпляров).

        Когда применять: чтобы по известному ``ObjectTypeID`` получить определение типа.
        Аналоги по другим ключам — :meth:`object_type_definition_by_guid` и
        :meth:`object_type_definition_by_name`. Если нужны только id/GUID/имя —
        дешевле :meth:`object_type_quick_info`.

        Args:
            object_type_id: Идентификатор ТИПА объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID`` конкретного
                объекта или его версии).

        Returns:
            Определение типа по схеме :class:`ObjectTypeDefinition` либо ``None``, если
            тип с таким идентификатором не найден (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                definition = await ips.object_type_definition(1742)
                if definition is not None:
                    print(definition.object_type_name, definition.versionable)

        Notes:
            operationId ``ObjectTypes_GetObjectType``; путь
            ``GET /core/api/objectTypes/{objectTypeId}``
            (обёртка ``ObjectTypeDtoNullableResultDto``).
        """
        data = await self._request("get", f"/core/api/objectTypes/{object_type_id}")
        entity = data.get("entity") if isinstance(data, dict) else None
        return ObjectTypeDefinition.model_validate(entity) if entity is not None else None
