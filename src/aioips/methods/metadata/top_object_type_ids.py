"""Метод получения id всех корневых типов объектов иерархии."""

from ...core import APIManager


class TopObjectTypeIdsMixin(APIManager):
    """Реализует ``GET .../objectTypeTree/topObjectTypes/ids``."""

    async def top_object_type_ids(
        self: "TopObjectTypeIdsMixin",
    ) -> list[int]:
        """Возвращает id всех КОРНЕВЫХ типов объектов (верхний уровень дерева).

        Перечень корней дерева ТИПОВ: типы, у которых нет родителя — отправные точки
        для обхода всей иерархии сверху вниз. От каждого можно спускаться через
        :meth:`children_type_ids`. Ответ сервера — массив целых чисел.

        Когда применять: как стартовый набор для полного обхода дерева типов, построения
        корневых веток в UI, инвентаризации верхнеуровневых категорий. Те же корни в
        виде GUID — :meth:`top_object_type_guids`; корень ветви конкретного типа —
        :meth:`top_parent_type_id`.

        Returns:
            Список идентификаторов корневых типов (``ObjectTypeID`` — id-пространство
            ТИПОВ объектов). Пустой список — корневых типов нет (пустая метамодель).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                roots = await ips.top_object_type_ids()
                print(roots)

        Notes:
            operationId ``Metadata_GetTopObjectTypeIds``; путь
            ``GET /core/api/metadata/objectTypeTree/topObjectTypes/ids``
            (ответ — массив ``int``). См. [[ips-object-model]] (иерархия типов).
            Связанные методы: :meth:`top_object_type_guids`, :meth:`children_type_ids`,
            :meth:`top_parent_type_id`.
        """
        path = "/core/api/metadata/objectTypeTree/topObjectTypes/ids"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
