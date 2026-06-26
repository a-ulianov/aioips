"""Метод получения GUID типов объектов, поддающихся группировке."""

from ...core import APIManager


class GroupableObjectTypeGuidsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/grouping/objectTypes/groupable/guids``."""

    async def groupable_object_type_guids(
        self: "GroupableObjectTypeGuidsMixin",
    ) -> list[str]:
        """Возвращает GUID типов объектов, экземпляры которых можно группировать.

        «Groupable» тип объекта — тот, что может быть СГРУППИРОВАН (выступать
        сгруппированным потомком по типам связей), в отличие от «grouping» типа,
        выполняющего группировку (см. :meth:`grouping_object_type_guids`). GUID стабильны
        между установками IPS (в отличие от ``id``), поэтому подходят для сверки конфигурации
        между средами. Ответ сервера — массив строк, без обёртки ``...NullableResultDto``.

        Когда применять: для переносимой инвентаризации/сравнения наборов группируемых
        типов объектов между средами. Перечень числовых id — :meth:`groupable_object_type_ids`;
        проверка одного типа — :meth:`object_type_is_groupable_by_guid`.

        Returns:
            Список GUID типов объектов (строки в id-пространстве ТИПОВ объектов), которые
            могут быть сгруппированы. Пустой список — таких типов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guids = await ips.groupable_object_type_guids()
                print(len(guids))

        Notes:
            operationId ``Metadata_GetSpecialGroupedGuids``; путь
            ``GET /core/api/metadata/grouping/objectTypes/groupable/guids`` (ответ —
            массив строк). Связанные методы: :meth:`groupable_object_type_ids`,
            :meth:`object_type_is_groupable_by_guid`, :meth:`grouping_object_type_guids`.
        """
        path = "/core/api/metadata/grouping/objectTypes/groupable/guids"
        data = await self._request("get", path)
        return [str(item) for item in data] if data is not None else []
