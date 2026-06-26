"""Метод получения GUID типов объектов, выполняющих группировку."""

from ...core import APIManager


class GroupingObjectTypeGuidsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/grouping/objectTypes/grouping/guids``."""

    async def grouping_object_type_guids(
        self: "GroupingObjectTypeGuidsMixin",
    ) -> list[str]:
        """Возвращает GUID типов объектов, которые ВЫПОЛНЯЮТ группировку.

        «Grouping» тип объекта — тот, что группирует другие экземпляры по типам связей
        (выступает группирующим родителем), в отличие от «groupable» типа, который сам
        может быть сгруппирован (см. :meth:`groupable_object_type_guids`). GUID стабильны
        между установками IPS (в отличие от ``id``), поэтому подходят для сверки
        конфигурации между средами. Ответ сервера — массив строк, без обёртки
        ``...NullableResultDto``.

        Когда применять: для переносимой инвентаризации/сравнения типов-группировщиков
        между средами. Перечень числовых id — :meth:`grouping_object_type_ids`; проверка
        одного типа — :meth:`object_type_has_grouping_by_guid`.

        Returns:
            Список GUID типов объектов (строки в id-пространстве ТИПОВ объектов),
            выполняющих группировку. Пустой список — таких типов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guids = await ips.grouping_object_type_guids()
                print(len(guids))

        Notes:
            operationId ``Metadata_GetSpecialGroupingGuids``; путь
            ``GET /core/api/metadata/grouping/objectTypes/grouping/guids`` (ответ —
            массив строк). Связанные методы: :meth:`grouping_object_type_ids`,
            :meth:`object_type_has_grouping_by_guid`, :meth:`groupable_object_type_guids`.
        """
        path = "/core/api/metadata/grouping/objectTypes/grouping/guids"
        data = await self._request("get", path)
        return [str(item) for item in data] if data is not None else []
