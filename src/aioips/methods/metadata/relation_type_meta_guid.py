"""Метод получения GUID типа связи по идентификатору."""

from ...core import APIManager


class RelationTypeMetaGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/relationTypes/{id}/guid``."""

    async def relation_type_meta_guid(
        self: "RelationTypeMetaGuidMixin",
        relation_type_id: int,
    ) -> str:
        """Возвращает GUID типа связи по его числовому идентификатору.

        Мост «локальный числовой id → переносимый GUID»: числовой ``id``
        (``RelationType``) специфичен для базы, а GUID стабилен между базами. Ответ
        сервера — голая строка (UUID в текстовом виде).

        Когда применять: чтобы по локальному ``id`` получить переносимый GUID для
        сохранения в конфигурации/переноса между инсталляциями IPS. Обратный мост
        (GUID → id) — :meth:`relation_type_meta_id_by_guid`.

        Args:
            relation_type_id: Идентификатор типа связи (``RelationType`` —
                id-пространство ТИПОВ связей, не ``RelationID`` конкретной связи).

        Returns:
            GUID типа связи в текстовом виде. Пустая строка, если сервер вернул
            ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guid = await ips.relation_type_meta_guid(501)
                print(guid)

        Notes:
            operationId ``Metadata_GetRelationTypeGuid``; путь
            ``GET /core/api/metadata/relationTypes/{id}/guid`` (ответ — ``uuid``).
            Обратный мост (GUID → id) — :meth:`relation_type_meta_id_by_guid`.
        """
        path = f"/core/api/metadata/relationTypes/{relation_type_id}/guid"
        data = await self._request("get", path)
        return "" if data is None else str(data)
