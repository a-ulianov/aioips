"""Метод получения id всей цепочки родительских типов по GUID потомка."""

from urllib.parse import quote

from ...core import APIManager


class ParentTypeIdsByGuidMixin(APIManager):
    """Реализует ``GET .../objectTypeTree/parents/byGuid/{childTypeGuid}/ids``."""

    async def parent_type_ids_by_guid(
        self: "ParentTypeIdsByGuidMixin",
        child_type_guid: str,
    ) -> list[int]:
        """Возвращает id ВСЕЙ цепочки родительских типов по GUID потомка.

        Вариант :meth:`parent_type_ids` с адресацией потомка по переносимому GUID вместо
        локального ``id``. Полный путь вверх по дереву ТИПОВ: от непосредственного
        родителя до корня. GUID кодируется в URL. Ответ сервера — массив целых чисел;
        порядок — от ближнего предка к корню.

        Когда применять: когда тип-потомок известен по стабильному GUID, а нужны
        локальные ``id`` всех его предков. Предки в виде GUID —
        :meth:`parent_type_guids_by_guid`; адресация по id потомка —
        :meth:`parent_type_ids`.

        Args:
            child_type_guid: GUID ДОЧЕРНЕГО типа объекта (строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``); кодируется в URL.

        Returns:
            Список идентификаторов всех типов-предков (``ObjectTypeID``) от ближайшего
            родителя к корню. Пустой список — предков нет (корневой) либо не найден.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ancestors = await ips.parent_type_ids_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(ancestors)

        Notes:
            operationId ``Metadata_GetObjectTypeParentIdsByGuid``; путь
            ``GET /core/api/metadata/objectTypeTree/parents/byGuid/{childTypeGuid}/ids``
            (ответ — массив ``int``). См. [[ips-object-model]] (иерархия типов).
            Связанные методы: :meth:`parent_type_ids`,
            :meth:`parent_type_guids_by_guid`.
        """
        encoded_guid = quote(child_type_guid, safe="")
        path = f"/core/api/metadata/objectTypeTree/parents/byGuid/{encoded_guid}/ids"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
