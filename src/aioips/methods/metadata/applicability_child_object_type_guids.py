"""Метод получения GUID дочерних типов по id родителя и типа связи."""

from ...core import APIManager


class ApplicabilityChildObjectTypeGuidsMixin(APIManager):
    """Реализует ``GET .../childObjectTypes/byIds/{parentObjectTypeId}/{relationTypeId}/guids``."""

    async def applicability_child_object_type_guids(
        self: "ApplicabilityChildObjectTypeGuidsMixin",
        parent_object_type_id: int,
        relation_type_id: int,
    ) -> list[str] | None:
        """Возвращает GUID дочерних типов, допустимых в составе родителя по одной связи.

        То же, что :meth:`applicability_child_object_type_ids`, но возвращает
        переносимые между базами GUID типов объектов вместо локальных числовых id.
        Перечисляет типы, которые можно включить в состав объекта типа
        ``parent_object_type_id`` по связи ``relation_type_id``. Ответ обёрнут в
        ``GuidListNullableResultDto`` (``{entity, isEntityPresent}``); обёртка
        разворачивается здесь.

        Когда применять: когда дальнейшая логика оперирует переносимыми GUID типов
        (интеграции, сравнение между базами), а не локальными id. Полные описания
        типов по GUID — :meth:`applicability_child_object_types_by_guids`.

        Args:
            parent_object_type_id: Идентификатор типа объекта-РОДИТЕЛЯ
                (``ObjectTypeID`` — id-пространство ТИПОВ объектов, не ``ObjectID``/``ID``).
            relation_type_id: Идентификатор типа связи (``RelationType``).

        Returns:
            Список GUID дочерних типов (строки; ``ObjectType.guid``) либо ``None``,
            если применяемостей нет (``isEntityPresent == false`` / ``entity == null``).
            Пустой список — допустимых потомков по этой связи нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guids = await ips.applicability_child_object_type_guids(1742, 501)
                if guids:
                    print(guids)

        Notes:
            operationId
            ``Metadata_GetApplicabilityChildObjectTypeGuidsByParentIdRelationId``; путь
            ``GET /core/api/metadata/applicabilities/childObjectTypes/byIds/``
            ``{parentObjectTypeId}/{relationTypeId}/guids`` (``GuidListNullableResultDto``).
            См. объектной модели IPS (раздел «Связи и состав»). Связанные методы:
            :meth:`applicability_child_object_type_ids`,
            :meth:`applicability_child_object_types_by_guids`.
        """
        path = (
            "/core/api/metadata/applicabilities/childObjectTypes/byIds/"
            f"{parent_object_type_id}/{relation_type_id}/guids"
        )
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        return list(entity) if entity is not None else None
