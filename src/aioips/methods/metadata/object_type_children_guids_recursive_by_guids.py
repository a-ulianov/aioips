"""Метод рекурсивной выборки GUID потомков для набора типов по их GUID."""

from ...core import APIManager


class ObjectTypeChildrenGuidsRecursiveByGuidsMixin(APIManager):
    """Реализует ``POST .../objectTypeTree/children/byGuids/recursive/guids``."""

    async def object_type_children_guids_recursive_by_guids(
        self: "ObjectTypeChildrenGuidsRecursiveByGuidsMixin",
        object_type_guids: list[str],
    ) -> list[str]:
        """Возвращает GUID всех потомков рекурсивно для НАБОРА типов, заданных их GUID.

        Пакетный аналог :meth:`children_type_guids_recursive_by_guid` (один корень): за один
        запрос рекурсивно обходит поддеревья сразу нескольких корневых типов и собирает GUID
        их потомков на всех уровнях глубины. Результат — объединённый плоский список без
        гарантии порядка. Операция ЧТЕНИЯ метамодели: POST используется лишь для передачи
        списка корневых GUID телом, дерево типов не изменяется.

        Когда применять: для фильтров вида «эти типы и все их подтипы», когда корни известны
        по переносимым GUID (интеграция, переносимый конфиг). Вариант по локальным id —
        :meth:`object_type_children_ids_recursive_by_ids`.

        Args:
            object_type_guids: Список GUID корневых ТИПОВ объектов (``ObjectType.guid``;
                переносимы между базами). Передаётся телом запроса (JSON-массив).

        Returns:
            Список GUID всех потомков на всех уровнях (``ObjectType.guid``). Пустой список —
            ни у одного корня нет потомков либо входной список пуст.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guids = await ips.object_type_children_guids_recursive_by_guids(
                    ["cad001c5-306c-11d8-b4e9-00304f19f545"]
                )
                print(len(guids))

        Notes:
            operationId ``Metadata_GetObjectTypeChildrenGuidsRecursiveByGuids``; путь
            ``POST /core/api/metadata/objectTypeTree/children/byGuids/recursive/guids``
            (тело — ``list[str]``; ответ — массив ``str``). См. [[ips-object-model]].
            Связанные методы: :meth:`object_type_children_ids_recursive_by_ids`.
        """
        path = "/core/api/metadata/objectTypeTree/children/byGuids/recursive/guids"
        data = await self._request("post", path, json=object_type_guids)
        return [str(item) for item in data] if data is not None else []
