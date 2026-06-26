"""Схема цвета виджета форм IPS.

References:
    ``GET /core/api/forms/getColors`` и ``GET /core/api/forms/getSystemColors`` —
    массивы ``WidgetColor``.
"""

from pydantic import Field

from ..base import IPSModel


class WidgetColor(IPSModel):
    """Цвет из палитры виджетов форм IPS (DTO ``WidgetColor``).

    Описывает один именованный цвет, применяемый при оформлении виджетов на формах.
    Цвет задан и текстовым представлением (``color_rgba`` в формате строки), и
    отдельными компонентами ``r``/``g``/``b``/``a`` (0..255), что позволяет как
    отрисовать цвет, так и сопоставить его по имени.

    Когда применять: для интерпретации результата :meth:`widget_colors` (пользовательская
    палитра форм) или :meth:`system_colors` (системная палитра). Обе возвращают список
    таких записей; различие — источник палитры, структура одна и та же.

    Все поля необязательны: имя/строка цвета могут отсутствовать (``None``), а
    компоненты по умолчанию ``0`` (чёрный, полностью прозрачный при ``a = 0``).

    Attributes:
        color_name: Имя цвета (``colorName``), например системное или пользовательское.
        color_rgba: Строковое представление цвета в формате RGBA (``colorRGBA``).
        a: Компонента альфа-канала (прозрачность), 0..255.
        r: Компонента красного канала, 0..255.
        g: Компонента зелёного канала, 0..255.
        b: Компонента синего канала, 0..255.
    """

    color_name: str | None = Field(default=None, alias="colorName", description="Имя цвета")
    color_rgba: str | None = Field(
        default=None, alias="colorRGBA", description="Строковое представление цвета RGBA"
    )
    a: int = Field(default=0, description="Альфа-канал (прозрачность), 0..255")
    r: int = Field(default=0, description="Красный канал, 0..255")
    g: int = Field(default=0, description="Зелёный канал, 0..255")
    b: int = Field(default=0, description="Синий канал, 0..255")
