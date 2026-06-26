"""Метод получения id типов связей, участвующих в сортировке."""

from ...core import APIManager


class SortingRelationTypeIdsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/sorting/relationTypes/ids``."""

    async def sorting_relation_type_ids(
        self: "SortingRelationTypeIdsMixin",
    ) -> list[int]:
        """Возвращает id типов связей, по которым выполняется сортировка.

        Сортировка экземпляров происходит по типам связей: данный метод перечисляет
        ТИПЫ СВЯЗЕЙ, помеченные как сортирующие (задающие порядок). Дополняет перечень
        типов объектов (:meth:`sorting_object_type_ids`), но в пространстве типов СВЯЗЕЙ.
        Ответ сервера — плоский массив целых, без обёртки ``...NullableResultDto``.

        Когда применять: для инвентаризации сортирующих типов связей, когда достаточно
        числовых ``id``. Перечень GUID — :meth:`sorting_relation_type_guids`; проверка
        одного типа связи — :meth:`relation_type_has_sorting`.

        Returns:
            Список ``id`` типов связей (id-пространство ТИПОВ связей), участвующих в
            сортировке. Пустой список — таких типов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ids = await ips.sorting_relation_type_ids()
                print(len(ids))

        Notes:
            operationId ``Metadata_GetSpecialSortingRelationIds``; путь
            ``GET /core/api/metadata/sorting/relationTypes/ids`` (ответ — массив ``int``).
            Связанные методы: :meth:`sorting_relation_type_guids`,
            :meth:`relation_type_has_sorting`.
        """
        path = "/core/api/metadata/sorting/relationTypes/ids"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
