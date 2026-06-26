"""Метод получения списка GUID типов объектов с атрибутом видимости."""

from ...core import APIManager


class VisibilityObjectTypeGuidsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/visibility/objectTypes/guids``."""

    async def visibility_object_type_guids(
        self: "VisibilityObjectTypeGuidsMixin",
    ) -> list[str]:
        """Возвращает GUID типов объектов, имеющих атрибут видимости.

        Плоский перечень стабильных GUID тех типов объектов метаданных, у которых задан
        атрибут видимости (visibility) — то есть видимость их экземпляров управляется
        специальным атрибутом. GUID переносимы между установками IPS (в отличие от
        ``id``). Ответ сервера — массив строк, без обёртки ``...NullableResultDto``.

        Когда применять: для сверки набора типов с атрибутом видимости между средами по
        стабильным GUID. Перечень числовых id — :meth:`visibility_object_type_ids`;
        точечная проверка по GUID — :meth:`object_type_has_visibility_attribute_by_guid`.

        Returns:
            Список GUID типов объектов (строки в id-пространстве ТИПОВ объектов). Пустой
            список — таких типов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guids = await ips.visibility_object_type_guids()
                print(len(guids))

        Notes:
            operationId ``Metadata_GetVisibilityObjectGuids``; путь
            ``GET /core/api/metadata/visibility/objectTypes/guids`` (ответ — массив строк).
            Связанные методы: :meth:`visibility_object_type_ids`,
            :meth:`object_type_has_visibility_attribute_by_guid`.
        """
        path = "/core/api/metadata/visibility/objectTypes/guids"
        data = await self._request("get", path)
        return [str(item) for item in data] if data is not None else []
