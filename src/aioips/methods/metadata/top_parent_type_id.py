"""Метод получения id корневого (верхнего) типа в ветви иерархии типов."""

from ...core import APIManager


class TopParentTypeIdMixin(APIManager):
    """Реализует ``GET .../objectTypeTree/topParent/{childTypeId}/id``."""

    async def top_parent_type_id(
        self: "TopParentTypeIdMixin",
        child_type_id: int,
    ) -> int:
        """Возвращает id КОРНЕВОГО типа ветви иерархии для заданного типа.

        Поднимается по дереву ТИПОВ до самого верха и возвращает идентификатор корневого
        предка (типа без родителя), которому принадлежит заданный тип. Это «голова»
        всей цепочки :meth:`parent_type_ids` — последний элемент при движении вверх.
        Ответ сервера — целое число.

        Когда применять: для группировки типов по корневым ветвям дерева, определения
        к какой верхнеуровневой категории относится тип. Вся цепочка предков —
        :meth:`parent_type_ids`; перечень всех корневых типов —
        :meth:`top_object_type_ids`.

        Args:
            child_type_id: Идентификатор типа объекта (``ObjectTypeID`` — id-пространство
                ТИПОВ объектов, не ``ObjectID``/``ID`` экземпляра).

        Returns:
            Идентификатор корневого типа ветви (``ObjectTypeID``). Если заданный тип сам
            корневой — возвращается его собственный ``id``. ``0`` — тип не найден.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                root_id = await ips.top_parent_type_id(1742)
                print(root_id)

        Notes:
            operationId ``Metadata_GetTopParentObjectTypeId``; путь
            ``GET /core/api/metadata/objectTypeTree/topParent/{childTypeId}/id``
            (ответ — ``int``). См. [[ips-object-model]] (иерархия типов).
            Связанные методы: :meth:`parent_type_ids`, :meth:`top_object_type_ids`.
        """
        path = f"/core/api/metadata/objectTypeTree/topParent/{child_type_id}/id"
        data = await self._request("get", path)
        return int(data) if data is not None else 0
