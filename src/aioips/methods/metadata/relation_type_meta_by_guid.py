"""Метод получения типа связи по GUID."""

from uuid import UUID

from ...core import APIManager
from ...schemas.metadata import RelationTypeMeta


class RelationTypeMetaByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/relationTypes/byGuid/{guid}``."""

    async def relation_type_meta_by_guid(
        self: "RelationTypeMetaByGuidMixin",
        guid: UUID | str,
    ) -> RelationTypeMeta | None:
        """Возвращает описание типа связи по его глобальному идентификатору (GUID).

        GUID типа связи стабилен между базами данных, поэтому удобен как переносимый
        ключ метаданных. Ответ сервера обёрнут в ``...NullableResultDto``
        (``{entity, isEntityPresent}``); обёртка разворачивается здесь, наружу
        отдаётся либо схема, либо ``None``.

        Когда применять: тот же результат, что у :meth:`relation_type_meta`, но
        ключ — переносимый GUID (когда числовой ``id`` между базами различается).
        Полезно для кода, работающего с несколькими инсталляциями IPS.

        Args:
            guid: Глобальный идентификатор типа связи (``UUID`` или строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Подставляется в URL как
                есть.

        Returns:
            Тип связи по схеме :class:`RelationTypeMeta` либо ``None``, если тип с
            таким GUID не найден (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                rel = await ips.relation_type_meta_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                if rel is not None:
                    print(rel.id, rel.type_name)

        Notes:
            operationId ``Metadata_GetRelationTypeByGuid``; путь
            ``GET /core/api/metadata/relationTypes/byGuid/{guid}``.
            Связанный метод по числовому id — :meth:`relation_type_meta`.
        """
        data = await self._request("get", f"/core/api/metadata/relationTypes/byGuid/{guid}")
        entity = data.get("entity") if isinstance(data, dict) else None
        return RelationTypeMeta.model_validate(entity) if entity is not None else None
