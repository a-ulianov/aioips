"""Метод получения id дочерних типов объектов, допустимых в составе родителя."""

from ...core import APIManager


class ChildObjectTypeIdsMixin(APIManager):
    """Реализует ``POST .../applicabilities/childObjectTypes/byIds/{parentObjectTypeId}/ids``."""

    async def child_object_type_ids(
        self: "ChildObjectTypeIdsMixin",
        parent_object_type_id: int,
        relation_type_ids: list[int],
    ) -> list[int] | None:
        """Возвращает id дочерних типов, допустимых в составе родителя по заданным связям.

        Свёртка применяемостей до плоского списка идентификаторов: какие типы объектов
        можно включить в состав объекта типа ``parent_object_type_id``, если связь —
        одного из типов ``relation_type_ids``. Несмотря на чтение, эндпоинт — ``POST``:
        список типов связей передаётся телом запроса. Ответ обёрнут в
        ``...ListNullableResultDto`` (``{entity, isEntityPresent}``, ``entity`` — массив
        или ``null``); обёртка разворачивается здесь, наружу отдаётся либо список int,
        либо ``None``.

        Когда применять: когда нужен только перечень допустимых дочерних ТИПОВ (а не
        полные правила со схемой :class:`ObjectTypeApplicability`) — например, чтобы
        отфильтровать кандидатов на добавление в состав по конкретным типам связи.
        За полными правилами обращайтесь к :meth:`object_type_applicabilities`.
        ``relation_type_ids`` берутся из ``relation_type_id`` применяемостей родителя.

        Args:
            parent_object_type_id: Идентификатор типа объекта-РОДИТЕЛЯ (``ObjectTypeID``
                — id-пространство ТИПОВ объектов, не ``ObjectID``/``ID``).
            relation_type_ids: Список идентификаторов типов связи (``RelationType``),
                по которым ограничивается поиск допустимых потомков; передаётся телом
                запроса. Пустой список вернёт пустую/``None`` выборку.

        Returns:
            Список идентификаторов дочерних типов объектов (``ObjectTypeID``) либо
            ``None``, если применяемостей нет (``isEntityPresent == false`` /
            ``entity == null``). Пустой список — допустимых потомков по этим связям нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                type_ids = await ips.child_object_type_ids(1742, [501])
                if type_ids:
                    print(type_ids)

        Notes:
            operationId ``Metadata_GetApplicabilityChildObjectTypeIdsByParentIdRelationIds``;
            путь ``POST /core/api/metadata/applicabilities/childObjectTypes/byIds/``
            ``{parentObjectTypeId}/ids`` (тело — массив id типов связи, ответ —
            ``Int32ListNullableResultDto``). См. объектной модели IPS
            (раздел «Связи и состав»). Связанный метод:
            :meth:`object_type_applicabilities`.
        """
        path = (
            f"/core/api/metadata/applicabilities/childObjectTypes/byIds/{parent_object_type_id}/ids"
        )
        data = await self._request("post", path, json=relation_type_ids)
        entity = data.get("entity") if isinstance(data, dict) else None
        if entity is None:
            return None
        return [int(item) for item in entity]
