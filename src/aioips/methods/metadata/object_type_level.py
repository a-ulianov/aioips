"""Метод получения уровня типа объекта в иерархии типов."""

from ...core import APIManager


class ObjectTypeLevelMixin(APIManager):
    """Реализует ``GET .../objectTypeTree/objectTypeLevel/{id}``."""

    async def object_type_level(
        self: "ObjectTypeLevelMixin",
        id: int,
    ) -> int:
        """Возвращает уровень (глубину) типа объекта в дереве типов.

        Глубина типа в иерархии ТИПОВ: насколько он удалён от корня. Корневые типы
        находятся на верхнем уровне, каждый шаг вниз по дереву увеличивает уровень.
        Численно совпадает с длиной цепочки :meth:`parent_type_ids`. Ответ сервера —
        целое число.

        Когда применять: для отрисовки отступов/вложенности в дереве типов, сортировки
        типов по глубине, оценки расположения типа в иерархии. Сама цепочка предков —
        :meth:`parent_type_ids`; корневые типы верхнего уровня — :meth:`top_object_type_ids`.

        Args:
            id: Идентификатор типа объекта (``ObjectTypeID`` — id-пространство ТИПОВ
                объектов, не ``ObjectID``/``ID`` экземпляра).

        Returns:
            Уровень типа в иерархии (целое; корневой уровень — наименьший). ``0`` —
            если сервер вернул ``null`` (тип не найден либо корневой, в зависимости от
            принятой нумерации уровней).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                level = await ips.object_type_level(1742)
                print(level)

        Notes:
            operationId ``Metadata_GetObjectTypeLevel``; путь
            ``GET /core/api/metadata/objectTypeTree/objectTypeLevel/{id}``
            (ответ — ``int``). См. объектной модели IPS (иерархия типов).
            Связанные методы: :meth:`parent_type_ids`, :meth:`top_object_type_ids`.
        """
        path = f"/core/api/metadata/objectTypeTree/objectTypeLevel/{id}"
        data = await self._request("get", path)
        return int(data) if data is not None else 0
