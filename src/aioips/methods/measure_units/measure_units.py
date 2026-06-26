"""Метод получения списка единиц измерения."""

from ...core import APIManager
from ...schemas.measure_units import MeasureUnit


class MeasureUnitsMixin(APIManager):
    """Реализует метод ``GET /core/api/measureUnits`` (``MeasureUnits_GetMeasureUnitList``)."""

    async def measure_units(self: "MeasureUnitsMixin") -> list[MeasureUnit]:
        """Возвращает полный справочник единиц измерения, определённых в IPS.

        Единицы измерения применяются атрибутами типа ``ftMeasured``, где значение
        складывается из числовой величины и единицы измерения. Каждая единица привязана
        к одной физической величине и хранит коэффициент приведения ``k`` к её базовой
        единице (для базовой ``k = 1``).

        Когда применять: чтобы интерпретировать/сформировать значение атрибута ``ftMeasured``
        (понять обозначение единицы, выполнить перевод между единицами одной величины через
        их ``k``) или построить справочник единиц по величинам. Перечень самих величин (без
        единиц) — :meth:`measure_unit_quantity_guids`. Предусловий нет.

        Returns:
            Список единиц измерения по схеме :class:`MeasureUnit`. Пустой список означает,
            что в базе не определено ни одной единицы измерения.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                units = await ips.measure_units()
                by_quantity: dict[int, list[str]] = {}
                for unit in units:
                    by_quantity.setdefault(unit.physical_quantity_id, []).append(unit.short_name)

        Notes:
            operationId ``MeasureUnits_GetMeasureUnitList``; путь
            ``GET /core/api/measureUnits`` (массив ``MeasureUnitDto``).
        """
        data = await self._request("get", "/core/api/measureUnits")
        return [MeasureUnit.model_validate(item) for item in data]
