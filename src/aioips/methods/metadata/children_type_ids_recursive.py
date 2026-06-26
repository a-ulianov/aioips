"""Метод рекурсивного получения id всех дочерних типов поддерева."""

from ...core import APIManager


class ChildrenTypeIdsRecursiveMixin(APIManager):
    """Реализует ``GET .../objectTypeTree/children/{parentTypeId}/recursive/ids``."""

    async def children_type_ids_recursive(
        self: "ChildrenTypeIdsRecursiveMixin",
        parent_type_id: int,
    ) -> list[int]:
        """Возвращает id ВСЕХ потомков типа объекта рекурсивно (всё поддерево).

        Рекурсивный обход поддерева иерархии ТИПОВ: в отличие от
        :meth:`children_type_ids` (только прямые потомки, один уровень), метод спускается
        по всем уровням и собирает идентификаторы всех потомков на любой глубине —
        дети, внуки и далее. Ответ сервера — плоский массив целых чисел.

        Когда применять: когда нужны все подтипы заданного типа целиком — например, для
        фильтра «объекты этого типа и всех его наследников», подсчёта охвата ветви,
        массовых операций по поддереву. Только прямые потомки — :meth:`children_type_ids`;
        то же поддерево в GUID — :meth:`children_type_guids_recursive`; ограничение только
        локальными типами — :meth:`local_children_type_ids_recursive`.

        Args:
            parent_type_id: Идентификатор типа-КОРНЯ поддерева (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID`` экземпляра).

        Returns:
            Список идентификаторов всех потомков типа на всех уровнях (``ObjectTypeID``).
            Пустой список — у типа нет потомков (лист дерева) либо тип не найден.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                all_subtype_ids = await ips.children_type_ids_recursive(1742)
                print(len(all_subtype_ids))

        Notes:
            operationId ``Metadata_GetObjectTypeChildrenIdsRecursiveById``; путь
            ``GET /core/api/metadata/objectTypeTree/children/{parentTypeId}/recursive/``
            ``ids`` (ответ — массив ``int``). См. объектной модели IPS (иерархия типов).
            Связанные методы: :meth:`children_type_ids`,
            :meth:`children_type_guids_recursive`,
            :meth:`local_children_type_ids_recursive`.
        """
        path = f"/core/api/metadata/objectTypeTree/children/{parent_type_id}/recursive/ids"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
