"""Метод получения имени типа связи по GUID."""

from uuid import UUID

from ...core import APIManager


class RelationTypeMetaNameByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/relationTypes/byGuid/{guid}/name``."""

    async def relation_type_meta_name_by_guid(
        self: "RelationTypeMetaNameByGuidMixin",
        guid: UUID | str,
    ) -> str:
        """Возвращает прямое имя типа связи по его GUID.

        Лёгкая выборка одного поля по переносимому между базами GUID: прямое имя
        связи (``type_name``, например «Входит в») без загрузки полного описания.
        Обратное имя в результат не входит — см. :meth:`relation_type_meta_by_guid`
        (поле ``reverse_name``). Ответ сервера — голая строка.

        Когда применять: тот же результат, что у :meth:`relation_type_meta_name`,
        но ключ — переносимый GUID (когда числовой ``id`` между базами различается).

        Args:
            guid: Глобальный идентификатор типа связи (``UUID`` или строка).
                Подставляется в URL как есть.

        Returns:
            Прямое имя типа связи. Пустая строка, если сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                name = await ips.relation_type_meta_name_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(name)

        Notes:
            operationId ``Metadata_GetRelationTypeNameByGuid``; путь
            ``GET /core/api/metadata/relationTypes/byGuid/{guid}/name`` (ответ —
            ``string``). Аналог по id — :meth:`relation_type_meta_name`.
        """
        data = await self._request("get", f"/core/api/metadata/relationTypes/byGuid/{guid}/name")
        return "" if data is None else str(data)
