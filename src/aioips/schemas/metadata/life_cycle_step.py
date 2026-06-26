"""Схема шага жизненного цикла типа объекта IPS.

References:
    ``GET /core/api/metadata/objectTypes/{objectTypeId}/lifeCycleSteps`` —
    массив ``ImsLifeCycleStepDto`` (в обёртке ``...ListNullableResultDto``).
"""

from typing import Annotated
from uuid import UUID

from pydantic import Field

from ...common.enumerations import ObjectModifyMode
from ..base import EmptyListIfNone, IPSModel


class LifeCycleStep(IPSModel):
    """Краткое описание шага жизненного цикла (``ImsLifeCycleStepDto``).

    Шаг жизненного цикла принадлежит схеме ЖЦ типа объекта и определяет, в каком
    режиме на этом шаге допускается правка атрибутов объекта (``object_modify_mode``)
    и какой контроль прав действует (``access_type``). Текущий шаг конкретного
    объекта хранится в ``ObjectDto.lc_step`` и сопоставляется со списком шагов типа.

    Когда применять: чтобы по типу объекта понять граф/набор шагов ЖЦ — например,
    выяснить, в каком режиме (``inBase``/``checkout``/``createVersion``/``cantModify``)
    разрешено редактирование на конкретном шаге, прежде чем выполнять запись. Список
    шагов отдаёт метод :meth:`object_type_life_cycle_steps`.

    Attributes:
        id: Идентификатор шага жизненного цикла (id-пространство шагов ЖЦ).
        guid: Глобальный идентификатор шага жизненного цикла (переносим между базами).
        scheme_id: Идентификатор схемы ЖЦ, к которой относится шаг.
        level_id: Идентификатор уровня продвижения для данного шага.
        name: Название шага жизненного цикла.
        note: Комментарий (может отсутствовать).
        object_type_id: Идентификатор типа объекта (в контексте кэша метаданных
            не используется, обычно ``0``).
        access_type: Тип контроля прав доступа на шаге (``LCAccessTypes``):
            ``noCheck``/``checkLCOnly``/``checkAll``.
        is_deleted: Признак того, что шаг удалён.
        object_modify_mode: Режим правки объектов на данном шаге
            (``inBase``/``checkout``/``createVersion``/``cantModify``).
        is_first_step: Признак первого шага в схеме жизненного цикла.
        options: Опции шага ЖЦ (``LCStepOptions``); ``null`` нормализуется в ``[]``.
    """

    id: int = Field(description="Идентификатор шага жизненного цикла")
    guid: UUID = Field(description="GUID шага жизненного цикла (переносим между базами)")
    scheme_id: int | None = Field(default=None, description="Идентификатор схемы ЖЦ шага")
    level_id: int | None = Field(default=None, description="Идентификатор уровня продвижения")
    name: str = Field(default="", description="Название шага жизненного цикла")
    note: str | None = Field(default=None, description="Комментарий")
    object_type_id: int | None = Field(
        default=None, description="Идентификатор типа объекта (в кэше метаданных обычно 0)"
    )
    access_type: str | None = Field(
        default=None, description="Тип контроля прав на шаге (LCAccessTypes)"
    )
    is_deleted: bool | None = Field(default=None, description="Признак удалённого шага")
    object_modify_mode: ObjectModifyMode | None = Field(
        default=None, description="Режим правки объектов на шаге (ObjectModifyModes)"
    )
    is_first_step: bool | None = Field(default=None, description="Признак первого шага в схеме ЖЦ")
    options: Annotated[list[str], EmptyListIfNone] = Field(
        default_factory=list, description="Опции шага ЖЦ (LCStepOptions)"
    )
