"""Метод получения id прямых дочерних типов объектов по GUID родителя."""

from urllib.parse import quote

from ...core import APIManager


class ChildrenTypeIdsByGuidMixin(APIManager):
    """Реализует ``GET .../objectTypeTree/children/byGuid/{parentTypeGuid}/ids``."""

    async def children_type_ids_by_guid(
        self: "ChildrenTypeIdsByGuidMixin",
        parent_type_guid: str,
    ) -> list[int]:
        """Возвращает id ПРЯМЫХ дочерних типов объектов по GUID родительского типа.

        Вариант :meth:`children_type_ids` с адресацией родителя по переносимому GUID
        вместо локального ``id``. Дерево типов — иерархия наследования ТИПОВ; метод
        возвращает только НЕПОСРЕДСТВЕННЫХ потомков (один уровень вниз), без рекурсии.
        GUID кодируется в URL. Ответ сервера — массив целых чисел.

        Когда применять: когда родительский тип известен по стабильному GUID (например,
        из конфигурации, переносимой между средами), а нужны локальные ``id`` его прямых
        потомков. Те же потомки в виде GUID — :meth:`children_type_guids_by_guid`; всё
        поддерево — :meth:`children_type_ids_recursive_by_guid`; адресация по id —
        :meth:`children_type_ids`.

        Args:
            parent_type_guid: GUID РОДИТЕЛЬСКОГО типа объекта (строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``); кодируется в URL.

        Returns:
            Список идентификаторов прямых дочерних типов (``ObjectTypeID``). Пустой
            список — у типа нет потомков (лист дерева) либо тип не найден.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                child_ids = await ips.children_type_ids_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(child_ids)

        Notes:
            operationId ``Metadata_GetObjectTypeChildrenIdsByGuid``; путь
            ``GET /core/api/metadata/objectTypeTree/children/byGuid/{parentTypeGuid}/ids``
            (ответ — массив ``int``). См. [[ips-object-model]] (иерархия типов).
            Связанные методы: :meth:`children_type_ids`,
            :meth:`children_type_guids_by_guid`,
            :meth:`children_type_ids_recursive_by_guid`.
        """
        encoded_guid = quote(parent_type_guid, safe="")
        path = f"/core/api/metadata/objectTypeTree/children/byGuid/{encoded_guid}/ids"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
