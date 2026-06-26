"""Схема параметров (настроек) календаря IPS.

References:
    ``GET /core/api/calendars/calendarSettings/{calendarId}`` — ``CalendarContract``.
    ``GET /core/api/calendars/unitCalendarForUser/{userId}`` — ``CalendarContract``.
    ``GET /core/api/calendars/userCalendarSettings/{userId}`` — ``CalendarContract``.
"""

from typing import Annotated, Any

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class Calendar(IPSModel):
    """Полные настройки рабочего календаря IPS (``CalendarContract``).

    Описывает параметры производственного календаря: владельца, начало недели/года,
    длительности рабочего дня/недели, стандартную рабочую неделю, набор рабочих
    периодов и особые дни (праздники, переносы). Используется для интерпретации
    рабочего времени при планировании.

    Когда применять: после выбора календаря из списка :meth:`calendars` —
    для загрузки его настроек через :meth:`calendar_settings`; либо для получения
    эффективного календаря пользователя (:meth:`user_calendar_settings`) или его
    подразделения (:meth:`unit_calendar_for_user`).

    Моделирование вложенности: глубоко вложенные коллекции (``standard_week``,
    ``standard_work_periods``, ``special_calendar_days``) и дополнительный календарь
    (``additional_calendar``, рекурсивная ссылка на ``CalendarContract``) типизированы
    как ``dict``/``list[Any]``. Это сделано осознанно: их подсхемы (``SpecialDayContract``
    и т.п.) тянут собственные перечисления и вложенные контракты, которые относятся к
    общему домену и должны выноситься отдельно; здесь они сохраняются «как есть» без
    потери данных. Перечислимые поля верхнего уровня (``owner``, ``week_start_day``,
    ``year_start_month``, ``where_is_from_additional_calendar``) типизированы как ``str``
    (значения-enum, см. Notes).

    Обязательно только поле идентичности ``calendar_id``; прочие поля объявлены
    необязательными с дефолтами — устойчиво к различиям между календарями и версиями API.

    Attributes:
        calendar_id: Идентификатор календаря (``calendarId``).
        name: Имя календаря.
        caption: Отображаемый заголовок календаря.
        owner: Тип владельца календаря: ``calendarObject`` | ``user`` |
            ``organizationUnit``.
        unit_id: Идентификатор подразделения-владельца (если ``owner`` —
            подразделение).
        user_id: Идентификатор пользователя-владельца (если ``owner`` — пользователь).
        week_start_day: День начала недели (``monday`` … ``sunday``).
        year_start_month: Месяц начала года (``january`` … ``december``).
        days_in_month: Число рабочих дней в месяце.
        hours_in_day: Число рабочих часов в дне.
        hours_in_week: Число рабочих часов в неделе.
        default_start_hour: Час начала рабочего дня по умолчанию.
        default_start_minute: Минута начала рабочего дня по умолчанию.
        default_finish_hour: Час окончания рабочего дня по умолчанию.
        default_finish_minute: Минута окончания рабочего дня по умолчанию.
        where_is_from_additional_calendar: Источник дополнительного календаря:
            ``isInAttribute`` | ``foundInOrganization`` | ``standardCalendar``.
        additional_calendar: Дополнительный (вложенный) календарь (``CalendarContract``),
            если задан; ``None`` иначе. Структура сохраняется без разбора.
        standard_week: Стандартная рабочая неделя (``StandardWeekContract``).
        standard_work_periods: Список стандартных рабочих периодов (``WorkTimeContract``).
        special_calendar_days: Список особых дней календаря (``SpecialDayContract``).

    Notes:
        Перечислимые поля верхнего уровня приходят строками. Допустимые значения:
        ``owner`` ∈ {``calendarObject``, ``user``, ``organizationUnit``};
        ``week_start_day`` ∈ {``monday``..``sunday``};
        ``year_start_month`` ∈ {``january``..``december``};
        ``where_is_from_additional_calendar`` ∈ {``isInAttribute``,
        ``foundInOrganization``, ``standardCalendar``}.
    """

    calendar_id: int = Field(description="Идентификатор календаря")
    name: str | None = Field(default=None, description="Имя календаря")
    caption: str | None = Field(default=None, description="Заголовок календаря")
    owner: str | None = Field(default=None, description="Тип владельца календаря")
    unit_id: int | None = Field(default=None, description="Идентификатор подразделения-владельца")
    user_id: int | None = Field(default=None, description="Идентификатор пользователя-владельца")
    week_start_day: str | None = Field(default=None, description="День начала недели")
    year_start_month: str | None = Field(default=None, description="Месяц начала года")
    days_in_month: int | None = Field(default=None, description="Число рабочих дней в месяце")
    hours_in_day: float | None = Field(default=None, description="Число рабочих часов в дне")
    hours_in_week: float | None = Field(default=None, description="Число рабочих часов в неделе")
    default_start_hour: int | None = Field(
        default=None, description="Час начала рабочего дня по умолчанию"
    )
    default_start_minute: int | None = Field(
        default=None, description="Минута начала рабочего дня по умолчанию"
    )
    default_finish_hour: int | None = Field(
        default=None, description="Час окончания рабочего дня по умолчанию"
    )
    default_finish_minute: int | None = Field(
        default=None, description="Минута окончания рабочего дня по умолчанию"
    )
    where_is_from_additional_calendar: str | None = Field(
        default=None, description="Источник дополнительного календаря"
    )
    additional_calendar: dict[str, Any] | None = Field(
        default=None, description="Дополнительный (вложенный) календарь"
    )
    standard_week: dict[str, Any] | None = Field(
        default=None, description="Стандартная рабочая неделя"
    )
    standard_work_periods: Annotated[list[Any], EmptyListIfNone] = Field(
        default_factory=list, description="Стандартные рабочие периоды"
    )
    special_calendar_days: Annotated[list[Any], EmptyListIfNone] = Field(
        default_factory=list, description="Особые дни календаря"
    )
