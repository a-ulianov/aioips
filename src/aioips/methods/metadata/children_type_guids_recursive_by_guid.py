"""Метод рекурсивного получения GUID всех дочерних типов поддерева по GUID родителя."""

from urllib.parse import quote

from ...core import APIManager


class ChildrenTypeGuidsRecursiveByGuidMixin(APIManager):
    """Реализует ``GET .../objectTypeTree/children/byGuid/{parentTypeGuid}/recursive/guids``."""

    async def children_type_guids_recursive_by_guid(
        self: "ChildrenTypeGuidsRecursiveByGuidMixin",
        parent_type_guid: str,
    ) -> list[str]:
        """Возвращает GUID ВСЕХ потомков типа рекурсивно по GUID родительского типа.

        Полностью GUID-ориентированный рекурсивный вариант: и корень поддерева (вход),
        и все потомки (выход) — переносимые GUID. Рекурсивный обход всего поддерева
        иерархии ТИПОВ: собираются GUID потомков на всех уровнях глубины. GUID
        кодируется в URL. Ответ сервера — плоский массив строк.

        Когда применять: для полной выгрузки/сверки поддерева типов между средами
        исключительно по стабильным GUID, без привязки к локальным ``id``. Потомки в
        виде id — :meth:`children_type_ids_recursive_by_guid`; адресация по id корня —
        :meth:`children_type_guids_recursive`.

        Args:
            parent_type_guid: GUID типа-КОРНЯ поддерева (строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``); кодируется в URL.

        Returns:
            Список GUID всех потомков типа на всех уровнях (строки в id-пространстве
            ТИПОВ объектов). Пустой список — потомков нет (лист) либо тип не найден.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guids = await ips.children_type_guids_recursive_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(len(guids))

        Notes:
            operationId ``Metadata_GetObjectTypeChildrenGuidsRecursiveByGuid``; путь
            ``GET /core/api/metadata/objectTypeTree/children/byGuid/{parentTypeGuid}/``
            ``recursive/guids`` (ответ — массив строк). См. [[ips-object-model]].
            Связанные методы: :meth:`children_type_guids_recursive`,
            :meth:`children_type_ids_recursive_by_guid`.
        """
        encoded_guid = quote(parent_type_guid, safe="")
        path = f"/core/api/metadata/objectTypeTree/children/byGuid/{encoded_guid}/recursive/guids"
        data = await self._request("get", path)
        return [str(item) for item in data] if data is not None else []
