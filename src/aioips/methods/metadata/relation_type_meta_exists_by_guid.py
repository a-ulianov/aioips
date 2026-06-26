"""Метод проверки существования типа связи по GUID."""

from uuid import UUID

from ...core import APIManager


class RelationTypeMetaExistsByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/relationTypes/byGuid/{guid}/exists``."""

    async def relation_type_meta_exists_by_guid(
        self: "RelationTypeMetaExistsByGuidMixin",
        guid: UUID | str,
    ) -> bool:
        """Проверяет, существует ли тип связи с заданным GUID.

        Дешёвый булев флаг наличия типа связи в метамодели по переносимому между
        базами GUID — без загрузки полного описания. Ответ сервера — голое булево
        значение, без обёртки ``...NullableResultDto``.

        Когда применять: тот же результат, что у :meth:`relation_type_meta_exists`,
        но ключ — переносимый GUID (когда числовой ``id`` между базами различается).

        Args:
            guid: Глобальный идентификатор типа связи (``UUID`` или строка).
                Подставляется в URL как есть.

        Returns:
            ``True`` — тип связи с таким GUID существует; ``False`` — не существует.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                exists = await ips.relation_type_meta_exists_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            operationId ``Metadata_ExistsRelationTypeByGuid``; путь
            ``GET /core/api/metadata/relationTypes/byGuid/{guid}/exists`` (ответ —
            ``boolean``). Аналог по id — :meth:`relation_type_meta_exists`.
        """
        path = f"/core/api/metadata/relationTypes/byGuid/{guid}/exists"
        data = await self._request("get", path)
        return bool(data)
