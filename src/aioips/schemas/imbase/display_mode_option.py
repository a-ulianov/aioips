"""Схема варианта режима отображения справочной системы IMBASE.

References:
    ``GET /core/api/imbase/displayModeOptions`` — массив ``DisplayModeOptionDto``.
"""

from pydantic import Field

from ..base import IPSModel


class DisplayModeOption(IPSModel):
    """Доступный режим отображения каталога/таблицы IMBASE и его название.

    Справочная система IMBASE может показывать содержимое каталога/таблицы в
    нескольких режимах (общий, персональный, по роли). Каждый элемент описывает
    один доступный режим и его человекочитаемое название для интерфейса.

    Когда применять: при построении переключателя режимов отображения IMBASE на
    клиенте. Полный набор доступных режимов отдаёт :meth:`imbase_display_mode_options`;
    также этот список присутствует в :class:`ImBaseClientCacheState`
    (поле ``display_mode_options``).

    Значения ``mode`` (enum ``DisplayMode`` из swagger): ``generalMode`` (общий),
    ``personalMode`` (персональный), ``roleMode`` (по роли). Поле типизировано как
    ``str``, чтобы не отвергать значения, не предусмотренные текущей версией клиента.

    Attributes:
        mode: Идентификатор режима отображения (``generalMode``/``personalMode``/
            ``roleMode``).
        name: Человекочитаемое название режима для интерфейса.
    """

    mode: str = Field(description="Режим отображения IMBASE (generalMode/personalMode/roleMode)")
    name: str = Field(description="Название режима отображения для интерфейса")
