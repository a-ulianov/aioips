"""Схема тела запроса обновления снимка состава объекта (``UpdateSnapshotDto``).

Содержит DTO :class:`UpdateSnapshot` — параметры мутирующего запроса обновления
существующего снимка (его наименования и/или зафиксированного состава версий).
Структурно совпадает с :class:`CreateSnapshot` (тот же набор полей в swagger), но
применяется к уже созданному снимку по его id. См. [[ips-object-model]] (раздел
«Состав») и читающий метод :meth:`snapshot_composition`.

References:
    ``PUT /core/api/snapshots/{snapshotId}`` — ``Snapshots_UpdateObjectSnapshot``.
"""

from typing import Annotated, Any

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class UpdateSnapshot(IPSModel):
    """Тело запроса обновления снимка состава (``UpdateSnapshotDto``).

    Задаёт новые значения для существующего снимка: наименование, перечень версий
    элементов состава и правило контекста. Применять при изменении ранее
    созданного снимка через :meth:`update_snapshot` (мутирующая операция; сам
    снимок идентифицируется отдельным аргументом ``snapshot_id`` метода).

    Предусловие по id-пространству (критично): ``composition_object_version_ids``
    — это идентификаторы ВЕРСИЙ (F_ID) элементов состава, а НЕ id объектов
    (F_OBJECT_ID) и НЕ id самого снимка. Тот же id-набор возвращает читающий
    метод :meth:`snapshot_composition`. См. [[ips-object-model]] (раздел
    «Идентичность»).

    Attributes:
        snapshot_name: Новое наименование снимка (итерации). ``None`` — поле не
            передаётся (наименование не изменяется на стороне DTO).
        composition_object_version_ids: Новый список id версий элементов состава
            (F_ID, int64) для снимка. ``None`` нормализуется в пустой список перед
            сериализацией (снимок без явных элементов).
        context_rule: Правило контекста версий (``ContextRuleDto``) как словарь
            ``{"versionRuleObjectId": ..., "editingContextId": ...,
            "editingContextMode": ...}`` или ``None`` (контекст по умолчанию).
    """

    snapshot_name: str | None = Field(
        default=None,
        alias="snapshotName",
        description="Новое наименование снимка (итерации); None — не изменять на стороне DTO",
    )
    composition_object_version_ids: Annotated[list[int] | None, EmptyListIfNone] = Field(
        default=None,
        alias="compositionObjectVersionIds",
        description="ID версий элементов состава (F_ID); None нормализуется в пустой список",
    )
    context_rule: dict[str, Any] | None = Field(
        default=None,
        alias="contextRule",
        description="Правило контекста версий (ContextRuleDto) как словарь или None",
    )
