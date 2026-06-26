"""Метод получения id используемых атрибутов без сортировки."""

from ...core import APIManager


class UsedUnsortedAttributeIdsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/usedUnsortedAttributes/ids``."""

    async def used_unsorted_attribute_ids(
        self: "UsedUnsortedAttributeIdsMixin",
    ) -> list[int]:
        """Возвращает идентификаторы используемых атрибутов без порядка сортировки.

        Плоский перечень числовых ``id`` реально используемых типов атрибутов БЕЗ
        применения пользовательского порядка сортировки (порядок не гарантируется).
        Парный к :meth:`used_sorted_attribute_ids`: тот же набор используемых
        атрибутов, но без упорядочивания — дешевле, когда порядок не важен (например,
        для проверки принадлежности через ``set``). Ответ — массив целых чисел, без
        обёртки ``...NullableResultDto``.

        Когда применять: чтобы быстро получить набор id используемых атрибутов, когда
        порядок не нужен. Если нужен порядок сортировки — :meth:`used_sorted_attribute_ids`;
        полные схемы — :meth:`used_sorted_attributes`.

        Returns:
            Список идентификаторов типов атрибутов (id-пространство ТИПОВ атрибутов) без
            гарантии порядка. Пустой список — используемых атрибутов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ids = set(await ips.used_unsorted_attribute_ids())
                print(1029 in ids)

        Notes:
            operationId ``Metadata_GetUsedUnsortedAttributeIds``; путь
            ``GET /core/api/metadata/usedUnsortedAttributes/ids`` (ответ — массив ``int``).
            Связанные методы: :meth:`used_sorted_attribute_ids`,
            :meth:`used_sorted_attributes`.
        """
        data = await self._request("get", "/core/api/metadata/usedUnsortedAttributes/ids")
        return [int(item) for item in data] if data is not None else []
