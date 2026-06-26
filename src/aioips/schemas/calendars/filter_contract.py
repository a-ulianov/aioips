"""Схема фильтра календарей IPS (особые дни).

References:
    ``GET /core/api/calendars/baseFilter`` — ``FilterContract``.
    ``GET /core/api/calendars/userFilter`` — ``FilterContract``.
"""

from typing import Annotated, Any

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class CalendarFilter(IPSModel):
    """Фильтр выборки особых дней календаря (``FilterContract``).

    Описывает критерии отбора особых дней (отпуска, командировки, переносы и т.п.)
    при загрузке базового (:meth:`base_calendar_filter`) или пользовательского
    (:meth:`user_calendar_filter`) фильтра календаря. Каждое поле-критерий парно
    флагу ``use_*``: критерий учитывается, только если соответствующий флаг ``True``.

    Когда применять: чтобы узнать текущие настройки фильтрации особых дней перед
    их применением/изменением, а также для интерпретации того, по каким признакам
    сервер отбирает особые дни календаря (см. :class:`Calendar` — поле
    ``special_calendar_days``).

    Моделирование вложенности: коллекции перечислимых значений типизированы как
    ``list[Any]`` (``type_special_day_periods`` — значения ``SpecialDaysPeriodType``;
    ``special_day_types`` — значения ``DayType``). Это сделано осознанно: их
    перечисления относятся к общему домену и должны выноситься отдельно; здесь
    значения сохраняются «как есть» (строки) без потери данных.

    Все поля необязательны с дефолтами — устойчиво к различиям версий API; в самом
    контракте обязательны только булевы флаги ``use_*``.

    Attributes:
        start_date_time: Нижняя граница диапазона дат (ISO-8601, UTC); учитывается,
            если ``use_start_date_time``.
        finish_date_time: Верхняя граница диапазона дат (ISO-8601, UTC); учитывается,
            если ``use_finish_date_time``.
        type_special_day_periods: Список типов периодов особых дней
            (``SpecialDaysPeriodType``: ``vacation``, ``businessTrip`` …); учитывается,
            если ``use_type_special_day_periods``.
        special_day_types: Список типов дней (``DayType``: ``standardWork``,
            ``holiday``, ``nonStandardWork``); учитывается, если
            ``use_special_day_types``.
        reason: Текст причины (подстрока) для отбора; учитывается, если ``use_reason``.
        use_start_date_time: Учитывать ли ``start_date_time``.
        use_finish_date_time: Учитывать ли ``finish_date_time``.
        use_type_special_day_periods: Учитывать ли ``type_special_day_periods``.
        use_special_day_types: Учитывать ли ``special_day_types``.
        use_reason: Учитывать ли ``reason``.

    Notes:
        Значения перечислений приходят строками. ``SpecialDaysPeriodType`` ∈
        {``none``, ``businessTrip``, ``workOut``, ``sideJob``, ``combination``,
        ``byNecessity``, ``vacation``, ``sick``, ``compensatoryHoliday``,
        ``lateness``, ``absenteeism``, ``other``}; ``DayType`` ∈ {``standardWork``,
        ``holiday``, ``nonStandardWork``}.
    """

    start_date_time: str | None = Field(default=None, description="Нижняя граница дат (UTC)")
    finish_date_time: str | None = Field(default=None, description="Верхняя граница дат (UTC)")
    type_special_day_periods: Annotated[list[Any], EmptyListIfNone] = Field(
        default_factory=list, description="Типы периодов особых дней"
    )
    special_day_types: Annotated[list[Any], EmptyListIfNone] = Field(
        default_factory=list, description="Типы дней"
    )
    reason: str | None = Field(default=None, description="Причина (подстрока)")
    use_start_date_time: bool = Field(default=False, description="Учитывать нижнюю границу дат")
    use_finish_date_time: bool = Field(default=False, description="Учитывать верхнюю границу дат")
    use_type_special_day_periods: bool = Field(
        default=False, description="Учитывать типы периодов особых дней"
    )
    use_special_day_types: bool = Field(default=False, description="Учитывать типы дней")
    use_reason: bool = Field(default=False, description="Учитывать причину")
