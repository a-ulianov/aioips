"""Метод получения id используемых атрибутов в порядке сортировки."""

from ...core import APIManager


class UsedSortedAttributeIdsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/usedSortedAttributes/ids``."""

    async def used_sorted_attribute_ids(
        self: "UsedSortedAttributeIdsMixin",
    ) -> list[int]:
        """Возвращает идентификаторы используемых атрибутов в порядке сортировки.

        Плоский перечень числовых ``id`` реально используемых типов атрибутов в заранее
        определённом порядке сортировки (его задаёт администратор для отображения).
        Облегчённый аналог :meth:`used_sorted_attributes` (полные схемы): когда нужен
        только упорядоченный набор идентификаторов. Ответ — массив целых чисел, без
        обёртки ``...NullableResultDto``.

        Когда применять: чтобы получить упорядоченный список id атрибутов для
        построения UI/гридов, не загружая полные метаописания. Неотсортированный набор
        тех же id — :meth:`used_unsorted_attribute_ids`.

        Returns:
            Список идентификаторов типов атрибутов (id-пространство ТИПОВ атрибутов) в
            порядке сортировки. Пустой список — используемых атрибутов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ids = await ips.used_sorted_attribute_ids()
                print(ids)

        Notes:
            operationId ``Metadata_GetUsedSortedAttributeIds``; путь
            ``GET /core/api/metadata/usedSortedAttributes/ids`` (ответ — массив ``int``).
            Связанные методы: :meth:`used_sorted_attributes`,
            :meth:`used_unsorted_attribute_ids`.
        """
        data = await self._request("get", "/core/api/metadata/usedSortedAttributes/ids")
        return [int(item) for item in data] if data is not None else []
