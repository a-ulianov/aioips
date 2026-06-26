"""Метод получения GUID всей цепочки родительских типов по GUID потомка."""

from urllib.parse import quote

from ...core import APIManager


class ParentTypeGuidsByGuidMixin(APIManager):
    """Реализует ``GET .../objectTypeTree/parents/byGuid/{childTypeGuid}/guids``."""

    async def parent_type_guids_by_guid(
        self: "ParentTypeGuidsByGuidMixin",
        child_type_guid: str,
    ) -> list[str]:
        """Возвращает GUID ВСЕЙ цепочки родительских типов по GUID потомка.

        Полностью GUID-ориентированный вариант: и потомок (вход), и все предки (выход) —
        переносимые GUID. Полный путь вверх по дереву ТИПОВ: от непосредственного
        родителя до корня. GUID кодируется в URL. Ответ сервера — массив строк;
        порядок — от ближнего предка к корню.

        Когда применять: для сверки/выгрузки цепочки наследования типа между средами
        исключительно по стабильным GUID, без привязки к локальным ``id``. Предки в виде
        id — :meth:`parent_type_ids_by_guid`; адресация по id потомка —
        :meth:`parent_type_guids`.

        Args:
            child_type_guid: GUID ДОЧЕРНЕГО типа объекта (строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``); кодируется в URL.

        Returns:
            Список GUID всех типов-предков (строки в id-пространстве ТИПОВ объектов) от
            ближайшего родителя к корню. Пустой список — предков нет (корневой) либо
            тип не найден.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ancestor_guids = await ips.parent_type_guids_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(ancestor_guids)

        Notes:
            operationId ``Metadata_GetObjectTypeParentGuidsByGuid``; путь
            ``GET /core/api/metadata/objectTypeTree/parents/byGuid/{childTypeGuid}/``
            ``guids`` (ответ — массив строк). См. [[ips-object-model]] (иерархия типов).
            Связанные методы: :meth:`parent_type_guids`,
            :meth:`parent_type_ids_by_guid`.
        """
        encoded_guid = quote(child_type_guid, safe="")
        path = f"/core/api/metadata/objectTypeTree/parents/byGuid/{encoded_guid}/guids"
        data = await self._request("get", path)
        return [str(item) for item in data] if data is not None else []
