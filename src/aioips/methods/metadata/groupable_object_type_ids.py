"""Метод получения id типов объектов, поддающихся группировке."""

from ...core import APIManager


class GroupableObjectTypeIdsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/grouping/objectTypes/groupable/ids``."""

    async def groupable_object_type_ids(
        self: "GroupableObjectTypeIdsMixin",
    ) -> list[int]:
        """Возвращает id типов объектов, экземпляры которых можно группировать.

        Группировка в IPS — это объединение экземпляров по типам связей: «groupable»
        тип объекта — тот, что может быть СГРУППИРОВАН (выступать сгруппированным
        потомком), в отличие от «grouping» типа, который выполняет группировку
        (см. :meth:`grouping_object_type_ids`). Ответ сервера — плоский массив целых,
        без обёртки ``...NullableResultDto``.

        Когда применять: для инвентаризации типов объектов, допускающих группировку,
        когда достаточно числовых ``id``. Перечень GUID — :meth:`groupable_object_type_guids`;
        проверка одного типа — :meth:`object_type_is_groupable`.

        Returns:
            Список ``id`` типов объектов (id-пространство ТИПОВ объектов), которые могут
            быть сгруппированы. Пустой список — таких типов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ids = await ips.groupable_object_type_ids()
                print(len(ids))

        Notes:
            operationId ``Metadata_GetSpecialGroupedIds``; путь
            ``GET /core/api/metadata/grouping/objectTypes/groupable/ids`` (ответ —
            массив ``int``). Связанные методы: :meth:`groupable_object_type_guids`,
            :meth:`object_type_is_groupable`, :meth:`grouping_object_type_ids`.
        """
        path = "/core/api/metadata/grouping/objectTypes/groupable/ids"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
