"""Метод получения GUID всех корневых типов объектов иерархии."""

from ...core import APIManager


class TopObjectTypeGuidsMixin(APIManager):
    """Реализует ``GET .../objectTypeTree/topObjectTypes/guids``."""

    async def top_object_type_guids(
        self: "TopObjectTypeGuidsMixin",
    ) -> list[str]:
        """Возвращает GUID всех КОРНЕВЫХ типов объектов (верхний уровень дерева).

        Перечень корней дерева ТИПОВ в виде стабильных GUID: типы без родителя —
        отправные точки для обхода иерархии сверху вниз. GUID переносимы между
        инсталляциями IPS (в отличие от числового ``id``). Ответ сервера — массив строк.

        Когда применять: для сверки набора верхнеуровневых типов между средами по
        переносимым GUID, старта обхода дерева по стабильным идентификаторам. Те же
        корни в виде числовых id — :meth:`top_object_type_ids`; спуск к потомкам по GUID —
        :meth:`children_type_guids_by_guid`.

        Returns:
            Список GUID корневых типов (строки в id-пространстве ТИПОВ объектов). Пустой
            список — корневых типов нет (пустая метамодель).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                root_guids = await ips.top_object_type_guids()
                print(root_guids)

        Notes:
            operationId ``Metadata_GetTopObjectTypeGuids``; путь
            ``GET /core/api/metadata/objectTypeTree/topObjectTypes/guids``
            (ответ — массив строк). См. [[ips-object-model]] (иерархия типов).
            Связанные методы: :meth:`top_object_type_ids`,
            :meth:`children_type_guids_by_guid`.
        """
        path = "/core/api/metadata/objectTypeTree/topObjectTypes/guids"
        data = await self._request("get", path)
        return [str(item) for item in data] if data is not None else []
