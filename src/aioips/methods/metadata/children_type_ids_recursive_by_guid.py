"""Метод рекурсивного получения id всех дочерних типов поддерева по GUID родителя."""

from urllib.parse import quote

from ...core import APIManager


class ChildrenTypeIdsRecursiveByGuidMixin(APIManager):
    """Реализует ``GET .../objectTypeTree/children/byGuid/{parentTypeGuid}/recursive/ids``."""

    async def children_type_ids_recursive_by_guid(
        self: "ChildrenTypeIdsRecursiveByGuidMixin",
        parent_type_guid: str,
    ) -> list[int]:
        """Возвращает id ВСЕХ потомков типа рекурсивно по GUID родительского типа.

        Вариант :meth:`children_type_ids_recursive` с адресацией корня поддерева по
        переносимому GUID вместо локального ``id``. Рекурсивный обход всего поддерева
        иерархии ТИПОВ: собираются идентификаторы потомков на всех уровнях глубины.
        GUID кодируется в URL. Ответ сервера — плоский массив целых чисел.

        Когда применять: когда тип-корень известен по стабильному GUID, а нужны локальные
        ``id`` всех его наследников (для фильтров «тип и все подтипы», массовых операций).
        Потомки в виде GUID — :meth:`children_type_guids_recursive_by_guid`; адресация по
        id корня — :meth:`children_type_ids_recursive`.

        Args:
            parent_type_guid: GUID типа-КОРНЯ поддерева (строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``); кодируется в URL.

        Returns:
            Список идентификаторов всех потомков типа на всех уровнях (``ObjectTypeID``).
            Пустой список — у типа нет потомков (лист дерева) либо тип не найден.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ids = await ips.children_type_ids_recursive_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(len(ids))

        Notes:
            operationId ``Metadata_GetObjectTypeChildrenIdsRecursiveByGuid``; путь
            ``GET /core/api/metadata/objectTypeTree/children/byGuid/{parentTypeGuid}/``
            ``recursive/ids`` (ответ — массив ``int``). См. [[ips-object-model]].
            Связанные методы: :meth:`children_type_ids_recursive`,
            :meth:`children_type_guids_recursive_by_guid`.
        """
        encoded_guid = quote(parent_type_guid, safe="")
        path = f"/core/api/metadata/objectTypeTree/children/byGuid/{encoded_guid}/recursive/ids"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
