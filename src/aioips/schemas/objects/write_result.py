"""Схемы результата операций записи атрибутов объекта IPS.

Методы записи атрибутов (set/delete/cleanup) на сервере оборачивают полезный
результат в DTO вида ``…ProcessResultWithLogInfoDto`` с двумя полями: ``result``
(собственно результат — список значений атрибутов, список атрибутов или «ничего»)
и ``modificationsHistory`` (журнал произведённых изменений). Методы-обёртки aioips
разворачивают эту структуру и обычно возвращают только ``result``; полный журнал
доступен через схему :class:`ModificationEntry`.

Списочные поля могут прийти от IPS как ``null`` вместо ``[]`` — нормализуются
валидатором ``EmptyListIfNone`` (см. [[gotchas]]). См. [[ips-object-model]]
(раздел «Редактирование»).

References:
    ``…ProcessResultWithLogInfoDto`` и ``ModificationsHistoryDto`` в swagger IPS.
"""

from uuid import UUID

from pydantic import Field

from ..base import IPSModel


class ModificationEntry(IPSModel):
    """Одна запись журнала изменений, произведённых операцией записи.

    Возвращается в поле ``modificationsHistory`` ответов методов записи, если
    журналирование истории изменений включено (``log_history=True``). Описывает,
    над какой сущностью и какое действие было выполнено.

    Attributes:
        category_type: Идентификатор типа категории (метаданных) изменённой сущности.
        category_id: Идентификатор изменённой сущности (объекта/атрибута).
        category_guid: GUID изменённой сущности.
        action_id: Тип действия (``ActionType``, напр. ``edit``/``delete``/``write``).
        metadata_type_id: Идентификатор метаданных, к которым относится действие
            (тип атрибута, объекта и т.п.).
        proj_id: Идентификатор родительского информационного объекта (``ObjectID``).
    """

    category_type: int | None = Field(
        default=None, description="Идентификатор типа категории изменённой сущности"
    )
    category_id: int | None = Field(
        default=None, alias="categoryID", description="Идентификатор изменённой сущности"
    )
    category_guid: UUID | None = Field(default=None, description="GUID изменённой сущности")
    action_id: str | None = Field(
        default=None, alias="actionID", description="Тип действия (ActionType)"
    )
    metadata_type_id: int | None = Field(
        default=None,
        alias="metadataTypeID",
        description="Идентификатор метаданных, к которым относится действие",
    )
    proj_id: int | None = Field(
        default=None,
        alias="projID",
        description="Идентификатор родительского объекта (ObjectID)",
    )
