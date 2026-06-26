"""Схема тела добавления объектов в состав по шаблону-таблице.

DTO запроса для ``POST /core/api/objects/{objectId}/addObjectsByTemplate``
(``Objects_AddObjectsByTemplate``). По шаблону-таблице (``template_id``) в состав
объекта добавляются строки-объекты; ``object_ids`` задаёт двумерный набор
идентификаторов (по строкам шаблона), либо ``None`` — добавить все строки шаблона.

References:
    ``POST /core/api/objects/{objectId}/addObjectsByTemplate`` —
    ``Objects_AddObjectsByTemplate``.
"""

from typing import Annotated, Any

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class AddObjectsByTemplateBody(IPSModel):
    """Параметры добавления объектов в состав по шаблону (тело ``..._add_objects_by_template``).

    Задаёт шаблон-таблицу (``template_id``) и набор идентификаторов объектов
    ``object_ids`` (список списков id — по строкам шаблона); если ``None`` — будут
    добавлены все строки шаблона. Необязательное ``context_rule`` уточняет контекст
    версий и передаётся «сырым» словарём серверного ``ContextRuleDto``.

    Attributes:
        template_id: Идентификатор шаблона-таблицы (``templateId``), по которому
            добавляются объекты в состав (обязателен).
        object_ids: Двумерный список id объектов по строкам шаблона
            (``list[list[int]]``); ``None`` — добавить все строки шаблона.
        context_rule: Правило контекста версий (``ContextRuleDto``) как словарь либо
            ``None`` (контекст по умолчанию).
    """

    template_id: int = Field(
        alias="templateId", description="Идентификатор шаблона-таблицы (обязателен)"
    )
    object_ids: Annotated[list[list[int]] | None, EmptyListIfNone] = Field(
        default=None,
        alias="objectIds",
        description="Список списков id объектов по строкам шаблона; None — все строки",
    )
    context_rule: dict[str, Any] | None = Field(
        default=None,
        alias="contextRule",
        description="Правило контекста версий (ContextRuleDto) как словарь или None",
    )
