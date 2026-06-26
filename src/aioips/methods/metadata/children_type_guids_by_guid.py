"""Метод получения GUID прямых дочерних типов объектов по GUID родителя."""

from urllib.parse import quote

from ...core import APIManager


class ChildrenTypeGuidsByGuidMixin(APIManager):
    """Реализует ``GET .../objectTypeTree/children/byGuid/{parentTypeGuid}/guids``."""

    async def children_type_guids_by_guid(
        self: "ChildrenTypeGuidsByGuidMixin",
        parent_type_guid: str,
    ) -> list[str]:
        """Возвращает GUID ПРЯМЫХ дочерних типов объектов по GUID родительского типа.

        Полностью GUID-ориентированный вариант: и вход (родитель), и выход (потомки) —
        переносимые GUID. Дерево типов — иерархия наследования ТИПОВ; метод возвращает
        только НЕПОСРЕДСТВЕННЫХ потомков (один уровень вниз), без рекурсии. GUID
        кодируется в URL. Ответ сервера — массив строк.

        Когда применять: для обхода/сверки иерархии типов исключительно по стабильным
        GUID, без привязки к локальным ``id`` конкретной инсталляции. Потомки в виде id —
        :meth:`children_type_ids_by_guid`; всё поддерево —
        :meth:`children_type_guids_recursive_by_guid`; адресация по id родителя —
        :meth:`children_type_guids`.

        Args:
            parent_type_guid: GUID РОДИТЕЛЬСКОГО типа объекта (строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``); кодируется в URL.

        Returns:
            Список GUID прямых дочерних типов (строки в id-пространстве ТИПОВ объектов).
            Пустой список — у типа нет потомков (лист дерева) либо тип не найден.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                child_guids = await ips.children_type_guids_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(child_guids)

        Notes:
            operationId ``Metadata_GetObjectTypeChildrenGuidsByGuid``; путь
            ``GET /core/api/metadata/objectTypeTree/children/byGuid/{parentTypeGuid}/``
            ``guids`` (ответ — массив строк). См. объектной модели IPS (иерархия типов).
            Связанные методы: :meth:`children_type_ids_by_guid`,
            :meth:`children_type_guids`,
            :meth:`children_type_guids_recursive_by_guid`.
        """
        encoded_guid = quote(parent_type_guid, safe="")
        path = f"/core/api/metadata/objectTypeTree/children/byGuid/{encoded_guid}/guids"
        data = await self._request("get", path)
        return [str(item) for item in data] if data is not None else []
