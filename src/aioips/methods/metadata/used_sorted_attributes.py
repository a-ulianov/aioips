"""Метод получения используемых атрибутов в порядке сортировки."""

from ...core import APIManager
from ...schemas.metadata import AttributeType


class UsedSortedAttributesMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/usedSortedAttributes``."""

    async def used_sorted_attributes(
        self: "UsedSortedAttributesMixin",
    ) -> list[AttributeType]:
        """Возвращает используемые типы атрибутов в порядке сортировки.

        В отличие от :meth:`attribute_types` (все типы атрибутов метаданных), этот
        метод отдаёт только реально используемые атрибуты и в заранее определённом
        порядке сортировки (его задаёт администратор системы для удобного отображения,
        например в карточках/гридах). Ответ — голый массив ``ImsAttributeTypeDto`` без
        обёртки ``...NullableResultDto``.

        Когда применять: чтобы построить список атрибутов для UI/отчёта в правильном
        пользовательском порядке, исключив неиспользуемые. Если нужны только
        идентификаторы — дешевле :meth:`used_sorted_attribute_ids`; неотсортированный
        набор id — :meth:`used_unsorted_attribute_ids`.

        Returns:
            Список типов атрибутов по схеме :class:`AttributeType` в порядке сортировки.
            Пустой список — используемых атрибутов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                attrs = await ips.used_sorted_attributes()
                order = [a.name for a in attrs]

        Notes:
            operationId ``Metadata_GetUsedSortedAttributes``; путь
            ``GET /core/api/metadata/usedSortedAttributes`` (массив ``ImsAttributeTypeDto``).
            Связанные методы: :meth:`used_sorted_attribute_ids`,
            :meth:`used_unsorted_attribute_ids`, :meth:`attribute_types`.
        """
        data = await self._request("get", "/core/api/metadata/usedSortedAttributes")
        return [AttributeType.model_validate(item) for item in data]
