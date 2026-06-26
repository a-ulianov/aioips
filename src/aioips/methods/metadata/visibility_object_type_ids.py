"""Метод получения списка идентификаторов типов объектов с атрибутом видимости."""

from ...core import APIManager


class VisibilityObjectTypeIdsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/visibility/objectTypes/ids``."""

    async def visibility_object_type_ids(
        self: "VisibilityObjectTypeIdsMixin",
    ) -> list[int]:
        """Возвращает идентификаторы типов объектов, имеющих атрибут видимости.

        Плоский перечень числовых ``id`` тех типов объектов метаданных, у которых задан
        атрибут видимости (visibility) — то есть видимость их экземпляров управляется
        специальным атрибутом. Ответ сервера — массив целых чисел, без обёртки
        ``...NullableResultDto``.

        Когда применять: для инвентаризации типов, чья видимость регулируется атрибутом,
        когда достаточно идентификаторов (затем точечно проверить тип через
        :meth:`object_type_has_visibility_attribute`). Перечень GUID —
        :meth:`visibility_object_type_guids`.

        Returns:
            Список идентификаторов типов объектов (``id`` из id-пространства ТИПОВ
            объектов). Пустой список — таких типов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ids = await ips.visibility_object_type_ids()
                print(len(ids))

        Notes:
            operationId ``Metadata_GetVisibilityObjectIds``; путь
            ``GET /core/api/metadata/visibility/objectTypes/ids`` (ответ — массив ``int``).
            Связанные методы: :meth:`visibility_object_type_guids`,
            :meth:`object_type_has_visibility_attribute`.
        """
        path = "/core/api/metadata/visibility/objectTypes/ids"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
