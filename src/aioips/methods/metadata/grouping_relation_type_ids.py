"""Метод получения id типов связей, участвующих в группировке."""

from ...core import APIManager


class GroupingRelationTypeIdsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/grouping/relationTypes/ids``."""

    async def grouping_relation_type_ids(
        self: "GroupingRelationTypeIdsMixin",
    ) -> list[int]:
        """Возвращает id типов связей, по которым выполняется группировка.

        Группировка экземпляров происходит по типам связей: данный метод перечисляет
        ТИПЫ СВЯЗЕЙ, помеченные как группирующие. Дополняет перечни типов объектов
        (:meth:`grouping_object_type_ids` / :meth:`groupable_object_type_ids`), но в
        пространстве типов СВЯЗЕЙ. Ответ сервера — плоский массив целых, без обёртки
        ``...NullableResultDto``.

        Когда применять: для инвентаризации группирующих типов связей, когда достаточно
        числовых ``id``. Перечень GUID — :meth:`grouping_relation_type_guids`; проверка
        одного типа связи — :meth:`relation_type_has_grouping`.

        Returns:
            Список ``id`` типов связей (id-пространство ТИПОВ связей), участвующих в
            группировке. Пустой список — таких типов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ids = await ips.grouping_relation_type_ids()
                print(len(ids))

        Notes:
            operationId ``Metadata_GetSpecialGroupingRelationIds``; путь
            ``GET /core/api/metadata/grouping/relationTypes/ids`` (ответ — массив ``int``).
            Связанные методы: :meth:`grouping_relation_type_guids`,
            :meth:`relation_type_has_grouping`.
        """
        path = "/core/api/metadata/grouping/relationTypes/ids"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
