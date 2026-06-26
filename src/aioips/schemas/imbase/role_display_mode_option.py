"""Схема режима отображения таблицы IMBASE для роли.

References:
    ``GET /core/api/imbase/roleDisplayModeOptions`` — массив ``RoleDisplayModeOptionDto``.
"""

from pydantic import Field

from ..base import IPSModel


class RoleDisplayModeOption(IPSModel):
    """Режим отображения таблицы IMBASE, заданный для конкретной роли.

    Справочная система IMBASE может настраивать отображение таблиц индивидуально для
    ролей пользователей. Каждый элемент связывает роль (по её глобальному id и id
    версии) с её человекочитаемым названием — для выбора режима «по роли» в интерфейсе.

    Когда применять: при построении переключателя ролевых режимов отображения IMBASE.
    Полный набор отдаёт :meth:`imbase_role_display_mode_options`; те же данные входят
    в :class:`ImBaseClientCacheState` (поле ``role_display_mode_options``, там — как
    «сырые» словари).

    ``object_id`` — глобальный идентификатор роли (GUID/uuid), ``object_version_id`` —
    идентификатор ВЕРСИИ объекта роли (id-пространство версий).

    Attributes:
        object_id: Глобальный идентификатор роли (GUID).
        object_version_id: Идентификатор версии объекта роли.
        name: Название роли для интерфейса.
    """

    object_id: str = Field(description="Глобальный идентификатор роли (GUID)")
    object_version_id: int = Field(description="Идентификатор версии объекта роли")
    name: str = Field(description="Название роли для интерфейса")
