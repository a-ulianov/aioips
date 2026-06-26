"""Метод получения дерева (иерархии) типов объектов."""

from typing import Any

from ...core import APIManager


class ObjectTypesTreeMixin(APIManager):
    """Реализует метод ``POST /core/api/objectTypes/GetObjectTypesTree``."""

    async def object_types_tree(
        self: "ObjectTypesTreeMixin",
        object_type_ids: list[int],
    ) -> dict[str, Any]:
        """Возвращает дерево (иерархию родитель→потомок) типов объектов.

        Отдаёт структуру связей типов в виде дерева: применяется для построения
        навигатора/классификатора типов в UI. Список ``object_type_ids`` ограничивает
        выборку конкретными типами; пустой список означает «все типы» (по swagger).

        POST-verb, но операция ЧТЕНИЯ (идемпотентна, ничего не мутирует): тело несёт
        лишь список идентификаторов для фильтрации.

        Args:
            object_type_ids: Список идентификаторов ТИПОВ объектов (``ObjectTypeID`` —
                id-пространство ТИПОВ, не ``ObjectID``/``ID`` объекта или версии).
                Пустой список ``[]`` — вернуть дерево по всем типам. Передаётся как
                «голый» JSON-массив ``list[int]`` в теле запроса.

        Returns:
            Словарь, описывающий дерево типов (ответ swagger — ``object``).
            Возвращается «как есть» без фиксированной типизации структуры. Пустой
            словарь, если ответ не является объектом.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                tree = await ips.object_types_tree([])  # все типы

        Notes:
            operationId ``ObjectTypes_GetObjectTypesTree``; путь
            ``POST /core/api/objectTypes/GetObjectTypesTree``. Тело — голый
            ``list[int]``; ответ — словарь-дерево (не result-обёртка).
            Связанные методы: :meth:`object_type_icons`.
        """
        data = await self._request(
            "post", "/core/api/objectTypes/GetObjectTypesTree", json=object_type_ids
        )
        return data if isinstance(data, dict) else {}
