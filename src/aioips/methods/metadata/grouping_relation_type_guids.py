"""Метод получения GUID типов связей, участвующих в группировке."""

from ...core import APIManager


class GroupingRelationTypeGuidsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/grouping/relationTypes/guids``."""

    async def grouping_relation_type_guids(
        self: "GroupingRelationTypeGuidsMixin",
    ) -> list[str]:
        """Возвращает GUID типов связей, по которым выполняется группировка.

        Группировка экземпляров происходит по типам связей: данный метод перечисляет
        ТИПЫ СВЯЗЕЙ, помеченные как группирующие, по их стабильным GUID. GUID переносимы
        между установками IPS (в отличие от ``id``), поэтому подходят для сверки
        конфигурации между средами. Ответ сервера — массив строк, без обёртки
        ``...NullableResultDto``.

        Когда применять: для переносимой инвентаризации группирующих типов связей.
        Перечень числовых id — :meth:`grouping_relation_type_ids`; проверка одного типа
        связи — :meth:`relation_type_has_grouping_by_guid`.

        Returns:
            Список GUID типов связей (строки в id-пространстве ТИПОВ связей), участвующих
            в группировке. Пустой список — таких типов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guids = await ips.grouping_relation_type_guids()
                print(len(guids))

        Notes:
            operationId ``Metadata_GetSpecialGroupingRelationGuids``; путь
            ``GET /core/api/metadata/grouping/relationTypes/guids`` (ответ — массив строк).
            Связанные методы: :meth:`grouping_relation_type_ids`,
            :meth:`relation_type_has_grouping_by_guid`.
        """
        path = "/core/api/metadata/grouping/relationTypes/guids"
        data = await self._request("get", path)
        return [str(item) for item in data] if data is not None else []
