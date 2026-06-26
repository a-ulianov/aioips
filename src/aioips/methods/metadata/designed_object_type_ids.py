"""Метод получения списка идентификаторов типов объектов с проектируемыми связями."""

from ...core import APIManager


class DesignedObjectTypeIdsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/design/objectTypes/ids``."""

    async def designed_object_type_ids(
        self: "DesignedObjectTypeIdsMixin",
    ) -> list[int]:
        """Возвращает идентификаторы типов объектов, имеющих проектируемые типы связей.

        Плоский перечень числовых ``id`` тех типов объектов метаданных, для которых задан
        хотя бы один проектируемый (designed) тип связи — то есть состав потомков такого
        типа можно проектировать (формировать связи конструкторского состава). Ответ
        сервера — массив целых чисел, без обёртки ``...NullableResultDto``.

        Когда применять: для инвентаризации типов, участвующих в проектировании состава,
        когда достаточно идентификаторов (затем точечно проверить конкретный тип через
        :meth:`object_type_has_design`). Перечень GUID — :meth:`designed_object_type_guids`.

        Returns:
            Список идентификаторов типов объектов (``id`` из id-пространства ТИПОВ
            объектов). Пустой список — таких типов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ids = await ips.designed_object_type_ids()
                print(len(ids))

        Notes:
            operationId ``Metadata_GetDesignedObjectIds``; путь
            ``GET /core/api/metadata/design/objectTypes/ids`` (ответ — массив ``int``).
            Связанные методы: :meth:`designed_object_type_guids`,
            :meth:`object_type_has_design`.
        """
        path = "/core/api/metadata/design/objectTypes/ids"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
