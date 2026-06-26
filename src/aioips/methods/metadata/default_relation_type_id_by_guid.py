"""Метод получения id типа связи по умолчанию по GUID типа объекта-родителя."""

from uuid import UUID

from ...core import APIManager


class DefaultRelationTypeIdByGuidMixin(APIManager):
    """Реализует ``GET .../objectTypeDefault/byGuid/{parentObjectTypeGuid}/id``."""

    async def default_relation_type_id_by_guid(
        self: "DefaultRelationTypeIdByGuidMixin",
        parent_object_type_guid: UUID | str,
    ) -> int:
        """Возвращает id типа связи по умолчанию по GUID типа объекта-родителя.

        То же, что :meth:`default_relation_type_id`, но тип объекта-родителя задаётся
        переносимым между базами GUID, а не локальным числовым id. Возвращает
        локальный числовой id типа связи по умолчанию (``RelationType``). Ответ
        сервера — целое число, а не объект-обёртка.

        Когда применять: при построении состава, когда на руках GUID типа объекта
        (переносимый ключ), а нужен числовой ``relationTypeId``. Вариант с GUID связи
        на выходе — :meth:`default_relation_type_guid_by_guid`.

        Args:
            parent_object_type_guid: Глобальный идентификатор типа объекта-РОДИТЕЛЯ
                (``UUID`` или строка). Это GUID ТИПА объекта, не GUID конкретного
                объекта/версии. Подставляется в URL как есть.

        Returns:
            Числовой идентификатор типа связи по умолчанию (``RelationType``). Сервер
            не возвращает ``None``: при отсутствии типа/связи — ошибка.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                rel_id = await ips.default_relation_type_id_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(rel_id)

        Notes:
            operationId ``Metadata_GetDefaultRelationTypeIdByGuid``; путь
            ``GET /core/api/metadata/relationTypes/objectTypeDefault/byGuid/``
            ``{parentObjectTypeGuid}/id``. Парный метод (GUID связи) —
            :meth:`default_relation_type_guid_by_guid`.
        """
        path = (
            f"/core/api/metadata/relationTypes/objectTypeDefault/byGuid/"
            f"{parent_object_type_guid}/id"
        )
        data = await self._request("get", path)
        return int(data)
