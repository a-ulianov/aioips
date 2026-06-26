"""Метод рекурсивного получения id только локальных дочерних типов поддерева."""

from ...core import APIManager


class LocalChildrenTypeIdsRecursiveMixin(APIManager):
    """Реализует ``GET .../objectTypeTree/children/{parentTypeId}/local/recursive/ids``."""

    async def local_children_type_ids_recursive(
        self: "LocalChildrenTypeIdsRecursiveMixin",
        parent_type_id: int,
    ) -> list[int]:
        """Возвращает id ЛОКАЛЬНЫХ потомков типа объекта рекурсивно (всё поддерево).

        Как :meth:`children_type_ids_recursive`, но ограничивает результат только
        ЛОКАЛЬНЫМИ типами объектов — теми, что определены в текущей базе, а не
        унаследованы из общей (системной) части метамодели. Рекурсивный обход поддерева
        иерархии ТИПОВ с фильтром по признаку локальности. Ответ сервера — плоский
        массив целых чисел.

        Когда применять: когда нужны только пользовательские/локальные подтипы ветви —
        например, при выгрузке кастомизаций конкретной БД без общесистемных типов.
        Признак локальности отдельного типа — :meth:`object_type_is_local`; все потомки
        без фильтра — :meth:`children_type_ids_recursive`.

        Args:
            parent_type_id: Идентификатор типа-КОРНЯ поддерева (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID`` экземпляра).

        Returns:
            Список идентификаторов локальных потомков типа на всех уровнях
            (``ObjectTypeID``). Пустой список — локальных потомков нет либо тип не найден.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                local_ids = await ips.local_children_type_ids_recursive(1742)
                print(local_ids)

        Notes:
            operationId ``Metadata_GetLocalObjectTypeChildrenIdsRecursiveById``; путь
            ``GET /core/api/metadata/objectTypeTree/children/{parentTypeId}/local/``
            ``recursive/ids`` (ответ — массив ``int``). См. объектной модели IPS.
            Связанные методы: :meth:`children_type_ids_recursive`,
            :meth:`object_type_is_local`.
        """
        path = f"/core/api/metadata/objectTypeTree/children/{parent_type_id}/local/recursive/ids"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
