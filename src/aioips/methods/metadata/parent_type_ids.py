"""Метод получения id всей цепочки родительских типов объекта."""

from ...core import APIManager


class ParentTypeIdsMixin(APIManager):
    """Реализует ``GET .../objectTypeTree/parents/{childTypeId}/ids``."""

    async def parent_type_ids(
        self: "ParentTypeIdsMixin",
        child_type_id: int,
    ) -> list[int]:
        """Возвращает id ВСЕЙ цепочки родительских типов (предков) в иерархии типов.

        Полный путь вверх по дереву ТИПОВ: от непосредственного родителя заданного типа
        до корня — список идентификаторов всех типов-предков. В отличие от
        :meth:`parent_type_id` (только ближайший родитель) — вся ветвь наследования.
        Ответ сервера — массив целых чисел; порядок — от ближнего предка к корню.

        Когда применять: для проверки принадлежности типа ветви, построения «хлебных
        крошек» по иерархии, определения всех супертипов. Обратный порядок (от корня
        вниз) — :meth:`parent_type_ids_reverse`; предки в виде GUID —
        :meth:`parent_type_guids`; только ближайший родитель — :meth:`parent_type_id`.

        Args:
            child_type_id: Идентификатор ДОЧЕРНЕГО типа объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID`` экземпляра).

        Returns:
            Список идентификаторов всех типов-предков (``ObjectTypeID``) от ближайшего
            родителя к корню. Пустой список — у типа нет предков (корневой) либо не найден.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ancestors = await ips.parent_type_ids(1742)
                print(ancestors)

        Notes:
            operationId ``Metadata_GetObjectTypeParentIdsById``; путь
            ``GET /core/api/metadata/objectTypeTree/parents/{childTypeId}/ids``
            (ответ — массив ``int``). См. [[ips-object-model]] (иерархия типов).
            Связанные методы: :meth:`parent_type_id`, :meth:`parent_type_guids`,
            :meth:`parent_type_ids_reverse`.
        """
        path = f"/core/api/metadata/objectTypeTree/parents/{child_type_id}/ids"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
