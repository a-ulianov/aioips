"""Перечисление масштаба шкалы времени диаграммы Ганта (Improject).

References:
    ``POST /core/api/improjects/{projectId}/saveZoomLevel`` — query ``scaleType``
    (``ScaleType``).
"""

from enum import StrEnum


class ScaleType(StrEnum):
    """Масштаб (уровень детализации) шкалы времени диаграммы Ганта проекта.

    Задаёт цену деления горизонтальной шкалы времени на диаграмме Ганта
    проекта Improject. Применяйте как значение параметра ``scale_type`` метода
    :meth:`save_project_zoom_level`, чтобы сохранить выбранный пользователем
    масштаб отображения план-графика. Значение сериализуется как строка
    (``StrEnum``) и передаётся в query-параметре ``scaleType``.

    Члены:
        DAYS: ``days`` — деления по дням.
        WEEKS: ``weeks`` — деления по неделям.
        MONTHS: ``months`` — деления по месяцам.
        QUARTERS: ``quarters`` — деления по кварталам.
        YEARS: ``years`` — деления по годам.

    Notes:
        Соответствует enum ``ScaleType`` IPS Web API. Связанный метод:
        :meth:`save_project_zoom_level`.
    """

    DAYS = "days"
    WEEKS = "weeks"
    MONTHS = "months"
    QUARTERS = "quarters"
    YEARS = "years"
