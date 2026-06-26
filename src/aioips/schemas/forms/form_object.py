"""Схема объекта-результата форменных поисков IPS.

References:
    ``POST /core/api/forms/findApplicability`` · ``findCollection`` · ``findComposition`` ·
    ``findObjectsList`` — массив ``FormObjectDto``. Базовые поля идентичности — как в
    ``IEntityDto`` (``id``/``versionID``/``typeID``/``caption``).
"""

from typing import Annotated, Any
from uuid import UUID

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class FormObjectDto(IPSModel):
    """Объект, найденный форменным поиском IPS (DTO ``FormObjectDto``).

    Лёгкое представление сущности-объекта в контексте формы: идентичность, заголовок,
    тип, признак «только чтение» и набор атрибутов-колонок. Возвращается методами
    форменных поисков (`find*`), которые подбирают применимость/коллекцию/состав/список
    объектов по параметрам формы.

    Когда применять: при интерпретации результата :meth:`forms_find_applicability`,
    :meth:`forms_find_collection`, :meth:`forms_find_composition`,
    :meth:`forms_find_objects_list` — например, чтобы вывести подобранные формой объекты
    в таблице (с заголовком и значениями колонок-атрибутов).

    Предупреждение об id-пространствах (критично, см. [[ips-object-model]]): поле ``id``
    здесь — идентификатор ВЕРСИИ объекта (F_ID), а поле ``version_id`` — также версия
    (``versionID``); идентификатор ОБЪЕКТА (F_OBJECT_ID, ``objectID``) этот DTO не несёт.
    Для разворота версии в объект используйте методы раздела objects.

    В swagger поля ``id``/``versionID``/``typeID``/``caption`` помечены required, но для
    устойчивости к различиям версий API необязательные поля объявлены с дефолтами.
    Атрибуты-колонки моделируются как сырые ``dict`` (структура ``AttributeDto`` обширна,
    нестабильна и наружу отдаётся как есть).

    Attributes:
        id: Идентификатор ВЕРСИИ объекта (``id`` / F_ID); первичный идентификатор DTO.
        version_id: Идентификатор версии сущности (``versionID``); обычно совпадает с ``id``.
        type_id: Идентификатор типа сущности (``typeID`` в метамодели IPS).
        caption: Заголовок (отображаемое имя) объекта.
        version_guid: GUID версии объекта (``versionGuid``).
        read_only: Признак «только чтение» (``readOnly``) для найденного объекта.
        attributes: Атрибуты-колонки объекта (``attributes``, swagger ``AttributeDto``);
            список сырых объектов, ``null`` нормализуется в пустой список.
    """

    id: int = Field(default=0, description="Идентификатор версии объекта (F_ID)")
    version_id: int | None = Field(
        default=None, alias="versionID", description="Идентификатор версии сущности"
    )
    type_id: int | None = Field(
        default=None, alias="typeID", description="Идентификатор типа сущности"
    )
    caption: str | None = Field(default=None, description="Заголовок объекта")
    version_guid: UUID | None = Field(
        default=None, alias="versionGuid", description="GUID версии объекта"
    )
    read_only: bool = Field(default=False, alias="readOnly", description="Признак «только чтение»")
    attributes: Annotated[list[dict[str, Any]], EmptyListIfNone] = Field(
        default_factory=list, description="Атрибуты-колонки объекта (AttributeDto)"
    )
