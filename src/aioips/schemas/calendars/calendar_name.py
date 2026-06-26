"""Схема краткого описания календаря IPS.

References:
    ``GET /core/api/calendars`` — массив ``CalendarName``.
"""

from pydantic import Field

from ..base import IPSModel


class CalendarName(IPSModel):
    """Краткая запись календаря в общем списке календарей IPS.

    Облегчённый элемент справочника календарей: содержит только идентификатор и
    отображаемое имя. Используется для построения списков выбора календаря; полные
    параметры конкретного календаря загружаются отдельно по ``calendar_id`` методом
    :meth:`calendar_settings`.

    Оба поля обязательны (приходят с сервера всегда).

    Attributes:
        calendar_id: Числовой идентификатор календаря (``calendarId``).
        name: Отображаемое имя календаря.
    """

    calendar_id: int = Field(description="Идентификатор календаря")
    name: str = Field(description="Отображаемое имя календаря")
