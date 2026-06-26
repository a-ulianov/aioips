"""Метод получения id цепочки родительских типов в обратном порядке (от корня)."""

from ...core import APIManager


class ParentTypeIdsReverseMixin(APIManager):
    """Реализует ``GET .../objectTypeTree/parents/{childTypeId}/ids/reverse``."""

    async def parent_type_ids_reverse(
        self: "ParentTypeIdsReverseMixin",
        child_type_id: int,
    ) -> list[int]:
        """Возвращает id цепочки родительских типов в ОБРАТНОМ порядке (от корня вниз).

        То же множество предков, что и :meth:`parent_type_ids`, но в обратном порядке:
        от КОРНЕВОГО типа иерархии к непосредственному родителю заданного типа. Удобно,
        когда путь по дереву ТИПОВ нужно читать сверху вниз (корень → ... → ближайший
        родитель). Ответ сервера — массив целых чисел.

        Когда применять: для построения пути «от корня» (хлебные крошки, отступы в
        дереве, иерархические заголовки), когда естественен порядок «общий → частный».
        Прямой порядок (от ближнего предка к корню) — :meth:`parent_type_ids`; корневой
        предок одним значением — :meth:`top_parent_type_id`.

        Args:
            child_type_id: Идентификатор ДОЧЕРНЕГО типа объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID`` экземпляра).

        Returns:
            Список идентификаторов типов-предков (``ObjectTypeID``) в порядке от корня к
            ближайшему родителю. Пустой список — предков нет (корневой) либо не найден.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                path_from_root = await ips.parent_type_ids_reverse(1742)
                print(path_from_root)

        Notes:
            operationId ``Metadata_GetObjectTypeParentIdsReverse``; путь
            ``GET /core/api/metadata/objectTypeTree/parents/{childTypeId}/ids/reverse``
            (ответ — массив ``int``). См. [[ips-object-model]] (иерархия типов).
            Связанные методы: :meth:`parent_type_ids`, :meth:`top_parent_type_id`.
        """
        path = f"/core/api/metadata/objectTypeTree/parents/{child_type_id}/ids/reverse"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
