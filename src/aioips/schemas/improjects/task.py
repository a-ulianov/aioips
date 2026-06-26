"""Схема сведений о задаче проекта IPS (Improject).

References:
    ``GET /core/api/improjects/tasks/{taskId}`` — ``TaskInfoDto``.
"""

from typing import Any

from pydantic import Field

from ..base import IPSModel


class Task(IPSModel):
    """Сведения об одной задаче проекта Improject (карточка задачи).

    Возвращается методом :meth:`task` по идентификатору задачи. Содержит контекст
    проекта (``project_id``, ``project_name``), ответ руководителя по задаче
    (``manager_answer``) и собственно данные задачи (``task_data``) — «сырое»
    представление ``TaskDto``.

    Поле ``task_data`` типизировано как ``dict[str, Any]``: DTO ``TaskDto`` обширно и
    нестабильно между версиями API (десятки полей: сроки, прогресс, назначения,
    статус и т. п.); для раздела READ достаточно доступа к нему без жёсткой схемы.
    Вложений у задачи нет в этом DTO — их получают отдельно через
    :meth:`task_attachments`.

    Обязательно лишь поле ``task_data`` (по описанию API).

    Attributes:
        task_data: Данные задачи (``TaskDto``) в виде «сырого» словаря.
        project_id: Идентификатор проекта, которому принадлежит задача.
        project_name: Наименование проекта.
        manager_answer: Ответ (резолюция) руководителя по задаче.
    """

    task_data: dict[str, Any] = Field(description="Данные задачи (TaskDto)")
    project_id: int | None = Field(default=None, description="Идентификатор проекта задачи")
    project_name: str | None = Field(default=None, description="Наименование проекта")
    manager_answer: str | None = Field(default=None, description="Ответ руководителя по задаче")
