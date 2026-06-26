"""Метод получения GUID всей цепочки родительских типов объекта."""

from ...core import APIManager


class ParentTypeGuidsMixin(APIManager):
    """Реализует ``GET .../objectTypeTree/parents/{childTypeId}/guids``."""

    async def parent_type_guids(
        self: "ParentTypeGuidsMixin",
        child_type_id: int,
    ) -> list[str]:
        """Возвращает GUID ВСЕЙ цепочки родительских типов (предков) в иерархии типов.

        Полный путь вверх по дереву ТИПОВ в виде стабильных GUID: от непосредственного
        родителя заданного типа до корня. В отличие от :meth:`parent_type_id` (только
        ближайший родитель) — вся ветвь наследования. GUID переносимы между
        инсталляциями. Ответ сервера — массив строк; порядок — от ближнего предка к корню.

        Когда применять: для сверки цепочки наследования типа между средами по
        переносимым GUID, проверки принадлежности ветви. Те же предки в числовых id —
        :meth:`parent_type_ids`; адресация по GUID потомка —
        :meth:`parent_type_guids_by_guid`.

        Args:
            child_type_id: Идентификатор ДОЧЕРНЕГО типа объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID`` экземпляра).

        Returns:
            Список GUID всех типов-предков (строки в id-пространстве ТИПОВ объектов) от
            ближайшего родителя к корню. Пустой список — предков нет (корневой) либо
            тип не найден.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ancestor_guids = await ips.parent_type_guids(1742)
                print(ancestor_guids)

        Notes:
            operationId ``Metadata_GetObjectTypeParentGuidsById``; путь
            ``GET /core/api/metadata/objectTypeTree/parents/{childTypeId}/guids``
            (ответ — массив строк). См. [[ips-object-model]] (иерархия типов).
            Связанные методы: :meth:`parent_type_ids`,
            :meth:`parent_type_guids_by_guid`.
        """
        path = f"/core/api/metadata/objectTypeTree/parents/{child_type_id}/guids"
        data = await self._request("get", path)
        return [str(item) for item in data] if data is not None else []
