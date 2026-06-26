"""Метод выборки id дочерних типов по GUID родителя и списку GUID типов связей."""

from urllib.parse import quote

from ...core import APIManager


class ApplicabilityChildObjectTypeIdsByParentGuidRelationGuidsMixin(APIManager):
    """Реализует ``POST .../childObjectTypes/byGuids/{parentObjectTypeGuid}/ids``."""

    async def applicability_child_object_type_ids_by_parent_guid_relation_guids(
        self: "ApplicabilityChildObjectTypeIdsByParentGuidRelationGuidsMixin",
        parent_object_type_guid: str,
        relation_type_guids: list[str],
    ) -> list[int] | None:
        """Возвращает id дочерних типов состава по GUID родителя и набору GUID связей.

        То же, что :meth:`applicability_child_object_type_guids_by_parent_guid_relation_guids`,
        но на выходе локальные числовые id типов вместо переносимых GUID. Применяемость
        проверяется сразу по НЕСКОЛЬКИМ типам связей за один запрос. Возвращает плоский
        список id типов объектов, допустимых к включению в состав объекта типа
        ``parent_object_type_guid`` хотя бы по одной из переданных связей. Операция ЧТЕНИЯ
        метамодели: POST применяется лишь для передачи списка GUID связей телом, схема НЕ
        изменяется.

        Когда применять: когда тип-родитель и типы связей известны по переносимым GUID, а
        для дальнейшей фильтрации удобнее локальные ``id`` (массовые операции, индексы).
        Вариант с GUID на выходе —
        :meth:`applicability_child_object_type_guids_by_parent_guid_relation_guids`;
        полностью по локальным id —
        :meth:`applicability_child_object_type_guids_by_parent_id_relation_ids`.

        Args:
            parent_object_type_guid: GUID типа объекта-РОДИТЕЛЯ (``ObjectType.guid``;
                переносим между базами; id-пространство ТИПОВ объектов). Кодируется в URL.
            relation_type_guids: Список GUID типов связей (``RelationType.guid``), по
                которым проверяется применяемость. Передаётся телом запроса (JSON-массив).

        Returns:
            Список id допустимых дочерних типов (``ObjectTypeID``) либо ``None``, если
            применяемостей нет (``isEntityPresent == false`` / ``entity == null``). Пустой
            список — допустимых потомков по этим связям нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                parent = "cad001c5-306c-11d8-b4e9-00304f19f545"
                relations = ["11111111-2222-3333-4444-555555555555"]
                ids = await ips.applicability_child_object_type_ids_by_parent_guid_relation_guids(
                    parent, relations
                )
                if ids:
                    print(ids)

        Notes:
            operationId
            ``Metadata_GetApplicabilityChildObjectTypeIdsByParentGuidRelationGuids``; путь
            ``POST /core/api/metadata/applicabilities/childObjectTypes/byGuids/``
            ``{parentObjectTypeGuid}/ids`` (тело — ``list[str]`` GUID связей; ответ —
            ``Int32ListNullableResultDto``). См. [[ips-object-model]] (раздел «Связи и
            состав»). Связанные методы:
            :meth:`applicability_child_object_type_guids_by_parent_guid_relation_guids`.
        """
        encoded_guid = quote(parent_object_type_guid, safe="")
        path = f"/core/api/metadata/applicabilities/childObjectTypes/byGuids/{encoded_guid}/ids"
        data = await self._request("post", path, json=relation_type_guids)
        entity = data.get("entity") if isinstance(data, dict) else None
        return [int(item) for item in entity] if entity is not None else None
