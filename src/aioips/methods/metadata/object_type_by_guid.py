"""Метод получения типа объекта по GUID."""

from uuid import UUID

from ...core import APIManager
from ...schemas.metadata import ObjectType


class ObjectTypeByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/objectTypes/byGuid/{guid}``."""

    async def object_type_by_guid(
        self: "ObjectTypeByGuidMixin",
        guid: UUID | str,
    ) -> ObjectType | None:
        """Возвращает описание типа объекта по его глобальному идентификатору (GUID).

        GUID типа объекта стабилен между базами данных, поэтому удобен как переносимый
        ключ метаданных. Ответ сервера обёрнут в ``...NullableResultDto``
        (``{entity, isEntityPresent}``); обёртка разворачивается здесь, наружу отдаётся
        либо схема, либо ``None``.

        Когда применять: тот же результат, что у :meth:`object_type`, но ключ —
        переносимый GUID (когда числовой ``id`` между базами различается). Полезно для
        кода, работающего с несколькими инсталляциями IPS.

        Args:
            guid: Глобальный идентификатор типа объекта (``UUID`` или строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Подставляется в URL как есть.

        Returns:
            Тип объекта по схеме :class:`ObjectType` либо ``None``, если тип с таким
            GUID не найден (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                object_type = await ips.object_type_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                if object_type is not None:
                    print(object_type.id, object_type.object_name)

        Notes:
            operationId ``Metadata_GetObjectTypeByGuid``; путь
            ``GET /core/api/metadata/objectTypes/byGuid/{guid}``.
            Связанный метод по числовому id — :meth:`object_type`.
        """
        data = await self._request("get", f"/core/api/metadata/objectTypes/byGuid/{guid}")
        entity = data.get("entity") if isinstance(data, dict) else None
        return ObjectType.model_validate(entity) if entity is not None else None
