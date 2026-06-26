"""Метод выборки GUID дочерних типов по GUID родителя и списку GUID типов связей."""

from urllib.parse import quote

from ...core import APIManager


class ApplicabilityChildObjectTypeGuidsByParentGuidRelationGuidsMixin(APIManager):
    """Реализует ``POST .../childObjectTypes/byGuids/{parentObjectTypeGuid}/guids``."""

    async def applicability_child_object_type_guids_by_parent_guid_relation_guids(
        self: "ApplicabilityChildObjectTypeGuidsByParentGuidRelationGuidsMixin",
        parent_object_type_guid: str,
        relation_type_guids: list[str],
    ) -> list[str] | None:
        """Возвращает GUID дочерних типов состава по GUID родителя и набору GUID связей.

        Пакетный аналог :meth:`applicability_child_object_type_guids_by_guids` (одна связь):
        здесь применяемость проверяется сразу по НЕСКОЛЬКИМ типам связей за один запрос.
        Возвращает плоский список GUID типов объектов, которые допустимо включать в состав
        объекта типа ``parent_object_type_guid`` хотя бы по одной из переданных связей.
        Это операция ЧТЕНИЯ метамодели: глагол POST используется лишь чтобы передать список
        GUID связей телом запроса, схема НЕ изменяется.

        Когда применять: при сборе кандидатов на добавление в состав, когда на руках
        переносимые между базами GUID типа-родителя и нескольких типов связей (интеграция,
        переносимый конфиг). Вариант с числовыми id на выходе —
        :meth:`applicability_child_object_type_ids_by_parent_guid_relation_guids`; адресация
        родителя и связей по локальным id —
        :meth:`applicability_child_object_type_guids_by_parent_id_relation_ids`.

        Args:
            parent_object_type_guid: GUID типа объекта-РОДИТЕЛЯ (``ObjectType.guid``;
                переносим между базами; id-пространство ТИПОВ объектов). Кодируется в URL.
            relation_type_guids: Список GUID типов связей (``RelationType.guid``), по
                которым проверяется применяемость. Передаётся телом запроса (JSON-массив).

        Returns:
            Список GUID допустимых дочерних типов (``ObjectType.guid``) либо ``None``, если
            применяемостей нет (``isEntityPresent == false`` / ``entity == null``). Пустой
            список — допустимых потомков по этим связям нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                parent = "cad001c5-306c-11d8-b4e9-00304f19f545"
                relations = ["11111111-2222-3333-4444-555555555555"]
                method = ips.applicability_child_object_type_guids_by_parent_guid_relation_guids
                guids = await method(parent, relations)
                if guids:
                    print(guids)

        Notes:
            operationId
            ``Metadata_GetApplicabilityChildObjectTypeGuidsByParentGuidRelationGuids``; путь
            ``POST /core/api/metadata/applicabilities/childObjectTypes/byGuids/``
            ``{parentObjectTypeGuid}/guids`` (тело — ``list[str]`` GUID связей; ответ —
            ``GuidListNullableResultDto``). См. [[ips-object-model]] (раздел «Связи и
            состав»). Связанные методы:
            :meth:`applicability_child_object_type_ids_by_parent_guid_relation_guids`.
        """
        encoded_guid = quote(parent_object_type_guid, safe="")
        path = f"/core/api/metadata/applicabilities/childObjectTypes/byGuids/{encoded_guid}/guids"
        data = await self._request("post", path, json=relation_type_guids)
        entity = data.get("entity") if isinstance(data, dict) else None
        return [str(item) for item in entity] if entity is not None else None
