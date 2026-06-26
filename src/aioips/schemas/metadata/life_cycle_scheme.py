"""Схема схемы жизненного цикла метаданных IPS.

References:
    ``GET /core/api/metadata/lifeCycleSchemes`` — массив ``ImsLifeCycleSchemeDto``.
"""

from uuid import UUID

from pydantic import Field

from ..base import IPSModel


class LifeCycleScheme(IPSModel):
    """Описание схемы жизненного цикла (``ImsLifeCycleSchemeDto``).

    Схема ЖЦ — это именованный набор шагов (состояний) с правилами продвижения,
    общий для типов объектов, которые на неё ссылаются. На каждом шаге схемы
    задан режим правки атрибутов (``ObjectModifyModes``) и контроль прав; сами
    шаги конкретной схемы отдаёт метод :meth:`life_cycle_scheme_steps`. Одна из
    схем в базе может быть помечена как схема по умолчанию (``is_default``).

    Обязательны только поля идентичности (``id``, ``guid``, ``name``, ``options``,
    ``default``); ``note`` и ``area_id`` могут приходить ``null`` и объявлены
    необязательными — это устойчиво к различиям между базами и версиями API.

    Attributes:
        id: Числовой идентификатор схемы ЖЦ (id-пространство СХЕМ ЖЦ; различается
            между инсталляциями). Принимается методами, требующими ``schemeId``/``id``
            схемы ЖЦ. Это не ``ObjectTypeID`` и не идентификатор шага.
        guid: Глобальный идентификатор схемы ЖЦ (переносим между базами).
        name: Отображаемое имя схемы ЖЦ.
        note: Примечание (может отсутствовать / приходить ``null``).
        area_id: Идентификатор области данных, к которой относится схема
            (может отсутствовать / приходить ``null``).
        options: Битовая маска опций схемы ЖЦ (``int64``; в swagger — целое число,
            а не список). ``0`` — опции не заданы.
        is_default: Признак того, что это схема ЖЦ по умолчанию. JSON-ключ —
            ``default`` (зарезервированное слово), поэтому поле названо ``is_default``.
    """

    id: int = Field(description="Идентификатор схемы ЖЦ (id-пространство схем ЖЦ)")
    guid: UUID = Field(description="GUID схемы ЖЦ (переносим между базами)")
    name: str = Field(default="", description="Отображаемое имя схемы ЖЦ")
    note: str | None = Field(default=None, description="Примечание")
    area_id: str | None = Field(default=None, description="Идентификатор области данных")
    options: int = Field(default=0, description="Битовая маска опций схемы ЖЦ (int64)")
    is_default: bool = Field(
        default=False,
        alias="default",
        description="Признак схемы ЖЦ по умолчанию (JSON-ключ default)",
    )
