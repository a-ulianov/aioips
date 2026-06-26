"""Метод получения id типа связи по умолчанию для типа объекта-родителя."""

from ...core import APIManager


class DefaultRelationTypeIdMixin(APIManager):
    """Реализует ``GET .../relationTypes/objectTypeDefault/{parentObjectTypeId}/id``."""

    async def default_relation_type_id(
        self: "DefaultRelationTypeIdMixin",
        parent_object_type_id: int,
    ) -> int:
        """Возвращает id типа связи по умолчанию для заданного типа объекта-родителя.

        У типа объекта может быть задан тип связи по умолчанию (``default_relation``),
        который используется при добавлении потомка в состав, если тип связи не указан
        явно. Этот метод отдаёт его числовой идентификатор по ``id`` типа-родителя.
        Ответ сервера — целое число, а не объект-обёртка.

        Когда применять: при программном построении состава, чтобы подобрать связь по
        умолчанию для родительского типа (раздел ``relation_types``). Полное
        метаописание полученного типа связи — :meth:`relation_type_meta`. Вариант с
        GUID типа объекта — :meth:`default_relation_type_id_by_guid`.

        Args:
            parent_object_type_id: Идентификатор типа объекта-РОДИТЕЛЯ
                (``ObjectTypeID`` — id-пространство ТИПОВ объектов, не ``ObjectID``/
                ``ID`` конкретного объекта или версии).

        Returns:
            Числовой идентификатор типа связи по умолчанию (``RelationType``). Сервер
            не возвращает ``None``: при отсутствии типа/связи — ошибка.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                rel_id = await ips.default_relation_type_id(1742)
                print(rel_id)

        Notes:
            operationId ``Metadata_GetDefaultRelationTypeIdById``; путь
            ``GET /core/api/metadata/relationTypes/objectTypeDefault/``
            ``{parentObjectTypeId}/id``. Парный метод (GUID связи) —
            :meth:`default_relation_type_guid`.
        """
        path = f"/core/api/metadata/relationTypes/objectTypeDefault/{parent_object_type_id}/id"
        data = await self._request("get", path)
        return int(data)
