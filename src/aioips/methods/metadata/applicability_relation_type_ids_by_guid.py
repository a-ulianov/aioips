"""Метод получения id типов связей применяемости по GUID типа объекта."""

from uuid import UUID

from ...core import APIManager


class ApplicabilityRelationTypeIdsByGuidMixin(APIManager):
    """Реализует ``GET .../applicabilityRelationTypes/byGuid/{objectTypeGuid}/ids``."""

    async def applicability_relation_type_ids_by_guid(
        self: "ApplicabilityRelationTypeIdsByGuidMixin",
        object_type_guid: UUID | str,
    ) -> list[int]:
        """Возвращает id типов связей применяемости типа объекта, адресованного по GUID.

        То же, что :meth:`applicability_relation_type_ids`, но тип объекта задаётся
        переносимым между базами GUID, а не локальным числовым id. Перечисляет
        идентификаторы типов связи (``RelationType``), по которым у типа вообще
        настроены применяемости — без различения роли «родитель/потомок». Это
        «алфавит связей» состава для типа. Ответ — голый массив целых (без обёртки
        ``...NullableResultDto``), поэтому метод всегда отдаёт список, а не ``None``.

        Когда применять: когда на руках GUID типа объекта (переносимый конфиг,
        интеграция между базами) и нужен набор релевантных типов связи — чтобы затем
        адресно запросить потомков по конкретной связи
        (:meth:`applicability_child_object_type_ids_by_guids`). Возврат в
        GUID-пространстве связей — :meth:`applicability_relation_type_guids_by_guid`;
        аналог по числовому id типа объекта — :meth:`applicability_relation_type_ids`.

        Args:
            object_type_guid: GUID типа объекта (``ObjectType.guid`` — переносим между
                базами; id-пространство ТИПОВ объектов, не ``objectGUID`` конкретного
                объекта). Подставляется в URL как есть (``UUID`` или строка).

        Returns:
            Список идентификаторов типов связи (``RelationType``). Пустой список —
            у типа нет применяемостей ни по одной связи (или тип с таким GUID не
            найден: сервер отдаёт пустую коллекцию, а не ошибку).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guid = "cad001c5-306c-11d8-b4e9-00304f19f545"
                relation_ids = await ips.applicability_relation_type_ids_by_guid(guid)
                print(relation_ids)

        Notes:
            operationId ``Metadata_GetApplicabilityRelationTypeIdsByGuid``; путь
            ``GET /core/api/metadata/applicabilities/applicabilityRelationTypes/``
            ``byGuid/{objectTypeGuid}/ids`` (голый массив ``int``). См.
            объектной модели IPS (раздел «Связи и состав»). Связанные методы:
            :meth:`applicability_relation_type_ids`,
            :meth:`applicability_relation_type_guids_by_guid`.
        """
        path = (
            "/core/api/metadata/applicabilities/applicabilityRelationTypes/"
            f"byGuid/{object_type_guid}/ids"
        )
        data = await self._request("get", path)
        items = data if isinstance(data, list) else []
        return [int(item) for item in items]
