"""Метод получения краткой информации о типе объекта по GUID."""

from urllib.parse import quote
from uuid import UUID

from ...core import APIManager
from ...schemas.object_types import QuickObjectTypeInfo


class ObjectTypeQuickInfoByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/objectTypes/byGuid/{objectTypeGuid}/objectTypeInfo``."""

    async def object_type_quick_info_by_guid(
        self: "ObjectTypeQuickInfoByGuidMixin",
        object_type_guid: UUID | str,
    ) -> QuickObjectTypeInfo | None:
        """Возвращает краткую информацию о ТИПЕ объекта по его GUID.

        Тот же облегчённый результат, что у :meth:`object_type_quick_info` (id, GUID,
        наименование типа), но ключом служит переносимый GUID типа (стабилен между
        базами). Ответ обёрнут в ``QuickObjectTypeInfoDtoNullableResultDto``
        (``{entity, isEntityPresent}``); обёртка разворачивается здесь, наружу — либо
        схема, либо ``None``.

        Это инфо о самом ТИПЕ, а не об экземплярах: счётчики реальных объектов —
        :meth:`object_type_objects_info`, перечень объектов — :meth:`object_type_objects`.

        Когда применять: чтобы по GUID типа дёшево узнать его id и имя в коде,
        переносимом между инсталляциями IPS.

        Args:
            object_type_guid: Глобальный идентификатор ТИПА объекта (``UUID`` или строка
                вида ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Кодируется в URL.

        Returns:
            Краткая информация по схеме :class:`QuickObjectTypeInfo` либо ``None``, если
            тип с таким GUID не найден (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                info = await ips.object_type_quick_info_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                if info is not None:
                    print(info.id, info.name)

        Notes:
            operationId ``ObjectTypes_GetObjectTypeInfoByGuid``; путь
            ``GET /core/api/objectTypes/byGuid/{objectTypeGuid}/objectTypeInfo``
            (обёртка ``QuickObjectTypeInfoDtoNullableResultDto``).
            Связанный метод по числовому id — :meth:`object_type_quick_info`.
        """
        encoded = quote(str(object_type_guid), safe="")
        path = f"/core/api/objectTypes/byGuid/{encoded}/objectTypeInfo"
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        return QuickObjectTypeInfo.model_validate(entity) if entity is not None else None
