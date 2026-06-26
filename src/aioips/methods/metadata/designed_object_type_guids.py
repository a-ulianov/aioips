"""Метод получения списка GUID типов объектов с проектируемыми связями."""

from ...core import APIManager


class DesignedObjectTypeGuidsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/design/objectTypes/guids``."""

    async def designed_object_type_guids(
        self: "DesignedObjectTypeGuidsMixin",
    ) -> list[str]:
        """Возвращает GUID типов объектов, имеющих проектируемые типы связей.

        Плоский перечень стабильных GUID тех типов объектов метаданных, для которых задан
        хотя бы один проектируемый (designed) тип связи — то есть состав потомков такого
        типа можно проектировать. GUID переносимы между установками IPS (в отличие от
        ``id``). Ответ сервера — массив строк, без обёртки ``...NullableResultDto``.

        Когда применять: для сверки набора «проектируемых» типов между средами по стабильным
        GUID. Перечень числовых id — :meth:`designed_object_type_ids`; точечная проверка по
        GUID — :meth:`object_type_has_design_by_guid`.

        Returns:
            Список GUID типов объектов (строки в id-пространстве ТИПОВ объектов). Пустой
            список — таких типов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guids = await ips.designed_object_type_guids()
                print(len(guids))

        Notes:
            operationId ``Metadata_GetDesignedObjectGuids``; путь
            ``GET /core/api/metadata/design/objectTypes/guids`` (ответ — массив строк).
            Связанные методы: :meth:`designed_object_type_ids`,
            :meth:`object_type_has_design_by_guid`.
        """
        path = "/core/api/metadata/design/objectTypes/guids"
        data = await self._request("get", path)
        return [str(item) for item in data] if data is not None else []
