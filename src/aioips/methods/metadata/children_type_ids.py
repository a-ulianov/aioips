"""Метод получения id прямых дочерних типов объектов в дереве типов."""

from ...core import APIManager


class ChildrenTypeIdsMixin(APIManager):
    """Реализует ``GET .../objectTypeTree/children/{parentTypeId}/ids``."""

    async def children_type_ids(
        self: "ChildrenTypeIdsMixin",
        parent_type_id: int,
    ) -> list[int]:
        """Возвращает id ПРЯМЫХ дочерних типов объектов в иерархии типов.

        Дерево типов объектов — это иерархия наследования ТИПОВ (не объектов и не
        состава): у каждого типа есть родительский тип и непосредственные потомки.
        Метод возвращает только НЕПОСРЕДСТВЕННЫХ потомков заданного типа (один уровень
        вниз), без рекурсивного спуска по поддереву. Ответ сервера — массив целых чисел.

        Когда применять: для пошагового обхода иерархии типов сверху вниз, построения
        веток дерева в UI, выбора подтипов одного уровня. Для всего поддерева целиком —
        :meth:`children_type_ids_recursive`; те же потомки в виде GUID —
        :meth:`children_type_guids`; обращение по GUID родителя —
        :meth:`children_type_ids_by_guid`.

        Args:
            parent_type_id: Идентификатор РОДИТЕЛЬСКОГО типа объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID`` экземпляра).

        Returns:
            Список идентификаторов прямых дочерних типов (``ObjectTypeID``). Пустой
            список — у типа нет потомков (лист дерева) либо тип не найден.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                child_ids = await ips.children_type_ids(1742)
                print(child_ids)

        Notes:
            operationId ``Metadata_GetObjectTypeChildrenIdsById``; путь
            ``GET /core/api/metadata/objectTypeTree/children/{parentTypeId}/ids``
            (ответ — массив ``int``). См. объектной модели IPS (иерархия типов).
            Связанные методы: :meth:`children_type_guids`,
            :meth:`children_type_ids_recursive`, :meth:`children_type_ids_by_guid`.
        """
        path = f"/core/api/metadata/objectTypeTree/children/{parent_type_id}/ids"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
