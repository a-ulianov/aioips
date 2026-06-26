"""Метод получения id типов объектов, выполняющих группировку."""

from ...core import APIManager


class GroupingObjectTypeIdsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/grouping/objectTypes/grouping/ids``."""

    async def grouping_object_type_ids(
        self: "GroupingObjectTypeIdsMixin",
    ) -> list[int]:
        """Возвращает id типов объектов, которые ВЫПОЛНЯЮТ группировку.

        «Grouping» тип объекта — тот, что группирует другие экземпляры по типам связей
        (выступает группирующим родителем), в отличие от «groupable» типа, который сам
        может быть сгруппирован (см. :meth:`groupable_object_type_ids`). Ответ сервера —
        плоский массив целых, без обёртки ``...NullableResultDto``.

        Когда применять: для инвентаризации типов-группировщиков, когда достаточно
        числовых ``id``. Перечень GUID — :meth:`grouping_object_type_guids`; проверка
        одного типа — :meth:`object_type_has_grouping`.

        Returns:
            Список ``id`` типов объектов (id-пространство ТИПОВ объектов), выполняющих
            группировку. Пустой список — таких типов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ids = await ips.grouping_object_type_ids()
                print(len(ids))

        Notes:
            operationId ``Metadata_GetSpecialGroupingIds``; путь
            ``GET /core/api/metadata/grouping/objectTypes/grouping/ids`` (ответ —
            массив ``int``). Связанные методы: :meth:`grouping_object_type_guids`,
            :meth:`object_type_has_grouping`, :meth:`groupable_object_type_ids`.
        """
        path = "/core/api/metadata/grouping/objectTypes/grouping/ids"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
