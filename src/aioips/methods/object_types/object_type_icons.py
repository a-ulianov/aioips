"""Метод пакетного получения иконок типов объектов по списку id типов."""

from typing import Any

from ...core import APIManager


class ObjectTypeIconsMixin(APIManager):
    """Реализует метод ``POST /core/api/objectTypes/GetObjectTypeIcons``."""

    async def object_type_icons(
        self: "ObjectTypeIconsMixin",
        object_type_ids: list[int],
    ) -> dict[str, Any]:
        """Возвращает иконки типов объектов по списку id типов (для UI).

        Отдаёт карту «id типа → иконка» для одновременного получения значков
        нескольких типов: типичный сценарий — отрисовка дерева/списка типов в
        интерфейсе, где каждому типу нужна своя иконка. Иконки приходят как
        base64-строки (в swagger — ``string``/``byte``).

        POST-verb, но операция ЧТЕНИЯ (идемпотентна, ничего не мутирует): тело
        запроса используется лишь для передачи списка идентификаторов, который
        неудобно слать в URL.

        Args:
            object_type_ids: Список идентификаторов ТИПОВ объектов (``ObjectTypeID`` —
                id-пространство ТИПОВ, не ``ObjectID``/``ID`` объекта или версии).
                Передаётся как «голый» JSON-массив ``list[int]`` в теле запроса.

        Returns:
            Словарь-карта ``{id_типа (str): иконка (str, base64)}``. Возвращается «как
            есть» (ответ swagger — ``object`` с ``additionalProperties``). Пустой
            словарь, если ответ не является объектом.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                icons = await ips.object_type_icons([1742, 1743])
                icon_b64 = icons.get("1742")

        Notes:
            operationId ``ObjectTypes_GetObjectTypeIcons``; путь
            ``POST /core/api/objectTypes/GetObjectTypeIcons``. Тело — голый
            ``list[int]``; ответ — словарь-карта (не result-обёртка).
            Связанные методы: :meth:`object_types_tree`.
        """
        data = await self._request(
            "post", "/core/api/objectTypes/GetObjectTypeIcons", json=object_type_ids
        )
        return data if isinstance(data, dict) else {}
