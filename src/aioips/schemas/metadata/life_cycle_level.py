"""Схема уровня жизненного цикла метаданных IPS.

References:
    ``GET /core/api/metadata/lifeCycleLevels`` — массив ``ImsLifeCycleLevelDto``.
"""

from uuid import UUID

from pydantic import Field

from ..base import IPSModel


class LifeCycleLevel(IPSModel):
    """Описание уровня жизненного цикла (УЖЦ) в метаданных IPS.

    Уровень ЖЦ — горизонтальный «слой зрелости» объекта (например «В разработке»,
    «Утверждено», «Архив»), общий для разных типов объектов; ему соответствует
    литера документа и физическое хранилище версий. Шаги ЖЦ конкретного типа
    объекта (``LifeCycleStep``) ссылаются на уровень через ``levelId``. Уровни
    образуют отдельное id-пространство УРОВНЕЙ — не путать с ``LifeCycleStep.id``
    (шаг), ``ObjectTypeID`` (тип объекта) или ``ObjectID``/``ID`` объекта/версии.

    Обязательны поля идентичности и состояния (``id``, ``guid``, ``name``,
    ``storage_id``, ``is_default``); ``area_id`` и ``litera`` приходят как ``null``,
    поэтому объявлены необязательными.

    Attributes:
        id: Числовой идентификатор уровня ЖЦ (``LifeCycleLevelID``; локальный, может
            различаться между инсталляциями). Принимается методами по ``id``.
        guid: Глобальный идентификатор уровня ЖЦ (стабилен между базами, переносим).
        name: Отображаемое имя уровня ЖЦ (например «Утверждено»).
        area_id: Идентификатор области данных (``areaId``); ``None``, если не задан.
        litera: Литера документа на этом уровне (в терминах ЕСКД); ``None``, если
            литера для уровня не предусмотрена.
        storage_id: Идентификатор хранилища (``storageId``), в которое попадают файлы
            версий объекта при переводе на этот уровень. ``0`` — хранилище не задано.
        is_default: Признак уровня ЖЦ по умолчанию (алиас JSON-ключа ``default``):
            ``True`` — уровень, присваиваемый объектам по умолчанию.
    """

    id: int = Field(description="LifeCycleLevelID уровня ЖЦ (id-пространство уровней)")
    guid: UUID = Field(description="GUID уровня ЖЦ (переносим между базами)")
    name: str = Field(default="", description="Отображаемое имя уровня ЖЦ")
    area_id: str | None = Field(
        default=None, alias="areaId", description="Идентификатор области данных"
    )
    litera: str | None = Field(default=None, description="Литера документа на уровне (ЕСКД)")
    storage_id: int = Field(
        default=0, alias="storageId", description="Идентификатор хранилища (0 — не задано)"
    )
    is_default: bool = Field(default=False, alias="default", description="Уровень ЖЦ по умолчанию")
