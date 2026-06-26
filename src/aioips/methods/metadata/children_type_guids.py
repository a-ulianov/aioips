"""Метод получения GUID прямых дочерних типов объектов в дереве типов."""

from ...core import APIManager


class ChildrenTypeGuidsMixin(APIManager):
    """Реализует ``GET .../objectTypeTree/children/{parentTypeId}/guids``."""

    async def children_type_guids(
        self: "ChildrenTypeGuidsMixin",
        parent_type_id: int,
    ) -> list[str]:
        """Возвращает GUID ПРЯМЫХ дочерних типов объектов в иерархии типов.

        Дерево типов объектов — иерархия наследования ТИПОВ (не объектов и не состава).
        Метод возвращает только НЕПОСРЕДСТВЕННЫХ потомков заданного типа (один уровень
        вниз) в виде стабильных GUID, без рекурсивного спуска по поддереву. GUID
        переносимы между инсталляциями IPS (в отличие от числового ``id``). Ответ
        сервера — массив строк.

        Когда применять: для обхода иерархии типов по переносимым идентификаторам,
        сверки наборов подтипов между средами. Те же потомки в виде числовых id —
        :meth:`children_type_ids`; всё поддерево целиком —
        :meth:`children_type_guids_recursive`; обращение по GUID родителя —
        :meth:`children_type_guids_by_guid`.

        Args:
            parent_type_id: Идентификатор РОДИТЕЛЬСКОГО типа объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID`` экземпляра).

        Returns:
            Список GUID прямых дочерних типов (строки в id-пространстве ТИПОВ объектов).
            Пустой список — у типа нет потомков (лист дерева) либо тип не найден.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                child_guids = await ips.children_type_guids(1742)
                print(child_guids)

        Notes:
            operationId ``Metadata_GetObjectTypeChildrenGuidsById``; путь
            ``GET /core/api/metadata/objectTypeTree/children/{parentTypeId}/guids``
            (ответ — массив строк). См. объектной модели IPS (иерархия типов).
            Связанные методы: :meth:`children_type_ids`,
            :meth:`children_type_guids_recursive`, :meth:`children_type_guids_by_guid`.
        """
        path = f"/core/api/metadata/objectTypeTree/children/{parent_type_id}/guids"
        data = await self._request("get", path)
        return [str(item) for item in data] if data is not None else []
