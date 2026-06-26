"""Метод выборки id верхних разрешённых родительских типов для набора типов."""

from ...core import APIManager


class TopParentEnabledObjectTypeIdsByIdsMixin(APIManager):
    """Реализует ``POST .../objectTypeTree/topParents/byIds/ids``."""

    async def top_parent_enabled_object_type_ids_by_ids(
        self: "TopParentEnabledObjectTypeIdsByIdsMixin",
        object_type_ids: list[int],
    ) -> list[int]:
        """Возвращает id верхних РАЗРЕШЁННЫХ родительских типов для НАБОРА типов по их id.

        Аналог :meth:`top_parent_enabled_object_type_guids_by_guids` с адресацией по
        локальным числовым ``id``: для каждого переданного типа поднимается по дереву до
        самого верхнего РАЗРЕШЁННОГО (включённого в применяемость) предка и собирает их id.
        «enabled» учитывает применяемость: возвращаются корни в пределах разрешённой
        иерархии. Результат — плоский список id без дублей/порядка. Операция ЧТЕНИЯ
        метамодели: POST используется лишь для передачи списка id телом.

        Когда применять: при группировке/нормализации набора типов до их разрешённых
        верхних родителей в пределах одной базы. Вариант по GUID —
        :meth:`top_parent_enabled_object_type_guids_by_guids`.

        Args:
            object_type_ids: Список id ТИПОВ объектов (``ObjectTypeID``; локальные).
                Передаётся телом запроса (JSON-массив).

        Returns:
            Список id верхних разрешённых родительских ТИПОВ (``ObjectTypeID``). Пустой
            список — нет разрешённых родителей либо входной список пуст.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                roots = await ips.top_parent_enabled_object_type_ids_by_ids([1742, 1801])
                print(roots)

        Notes:
            operationId ``Metadata_GetTopParentEnabledObjectTypeIdsByIds``; путь
            ``POST /core/api/metadata/objectTypeTree/topParents/byIds/ids`` (тело —
            ``list[int]``; ответ — массив ``int``). См. [[ips-object-model]]. Связанные
            методы: :meth:`top_parent_enabled_object_type_guids_by_guids`.
        """
        path = "/core/api/metadata/objectTypeTree/topParents/byIds/ids"
        data = await self._request("post", path, json=object_type_ids)
        return [int(item) for item in data] if data is not None else []
