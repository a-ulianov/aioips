"""Метод выборки GUID дочерних типов по id родителя и списку id типов связей."""

from ...core import APIManager


class ApplicabilityChildObjectTypeGuidsByParentIdRelationIdsMixin(APIManager):
    """Реализует ``POST .../childObjectTypes/byIds/{parentObjectTypeId}/guids``."""

    async def applicability_child_object_type_guids_by_parent_id_relation_ids(
        self: "ApplicabilityChildObjectTypeGuidsByParentIdRelationIdsMixin",
        parent_object_type_id: int,
        relation_type_ids: list[int],
    ) -> list[str] | None:
        """Возвращает GUID дочерних типов состава по id родителя и набору id связей.

        Симметричен
        :meth:`applicability_child_object_type_guids_by_parent_guid_relation_guids`, но
        родитель и связи адресуются локальными числовыми ``id`` (не переносимыми GUID), а на
        выходе — GUID типов. Применяемость проверяется сразу по НЕСКОЛЬКИМ типам связей за
        один запрос: возвращает плоский список GUID типов объектов, допустимых к включению в
        состав объекта типа ``parent_object_type_id`` хотя бы по одной из переданных связей.
        Операция ЧТЕНИЯ метамодели: POST используется лишь для передачи списка id связей
        телом, схема НЕ изменяется.

        Когда применять: когда тип-родитель и типы связей известны по локальным id (работа
        в пределах одной базы), а допустимые потомки нужны в виде переносимых GUID (экспорт,
        интеграция). Вариант полностью по GUID —
        :meth:`applicability_child_object_type_guids_by_parent_guid_relation_guids`.

        Args:
            parent_object_type_id: id типа объекта-РОДИТЕЛЯ (``ObjectTypeID``; локальный,
                id-пространство ТИПОВ объектов). Подставляется в путь.
            relation_type_ids: Список id типов связей (``RelationTypeID``), по которым
                проверяется применяемость. Передаётся телом запроса (JSON-массив).

        Returns:
            Список GUID допустимых дочерних типов (``ObjectType.guid``) либо ``None``, если
            применяемостей нет (``isEntityPresent == false`` / ``entity == null``). Пустой
            список — допустимых потомков по этим связям нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guids = await ips.applicability_child_object_type_guids_by_parent_id_relation_ids(
                    1742, [501, 502]
                )
                if guids:
                    print(guids)

        Notes:
            operationId
            ``Metadata_GetApplicabilityChildObjectTypeGuidsByParentIdRelationIds``; путь
            ``POST /core/api/metadata/applicabilities/childObjectTypes/byIds/``
            ``{parentObjectTypeId}/guids`` (тело — ``list[int]`` id связей; ответ —
            ``GuidListNullableResultDto``). См. объектной модели IPS (раздел «Связи и
            состав»). Связанные методы:
            :meth:`applicability_child_object_type_guids_by_parent_guid_relation_guids`.
        """
        path = (
            "/core/api/metadata/applicabilities/childObjectTypes/byIds/"
            f"{parent_object_type_id}/guids"
        )
        data = await self._request("post", path, json=relation_type_ids)
        entity = data.get("entity") if isinstance(data, dict) else None
        return [str(item) for item in entity] if entity is not None else None
