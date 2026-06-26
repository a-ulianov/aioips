"""Схема настроек видимости объекта IPS.

References:
    ``GET /api/visibilities/getDefault`` — массив ``VisibilitySettingsDto``.
"""

from pydantic import Field

from ..base import IPSModel


class VisibilitySettings(IPSModel):
    """Настройки видимости объекта (узла) в интерфейсе IPS.

    Описывает, как объект отображается по умолчанию: показан он или скрыт и какой
    значок ему сопоставлен. Возвращается методом :meth:`default_visibility_settings`
    как элемент массива дефолтных настроек видимости.

    Поля API записаны в ``camelCase`` без заглавных акронимов, поэтому достаточно
    автогенератора алиасов базовой модели (``objectId`` ↔ ``object_id`` и т. д.).
    Обязательны ``object_name`` и ``object_type``; остальные поля имеют дефолты —
    это устойчиво к различиям версий API.

    Attributes:
        object_id: Идентификатор объекта, к которому относится настройка (int64).
        object_type: Тип объекта (числовой код типа, int32).
        object_name: Наименование объекта (непустая строка).
        is_visible: Признак того, что объект отображается.
        is_hidden: Признак того, что объект скрыт.
        icon: Идентификатор/имя значка объекта (``None``, если не задан).
    """

    object_id: int = Field(default=0, description="Идентификатор объекта")
    object_type: int = Field(description="Тип объекта (числовой код)")
    object_name: str = Field(description="Наименование объекта")
    is_visible: bool = Field(default=False, description="Объект отображается")
    is_hidden: bool = Field(default=False, description="Объект скрыт")
    icon: str | None = Field(default=None, description="Идентификатор/имя значка объекта")
