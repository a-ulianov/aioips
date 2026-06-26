"""Метод выборки GUID верхних разрешённых родительских типов для набора типов."""

from ...core import APIManager


class TopParentEnabledObjectTypeGuidsByGuidsMixin(APIManager):
    """Реализует ``POST .../objectTypeTree/topParents/byGuids/guids``."""

    async def top_parent_enabled_object_type_guids_by_guids(
        self: "TopParentEnabledObjectTypeGuidsByGuidsMixin",
        object_type_guids: list[str],
    ) -> list[str]:
        """Возвращает GUID верхних РАЗРЕШЁННЫХ родительских типов для НАБОРА типов по GUID.

        Для каждого переданного типа поднимается по дереву до самого верхнего РАЗРЕШЁННОГО
        (включённого в применяемость) предка и собирает их GUID. В отличие от безусловной
        вершины дерева, «enabled» учитывает применяемость: возвращаются корни в пределах
        разрешённой иерархии. Результат — плоский список GUID без дублей/порядка. Операция
        ЧТЕНИЯ метамодели: POST используется лишь для передачи списка GUID телом.

        Когда применять: при группировке/нормализации набора типов до их разрешённых
        верхних родителей (например, для построения корневых узлов дерева выбора). Вариант
        по локальным id — :meth:`top_parent_enabled_object_type_ids_by_ids`.

        Args:
            object_type_guids: Список GUID ТИПОВ объектов (``ObjectType.guid``; переносимы
                между базами). Передаётся телом запроса (JSON-массив).

        Returns:
            Список GUID верхних разрешённых родительских ТИПОВ (``ObjectType.guid``). Пустой
            список — нет разрешённых родителей либо входной список пуст.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                roots = await ips.top_parent_enabled_object_type_guids_by_guids(
                    ["cad001c5-306c-11d8-b4e9-00304f19f545"]
                )
                print(roots)

        Notes:
            operationId ``Metadata_GetTopParentEnabledObjectTypeGuidsByGuids``; путь
            ``POST /core/api/metadata/objectTypeTree/topParents/byGuids/guids`` (тело —
            ``list[str]``; ответ — массив ``str``). См. объектной модели IPS. Связанные
            методы: :meth:`top_parent_enabled_object_type_ids_by_ids`.
        """
        path = "/core/api/metadata/objectTypeTree/topParents/byGuids/guids"
        data = await self._request("post", path, json=object_type_guids)
        return [str(item) for item in data] if data is not None else []
