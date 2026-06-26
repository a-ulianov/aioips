"""Методы раздела единиц измерения IPS Web API."""

from .measure_unit_quantity_guids import MeasureUnitQuantityGuidsMixin
from .measure_units import MeasureUnitsMixin


class MeasureUnitsAPI(MeasureUnitsMixin, MeasureUnitQuantityGuidsMixin):
    """Объединяет методы раздела единиц измерения.

    References:
        Эндпоинты ``/core/api/measureUnits/*`` IPS Server Web API.
    """


__all__ = ["MeasureUnitsAPI"]
