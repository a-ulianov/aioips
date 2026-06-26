"""Метод получения идентификатора типа связи по GUID."""

from uuid import UUID

from ...core import APIManager


class RelationTypeMetaIdByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/relationTypes/byGuid/{guid}/id``."""

    async def relation_type_meta_id_by_guid(
        self: "RelationTypeMetaIdByGuidMixin",
        guid: UUID | str,
    ) -> int:
        """Возвращает числовой идентификатор типа связи по его GUID.

        Мост «переносимый GUID → локальный числовой id»: GUID типа связи стабилен
        между базами, а числовой ``id`` (``RelationType``) — нет. Ответ сервера —
        целое число, а не объект-обёртка.

        Когда применять: чтобы по GUID получить ``id`` для последующих вызовов,
        требующих ``relationTypeId`` (например, в разделе ``relation_types`` при
        добавлении потомка в состав). Полное метаописание по GUID —
        :meth:`relation_type_meta_by_guid`.

        Args:
            guid: Глобальный идентификатор типа связи (``UUID`` или строка).
                Подставляется в URL как есть.

        Returns:
            Числовой идентификатор типа связи (``RelationType`` — id-пространство
            ТИПОВ связей). Сервер не возвращает ``None``: при отсутствии GUID —
            ошибка.

        Raises:
            IPSError: При ошибочном ответе сервера (в том числе если тип связи с
                таким GUID не найден).

        Example:
            async with IPSClient(config=config) as ips:
                rel_id = await ips.relation_type_meta_id_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(rel_id)

        Notes:
            operationId ``Metadata_GetRelationTypeId``; путь
            ``GET /core/api/metadata/relationTypes/byGuid/{guid}/id``.
            Обратный мост (id → GUID) — :meth:`relation_type_meta_guid`.
        """
        data = await self._request("get", f"/core/api/metadata/relationTypes/byGuid/{guid}/id")
        return int(data)
