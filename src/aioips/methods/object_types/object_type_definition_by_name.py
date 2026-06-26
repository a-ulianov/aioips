"""Метод получения определения типа объекта по имени."""

from urllib.parse import quote

from ...core import APIManager
from ...schemas.object_types import ObjectTypeDefinition


class ObjectTypeDefinitionByNameMixin(APIManager):
    """Реализует метод ``GET /core/api/objectTypes/byName/{objectTypeName}``."""

    async def object_type_definition_by_name(
        self: "ObjectTypeDefinitionByNameMixin",
        object_type_name: str,
    ) -> ObjectTypeDefinition | None:
        """Возвращает определение типа объекта (``ObjectTypeDto``) по его имени.

        Удобно, когда известно человекочитаемое наименование типа, но нужно его полное
        определение (включая числовой ``ObjectTypeID`` в поле ``object_type``). Имя
        кодируется в URL, поэтому допускаются пробелы и кириллица. Ответ обёрнут в
        ``ObjectTypeDtoNullableResultDto`` (``{entity, isEntityPresent}``); обёртка
        разворачивается здесь, наружу — либо схема, либо ``None``.

        Отличие от раздела ``metadata``: тот возвращает ``ImsObjectTypeDto`` — метамодель;
        здесь — ``ObjectTypeDto`` рабочего контроллера ``objectTypes``.

        Когда применять: как мост «имя → определение/id типа» перед методами раздела,
        требующими ``object_type_id`` (например :meth:`object_type_objects`). Аналоги по
        другим ключам — :meth:`object_type_definition`, :meth:`object_type_definition_by_guid`.

        Args:
            object_type_name: Наименование ТИПА объекта точно как в IPS (регистр и
                пробелы значимы); кодируется в URL, кириллица допускается.

        Returns:
            Определение типа по схеме :class:`ObjectTypeDefinition` либо ``None``, если
            тип с таким именем не найден (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                definition = await ips.object_type_definition_by_name("Деталь")
                if definition is not None:
                    print(definition.object_type)

        Notes:
            operationId ``ObjectTypes_GetObjectTypeByName``; путь
            ``GET /core/api/objectTypes/byName/{objectTypeName}``
            (обёртка ``ObjectTypeDtoNullableResultDto``).
        """
        encoded = quote(object_type_name, safe="")
        data = await self._request("get", f"/core/api/objectTypes/byName/{encoded}")
        entity = data.get("entity") if isinstance(data, dict) else None
        return ObjectTypeDefinition.model_validate(entity) if entity is not None else None
