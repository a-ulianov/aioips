"""Метод получения определения типа объекта по GUID."""

from urllib.parse import quote
from uuid import UUID

from ...core import APIManager
from ...schemas.object_types import ObjectTypeDefinition


class ObjectTypeDefinitionByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/objectTypes/byGuid/{objectTypeGuid}``."""

    async def object_type_definition_by_guid(
        self: "ObjectTypeDefinitionByGuidMixin",
        object_type_guid: UUID | str,
    ) -> ObjectTypeDefinition | None:
        """Возвращает определение типа объекта (``ObjectTypeDto``) по его GUID.

        Тот же результат, что у :meth:`object_type_definition`, но ключом служит
        переносимый GUID типа (стабилен между базами, в отличие от числового id). Ответ
        обёрнут в ``ObjectTypeDtoNullableResultDto`` (``{entity, isEntityPresent}``);
        обёртка разворачивается здесь, наружу — либо схема, либо ``None``.

        Отличие от раздела ``metadata``: тот возвращает ``ImsObjectTypeDto`` — метамодель;
        здесь — ``ObjectTypeDto``, определение типа из рабочего контроллера ``objectTypes``.

        Когда применять: для кода, переносимого между инсталляциями IPS, где числовой
        ``ObjectTypeID`` различается, а GUID типа постоянен.

        Args:
            object_type_guid: Глобальный идентификатор ТИПА объекта (``UUID`` или строка
                вида ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Кодируется в URL.

        Returns:
            Определение типа по схеме :class:`ObjectTypeDefinition` либо ``None``, если
            тип с таким GUID не найден (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                definition = await ips.object_type_definition_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                if definition is not None:
                    print(definition.object_type, definition.object_type_name)

        Notes:
            operationId ``ObjectTypes_GetObjectTypeByGuid``; путь
            ``GET /core/api/objectTypes/byGuid/{objectTypeGuid}``
            (обёртка ``ObjectTypeDtoNullableResultDto``).
            Связанный метод по числовому id — :meth:`object_type_definition`.
        """
        encoded = quote(str(object_type_guid), safe="")
        data = await self._request("get", f"/core/api/objectTypes/byGuid/{encoded}")
        entity = data.get("entity") if isinstance(data, dict) else None
        return ObjectTypeDefinition.model_validate(entity) if entity is not None else None
