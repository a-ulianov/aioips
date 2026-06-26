"""Метод проверки, является ли тип объекта потомком другого типа (по id обоих)."""

from ...core import APIManager


class IsObjectTypeChildMixin(APIManager):
    """Реализует ``GET .../objectTypeTree/isChild/byChildId/{id}/byParentId/{id}``."""

    async def is_object_type_child(
        self: "IsObjectTypeChildMixin",
        child_type_id: int,
        parent_type_id: int,
    ) -> bool:
        """Проверяет, является ли тип потомком другого типа в иерархии (по id обоих).

        Булева проверка отношения предок–потомок в дереве ТИПОВ: входит ли
        ``child_type_id`` в поддерево ``parent_type_id`` (на любой глубине, не только
        прямой потомок). Дешевле, чем извлекать всю цепочку :meth:`parent_type_ids` и
        искать в ней родителя. Ответ сервера — голое булево значение.

        Когда применять: как быстрый предикат «тип A является подтипом B» при фильтрации,
        валидации, маршрутизации по типам. Варианты адресации по GUID —
        :meth:`is_object_type_child_by_child_id_parent_guid` (смешанный) и
        :meth:`is_object_type_child_by_guids` (оба GUID).

        Args:
            child_type_id: Идентификатор предполагаемого ДОЧЕРНЕГО типа (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID`` экземпляра).
            parent_type_id: Идентификатор предполагаемого РОДИТЕЛЬСКОГО типа
                (``ObjectTypeID``, то же id-пространство ТИПОВ объектов).

        Returns:
            ``True`` — ``child_type_id`` входит в поддерево ``parent_type_id``;
            ``False`` — не входит (в т.ч. при отсутствии одного из типов).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.is_object_type_child(1742, 1700):
                    print("1742 — подтип 1700")

        Notes:
            operationId ``Metadata_IsObjectTypeChildOfByChildIdParentId``; путь
            ``GET /core/api/metadata/objectTypeTree/isChild/byChildId/{childTypeId}/``
            ``byParentId/{parentTypeId}`` (ответ — ``boolean``). См. [[ips-object-model]].
            Связанные методы: :meth:`is_object_type_child_by_child_id_parent_guid`,
            :meth:`is_object_type_child_by_guids`.
        """
        path = (
            f"/core/api/metadata/objectTypeTree/isChild/byChildId/{child_type_id}/"
            f"byParentId/{parent_type_id}"
        )
        data = await self._request("get", path)
        return bool(data) if data is not None else False
