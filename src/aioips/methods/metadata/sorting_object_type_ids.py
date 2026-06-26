"""Метод получения id типов объектов, поддерживающих сортировку."""

from ...core import APIManager


class SortingObjectTypeIdsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/sorting/objectTypes/ids``."""

    async def sorting_object_type_ids(
        self: "SortingObjectTypeIdsMixin",
    ) -> list[int]:
        """Возвращает id типов объектов, экземпляры которых можно сортировать.

        Сортировка в IPS — упорядочивание экземпляров по типам связей: данный метод
        перечисляет типы объектов, у которых есть сортирующие типы связей (можно задать
        порядок потомков). Ответ сервера — плоский массив целых, без обёртки
        ``...NullableResultDto``.

        Когда применять: для инвентаризации типов объектов с поддержкой сортировки, когда
        достаточно числовых ``id``. Перечень GUID — :meth:`sorting_object_type_guids`;
        проверка одного типа — :meth:`object_type_has_sorting`.

        Returns:
            Список ``id`` типов объектов (id-пространство ТИПОВ объектов) с поддержкой
            сортировки. Пустой список — таких типов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ids = await ips.sorting_object_type_ids()
                print(len(ids))

        Notes:
            operationId ``Metadata_GetSortingObjectIds``; путь
            ``GET /core/api/metadata/sorting/objectTypes/ids`` (ответ — массив ``int``).
            Связанные методы: :meth:`sorting_object_type_guids`,
            :meth:`object_type_has_sorting`.
        """
        path = "/core/api/metadata/sorting/objectTypes/ids"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
