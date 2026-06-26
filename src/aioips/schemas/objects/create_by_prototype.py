"""Схема тела запроса создания объекта по прототипу.

DTO запроса для ``POST /core/api/objects/CreateByPrototype``
(``Objects_CreateByPrototype``). Прототип — это объект-образец, по которому
создаётся новый объект (копируются тип и применимые атрибуты). Контекст версий и
текущий проект — необязательные «сырые» словари серверных DTO (``ContextRuleDto``,
``CurrentProjectDto``), чтобы не фиксировать здесь их полную структуру.

References:
    ``POST /core/api/objects/CreateByPrototype`` — ``Objects_CreateByPrototype``.
"""

from typing import Any

from pydantic import Field

from ..base import IPSModel


class CreateObjectByPrototype(IPSModel):
    """Параметры создания объекта по прототипу (тело ``object_create_by_prototype``).

    Задаёт объект-прототип (``prototype_id``) и необязательные модификаторы: признак
    создания изделия (``is_article``), правило контекста версий (``context_rule``) и
    дескриптор текущего проекта (``current_project``). Объект создаётся в режиме
    создания (черновик) — фиксация выполняется отдельно (см. :meth:`object_commit_creation`).

    Attributes:
        prototype_id: Идентификатор объекта-прототипа (``prototypeId``), по которому
            создаётся новый объект (обязателен).
        is_article: Если ``True``, создаётся изделие (``isArticle``); ``None`` —
            серверное значение по умолчанию (поле не передаётся).
        context_rule: Правило контекста версий (``ContextRuleDto``) как словарь либо
            ``None`` (контекст по умолчанию).
        current_project: Дескриптор текущего проекта (``CurrentProjectDto``) как словарь
            либо ``None`` (без привязки к проекту).
    """

    prototype_id: int = Field(
        alias="prototypeId", description="Идентификатор объекта-прототипа (обязателен)"
    )
    is_article: bool | None = Field(
        default=None, alias="isArticle", description="True — создаётся изделие (isArticle)"
    )
    context_rule: dict[str, Any] | None = Field(
        default=None,
        alias="contextRule",
        description="Правило контекста версий (ContextRuleDto) как словарь или None",
    )
    current_project: dict[str, Any] | None = Field(
        default=None,
        alias="currentProjectDto",
        description="Дескриптор текущего проекта (CurrentProjectDto) как словарь или None",
    )
