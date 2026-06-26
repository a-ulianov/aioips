"""Метод получения GUID всех дочерних типов объекта."""

from urllib.parse import quote
from uuid import UUID

from ...core import APIManager


class ObjectTypeAllChildGuidsMixin(APIManager):
    """Реализует метод ``GET /core/api/objectTypes/byGuid/{objectTypeGuid}/allChildGuids``."""

    async def object_type_all_child_guids(
        self: "ObjectTypeAllChildGuidsMixin",
        object_type_guid: UUID | str,
    ) -> list[str]:
        """Возвращает GUID всех дочерних ТИПОВ заданного типа объекта.

        Перечисляет глобальные идентификаторы типов, унаследованных от заданного
        (потомки в иерархии типов). Речь о ТИПАХ-потомках (структура метамодели типов),
        а не об экземплярах объектов: для реальных объектов типа используйте
        :meth:`object_type_object_ids` / :meth:`object_type_objects`.

        Когда применять: чтобы обойти поддерево типов (например, найти все конкретные
        типы под абстрактным родителем) и затем по каждому GUID получить определение
        через :meth:`object_type_definition_by_guid` или объекты через методы раздела.
        Ключом служит переносимый GUID типа.

        Args:
            object_type_guid: Глобальный идентификатор ТИПА-родителя (``UUID`` или строка
                вида ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Кодируется в URL.

        Returns:
            Список GUID дочерних типов в строковом представлении. Пустой список означает,
            что у типа нет дочерних типов.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                child_guids = await ips.object_type_all_child_guids(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(len(child_guids))

        Notes:
            operationId ``ObjectTypes_GetObjectTypeChildObjectInfoCollection``; путь
            ``GET /core/api/objectTypes/byGuid/{objectTypeGuid}/allChildGuids``
            (массив ``uuid``).
        """
        encoded = quote(str(object_type_guid), safe="")
        path = f"/core/api/objectTypes/byGuid/{encoded}/allChildGuids"
        data = await self._request("get", path)
        return [str(item) for item in data]
