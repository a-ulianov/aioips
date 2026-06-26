"""Схема тела запроса создания снимка состава объекта (``CreateSnapshotDto``).

Содержит DTO :class:`CreateSnapshot` — параметры мутирующего запроса создания
нового снимка (зафиксированного состава версий) для объекта. Снимок «замораживает»
перечень версий элементов на момент создания; см. объектной модели IPS (раздел
«Состав») и читающий метод :meth:`snapshot_composition`.

References:
    ``POST /core/api/snapshots`` — ``Snapshots_CreateObjectSnapshot``.
"""

from typing import Annotated, Any

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class CreateSnapshot(IPSModel):
    """Тело запроса создания снимка состава (``CreateSnapshotDto``).

    Описывает новый снимок: его наименование, явный перечень версий элементов
    состава, которые в него войдут, и необязательное правило контекста версий.
    Применять при создании исторической точки отсчёта состава объекта через
    :meth:`create_snapshot` (мутирующая операция, вернёт id созданного снимка).

    Предусловие по id-пространству (критично): ``composition_object_version_ids``
    — это идентификаторы ВЕРСИЙ (F_ID) элементов состава, а НЕ id объектов
    (F_OBJECT_ID). Тот же id-набор возвращает читающий метод
    :meth:`snapshot_composition`. См. объектной модели IPS (раздел «Идентичность»).

    Attributes:
        snapshot_name: Наименование снимка (итерации). ``None`` — поле не
            передаётся (сервер задаст значение по умолчанию).
        composition_object_version_ids: Список id версий элементов состава
            (F_ID, int64), которые сохранить в снимке. ``None`` нормализуется в
            пустой список перед сериализацией (снимок без явных элементов).
        context_rule: Правило контекста версий (``ContextRuleDto``) как словарь
            ``{"versionRuleObjectId": ..., "editingContextId": ...,
            "editingContextMode": ...}`` или ``None`` (контекст по умолчанию).
    """

    snapshot_name: str | None = Field(
        default=None,
        alias="snapshotName",
        description="Наименование снимка (итерации); None — значение по умолчанию",
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
