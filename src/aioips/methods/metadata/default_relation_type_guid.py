"""Метод получения GUID типа связи по умолчанию для типа объекта-родителя."""

from ...core import APIManager


class DefaultRelationTypeGuidMixin(APIManager):
    """Реализует ``GET .../relationTypes/objectTypeDefault/{parentObjectTypeId}/guid``."""

    async def default_relation_type_guid(
        self: "DefaultRelationTypeGuidMixin",
        parent_object_type_id: int,
    ) -> str:
        """Возвращает GUID типа связи по умолчанию для заданного типа объекта-родителя.

        То же, что :meth:`default_relation_type_id`, но возвращает переносимый между
        базами GUID типа связи по умолчанию (а не локальный числовой id). Ответ
        сервера — голая строка (UUID в текстовом виде).

        Когда применять: при программном построении состава, когда нужен переносимый
        идентификатор связи по умолчанию (например, для сохранения в конфигурации).
        Вариант с GUID типа объекта на входе —
        :meth:`default_relation_type_guid_by_guid`.

        Args:
            parent_object_type_id: Идентификатор типа объекта-РОДИТЕЛЯ
                (``ObjectTypeID`` — id-пространство ТИПОВ объектов, не ``ObjectID``/
                ``ID`` конкретного объекта или версии).

        Returns:
            GUID типа связи по умолчанию в текстовом виде. Пустая строка, если сервер
            вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guid = await ips.default_relation_type_guid(1742)
                print(guid)

        Notes:
            operationId ``Metadata_GetDefaultRelationTypeGuidById``; путь
            ``GET /core/api/metadata/relationTypes/objectTypeDefault/``
            ``{parentObjectTypeId}/guid`` (ответ — ``uuid``). Парный метод (id связи) —
            :meth:`default_relation_type_id`.
        """
        path = f"/core/api/metadata/relationTypes/objectTypeDefault/{parent_object_type_id}/guid"
        data = await self._request("get", path)
        return "" if data is None else str(data)
