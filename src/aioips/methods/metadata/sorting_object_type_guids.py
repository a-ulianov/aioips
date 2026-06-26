"""Метод получения GUID типов объектов, поддерживающих сортировку."""

from ...core import APIManager


class SortingObjectTypeGuidsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/sorting/objectTypes/guids``."""

    async def sorting_object_type_guids(
        self: "SortingObjectTypeGuidsMixin",
    ) -> list[str]:
        """Возвращает GUID типов объектов, экземпляры которых можно сортировать.

        Сортировка в IPS — упорядочивание экземпляров по типам связей: данный метод
        перечисляет типы объектов с сортирующими типами связей по их стабильным GUID.
        GUID переносимы между установками IPS (в отличие от ``id``), поэтому подходят для
        сверки конфигурации между средами. Ответ сервера — массив строк, без обёртки
        ``...NullableResultDto``.

        Когда применять: для переносимой инвентаризации типов объектов с поддержкой
        сортировки. Перечень числовых id — :meth:`sorting_object_type_ids`; проверка
        одного типа — :meth:`object_type_has_sorting_by_guid`.

        Returns:
            Список GUID типов объектов (строки в id-пространстве ТИПОВ объектов) с
            поддержкой сортировки. Пустой список — таких типов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guids = await ips.sorting_object_type_guids()
                print(len(guids))

        Notes:
            operationId ``Metadata_GetSortingObjectGuids``; путь
            ``GET /core/api/metadata/sorting/objectTypes/guids`` (ответ — массив строк).
            Связанные методы: :meth:`sorting_object_type_ids`,
            :meth:`object_type_has_sorting_by_guid`.
        """
        path = "/core/api/metadata/sorting/objectTypes/guids"
        data = await self._request("get", path)
        return [str(item) for item in data] if data is not None else []
