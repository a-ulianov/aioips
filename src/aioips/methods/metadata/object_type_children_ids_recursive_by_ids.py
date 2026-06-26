"""Метод рекурсивной выборки id потомков для набора типов по их id."""

from ...core import APIManager


class ObjectTypeChildrenIdsRecursiveByIdsMixin(APIManager):
    """Реализует ``POST .../objectTypeTree/children/byIds/recursive/ids``."""

    async def object_type_children_ids_recursive_by_ids(
        self: "ObjectTypeChildrenIdsRecursiveByIdsMixin",
        object_type_ids: list[int],
    ) -> list[int]:
        """Возвращает id всех потомков рекурсивно для НАБОРА типов, заданных их id.

        Пакетный аналог :meth:`children_type_ids_recursive` (один корень): за один запрос
        рекурсивно обходит поддеревья сразу нескольких корневых типов и собирает id их
        потомков на всех уровнях глубины. Результат — объединённый плоский список id без
        гарантии порядка. Операция ЧТЕНИЯ метамодели: POST используется лишь для передачи
        списка корневых id телом, дерево типов не изменяется.

        Когда применять: для фильтров «эти типы и все их подтипы» в пределах одной базы,
        когда корни известны по локальным id. Только локальные потомки —
        :meth:`local_object_type_children_ids_recursive_by_ids`; вариант по GUID —
        :meth:`object_type_children_guids_recursive_by_guids`.

        Args:
            object_type_ids: Список id корневых ТИПОВ объектов (``ObjectTypeID``; локальные).
                Передаётся телом запроса (JSON-массив).

        Returns:
            Список id всех потомков на всех уровнях (``ObjectTypeID``). Пустой список — ни у
            одного корня нет потомков либо входной список пуст.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ids = await ips.object_type_children_ids_recursive_by_ids([1742, 1801])
                print(len(ids))

        Notes:
            operationId ``Metadata_GetObjectTypeChildrenIdsRecursiveByIds``; путь
            ``POST /core/api/metadata/objectTypeTree/children/byIds/recursive/ids``
            (тело — ``list[int]``; ответ — массив ``int``). См. объектной модели IPS.
            Связанные методы: :meth:`local_object_type_children_ids_recursive_by_ids`,
            :meth:`object_type_children_guids_recursive_by_guids`.
        """
        path = "/core/api/metadata/objectTypeTree/children/byIds/recursive/ids"
        data = await self._request("post", path, json=object_type_ids)
        return [int(item) for item in data] if data is not None else []
