"""Схема информации о снимках объекта IPS.

Снимок (snapshot) — зафиксированное состояние объекта (как правило, состава) на
момент времени; у объекта может быть несколько снимков и один активный.

References:
    ``GET /core/api/objects/{objectId}/snapshots/info`` — ``Snapshots_GetObjectSnapshotInfo``
    (``SnapshotInfoDto``).
"""

from typing import Annotated

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class ObjectSnapshot(IPSModel):
    """Один снимок объекта (элемент коллекции снимков).

    Описывает зафиксированное состояние объекта: его идентификатор и наименование.
    Возвращается как элемент списка :attr:`SnapshotInfo.object_snapshot_collection`.

    Attributes:
        snapshot_id: Идентификатор снимка (int64); используется как ``snapshot_id`` в
            :meth:`object_snapshot_readonly_objects`.
        name: Наименование снимка (``None``, если не задано).
    """

    snapshot_id: int = Field(default=0, description="Идентификатор снимка")
    name: str | None = Field(default=None, description="Наименование снимка")


class SnapshotInfo(IPSModel):
    """Сводная информация о снимках объекта: активный снимок и их коллекция.

    Описывает, какой снимок объекта активен и какие снимки у него есть. Возвращается
    методом :meth:`object_snapshot_info`. Поле ``active_snapshot_id`` равно ``None``,
    если у объекта нет активного снимка; коллекция приходит ``null`` при отсутствии
    снимков и нормализуется в пустой список (``EmptyListIfNone``).

    Поля API записаны в ``camelCase`` без заглавных акронимов (``activeSnapshotId``,
    ``objectSnapshotCollection``), поэтому достаточно автогенератора алиасов базовой
    модели.

    Attributes:
        active_snapshot_id: Идентификатор активного снимка объекта (int64) или
            ``None``, если активного снимка нет.
        object_snapshot_collection: Коллекция снимков объекта (возможно пустая); каждый
            элемент — :class:`ObjectSnapshot`.
    """

    active_snapshot_id: int | None = Field(
        default=None, description="Идентификатор активного снимка объекта"
    )
    object_snapshot_collection: Annotated[list[ObjectSnapshot], EmptyListIfNone] = Field(
        default_factory=list, description="Коллекция снимков объекта"
    )
