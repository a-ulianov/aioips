"""Метод получения краткой информации о типе объекта по идентификатору."""

from ...core import APIManager
from ...schemas.object_types import QuickObjectTypeInfo


class ObjectTypeQuickInfoMixin(APIManager):
    """Реализует метод ``GET /core/api/objectTypes/{objectTypeId}/objectTypeInfo``."""

    async def object_type_quick_info(
        self: "ObjectTypeQuickInfoMixin",
        object_type_id: int,
    ) -> QuickObjectTypeInfo | None:
        """Возвращает краткую информацию о ТИПЕ объекта по идентификатору.

        Облегчённый запрос: по ``ObjectTypeID`` отдаёт только идентичность типа (id,
        GUID) и его наименование, без полного определения. Ответ обёрнут в
        ``QuickObjectTypeInfoDtoNullableResultDto`` (``{entity, isEntityPresent}``);
        обёртка разворачивается здесь, наружу — либо схема, либо ``None``.

        Это инфо о самом ТИПЕ (метаданные типа), а не об экземплярах: для счётчиков
        реальных объектов используйте :meth:`object_type_objects_info`, для перечня
        объектов — :meth:`object_type_objects`.

        Когда применять: чтобы дёшево узнать имя/GUID типа по его id, не загружая полное
        :meth:`object_type_definition`. Аналог по GUID — :meth:`object_type_quick_info_by_guid`.

        Args:
            object_type_id: Идентификатор ТИПА объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ, не ``ObjectID``/``ID`` объекта или версии).

        Returns:
            Краткая информация по схеме :class:`QuickObjectTypeInfo` либо ``None``, если
            тип не найден (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                info = await ips.object_type_quick_info(1742)
                if info is not None:
                    print(info.name, info.guid)

        Notes:
            operationId ``ObjectTypes_GetObjectTypeInfo``; путь
            ``GET /core/api/objectTypes/{objectTypeId}/objectTypeInfo``
            (обёртка ``QuickObjectTypeInfoDtoNullableResultDto``).
        """
        path = f"/core/api/objectTypes/{object_type_id}/objectTypeInfo"
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        return QuickObjectTypeInfo.model_validate(entity) if entity is not None else None
