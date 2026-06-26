"""Метод получения GUID физических величин единиц измерения."""

from ...core import APIManager


class MeasureUnitQuantityGuidsMixin(APIManager):
    """Реализует метод ``GET /core/api/measureUnits/quantityGuids``.

    operationId ``MeasureUnits_GetQuantityGuids``.
    """

    async def measure_unit_quantity_guids(self: "MeasureUnitQuantityGuidsMixin") -> list[str]:
        """Возвращает список GUID физических величин, имеющих единицы измерения.

        Физическая величина (например, длина, масса) объединяет набор единиц измерения
        с коэффициентами приведения к базовой единице. Метод отдаёт идентификаторы только
        тех величин, для которых в справочнике заданы единицы измерения; полезно как лёгкий
        способ перечислить доступные величины без загрузки всего справочника единиц.

        Когда применять: для быстрого перечня доступных физических величин (например, чтобы
        предложить выбор величины пользователю). Сами единицы каждой величины и их ``k``
        получают через :meth:`measure_units` (сопоставление по ``physical_quantity_guid``).

        Returns:
            Список GUID физических величин в строковом представлении. Пустой список
            означает, что ни у одной величины нет заданных единиц измерения.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                quantity_guids = await ips.measure_unit_quantity_guids()
                print(len(quantity_guids))

        Notes:
            operationId ``MeasureUnits_GetQuantityGuids``; путь
            ``GET /core/api/measureUnits/quantityGuids``.
        """
        data = await self._request("get", "/core/api/measureUnits/quantityGuids")
        return [str(item) for item in data]
