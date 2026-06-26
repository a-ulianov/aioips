"""Метод получения GUID типов связей, участвующих в сортировке."""

from ...core import APIManager


class SortingRelationTypeGuidsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/sorting/relationTypes/guids``."""

    async def sorting_relation_type_guids(
        self: "SortingRelationTypeGuidsMixin",
    ) -> list[str]:
        """Возвращает GUID типов связей, по которым выполняется сортировка.

        Сортировка экземпляров происходит по типам связей: данный метод перечисляет
        ТИПЫ СВЯЗЕЙ, помеченные как сортирующие (задающие порядок), по их стабильным GUID.
        GUID переносимы между установками IPS (в отличие от ``id``), поэтому подходят для
        сверки конфигурации между средами. Ответ сервера — массив строк, без обёртки
        ``...NullableResultDto``.

        Когда применять: для переносимой инвентаризации сортирующих типов связей.
        Перечень числовых id — :meth:`sorting_relation_type_ids`; проверка одного типа
        связи — :meth:`relation_type_has_sorting_by_guid`.

        Returns:
            Список GUID типов связей (строки в id-пространстве ТИПОВ связей), участвующих
            в сортировке. Пустой список — таких типов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guids = await ips.sorting_relation_type_guids()
                print(len(guids))

        Notes:
            operationId ``Metadata_GetSpecialSortingRelationGuids``; путь
            ``GET /core/api/metadata/sorting/relationTypes/guids`` (ответ — массив строк).
            Связанные методы: :meth:`sorting_relation_type_ids`,
            :meth:`relation_type_has_sorting_by_guid`.
        """
        path = "/core/api/metadata/sorting/relationTypes/guids"
        data = await self._request("get", path)
        return [str(item) for item in data] if data is not None else []
