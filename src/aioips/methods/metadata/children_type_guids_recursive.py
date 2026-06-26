"""Метод рекурсивного получения GUID всех дочерних типов поддерева."""

from ...core import APIManager


class ChildrenTypeGuidsRecursiveMixin(APIManager):
    """Реализует ``GET .../objectTypeTree/children/{parentTypeId}/recursive/guids``."""

    async def children_type_guids_recursive(
        self: "ChildrenTypeGuidsRecursiveMixin",
        parent_type_id: int,
    ) -> list[str]:
        """Возвращает GUID ВСЕХ потомков типа объекта рекурсивно (всё поддерево).

        Рекурсивный обход поддерева иерархии ТИПОВ: в отличие от
        :meth:`children_type_guids` (только прямые потомки, один уровень), метод
        спускается по всем уровням и собирает GUID всех потомков на любой глубине —
        дети, внуки и далее. GUID переносимы между инсталляциями IPS. Ответ сервера —
        плоский массив строк.

        Когда применять: когда нужны все подтипы целиком в виде переносимых GUID —
        для сверки охвата ветви между средами, экспорта/импорта конфигурации. Только
        прямые потомки — :meth:`children_type_guids`; то же поддерево в числовых id —
        :meth:`children_type_ids_recursive`; адресация по GUID родителя —
        :meth:`children_type_guids_recursive_by_guid`.

        Args:
            parent_type_id: Идентификатор типа-КОРНЯ поддерева (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID`` экземпляра).

        Returns:
            Список GUID всех потомков типа на всех уровнях (строки в id-пространстве
            ТИПОВ объектов). Пустой список — потомков нет (лист) либо тип не найден.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                all_subtype_guids = await ips.children_type_guids_recursive(1742)
                print(len(all_subtype_guids))

        Notes:
            operationId ``Metadata_GetObjectTypeChildrenGuidsRecursiveById``; путь
            ``GET /core/api/metadata/objectTypeTree/children/{parentTypeId}/recursive/``
            ``guids`` (ответ — массив строк). См. объектной модели IPS (иерархия типов).
            Связанные методы: :meth:`children_type_guids`,
            :meth:`children_type_ids_recursive`,
            :meth:`children_type_guids_recursive_by_guid`.
        """
        path = f"/core/api/metadata/objectTypeTree/children/{parent_type_id}/recursive/guids"
        data = await self._request("get", path)
        return [str(item) for item in data] if data is not None else []
