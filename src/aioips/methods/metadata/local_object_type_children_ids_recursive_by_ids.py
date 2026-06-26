"""Метод рекурсивной выборки id ЛОКАЛЬНЫХ потомков для набора типов по их id."""

from ...core import APIManager


class LocalObjectTypeChildrenIdsRecursiveByIdsMixin(APIManager):
    """Реализует ``POST .../objectTypeTree/children/byIds/local/recursive/ids``."""

    async def local_object_type_children_ids_recursive_by_ids(
        self: "LocalObjectTypeChildrenIdsRecursiveByIdsMixin",
        object_type_ids: list[int],
    ) -> list[int]:
        """Возвращает id ЛОКАЛЬНЫХ потомков рекурсивно для НАБОРА типов по их id.

        Пакетный и «локальный» аналог :meth:`object_type_children_ids_recursive_by_ids`:
        за один запрос рекурсивно обходит поддеревья нескольких корневых типов, но
        ограничивается ЛОКАЛЬНЫМИ типами (определёнными в текущей базе, без унаследованных
        из родительских/общих метамоделей). Результат — объединённый плоский список id без
        гарантии порядка. Операция ЧТЕНИЯ метамодели: POST лишь передаёт список корневых id
        телом, дерево не изменяется.

        Когда применять: когда нужны только локально определённые подтипы набора корней
        (например, при работе с расширениями метамодели конкретной базы). Полный (не только
        локальный) вариант — :meth:`object_type_children_ids_recursive_by_ids`.

        Args:
            object_type_ids: Список id корневых ТИПОВ объектов (``ObjectTypeID``; локальные).
                Передаётся телом запроса (JSON-массив).

        Returns:
            Список id локальных потомков на всех уровнях (``ObjectTypeID``). Пустой список —
            локальных потомков нет либо входной список пуст.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ids = await ips.local_object_type_children_ids_recursive_by_ids([1742])
                print(ids)

        Notes:
            operationId ``Metadata_GetLocalObjectTypeChildrenIdsRecursiveByIds``; путь
            ``POST /core/api/metadata/objectTypeTree/children/byIds/local/recursive/ids``
            (тело — ``list[int]``; ответ — массив ``int``). См. объектной модели IPS.
            Связанные методы: :meth:`object_type_children_ids_recursive_by_ids`.
        """
        path = "/core/api/metadata/objectTypeTree/children/byIds/local/recursive/ids"
        data = await self._request("post", path, json=object_type_ids)
        return [int(item) for item in data] if data is not None else []
