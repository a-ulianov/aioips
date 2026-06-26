"""Схема проекта модуля управления проектами IPS (Improject).

References:
    ``GET /core/api/improjects/{projectId}`` — ``ProjectDto``.
"""

from typing import Annotated, Any

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class Project(IPSModel):
    """Проект Improject со списком задач, связей и ресурсов (план-график проекта).

    Описывает один проект управления проектами IPS: его задачи (диаграмма Ганта),
    зависимости между задачами и назначенные ресурсы. Возвращается методом
    :meth:`project` по идентификатору проекта. Отдельную задачу с подробностями
    получают через :meth:`task`.

    Вложенные коллекции (``data``, ``links``, ``resources``) и настройки отображения
    (``display_settings``) сознательно типизированы как «сырые» структуры
    (``list[dict[str, Any]]`` / ``dict[str, Any]``): соответствующие DTO (``TaskDto``,
    ``DependencyDto``, ``ResourceDto``, ``DisplaySettingsDto``) обширны, вложены и
    нестабильны между версиями API; для раздела READ достаточно верхнеуровневой
    идентичности проекта и доступа к этим структурам без жёсткой схемы.

    Обязательно лишь поле идентичности ``id``.

    Attributes:
        id: Числовой идентификатор проекта.
        data: Задачи проекта (элементы ``TaskDto``) в виде «сырых» словарей.
        links: Зависимости между задачами (элементы ``DependencyDto``).
        resources: Ресурсы проекта (элементы ``ResourceDto``).
        display_settings: Настройки отображения проекта (``DisplaySettingsDto``).
    """

    id: int = Field(description="Идентификатор проекта")
    data: Annotated[list[dict[str, Any]], EmptyListIfNone] = Field(
        default_factory=list, description="Задачи проекта (TaskDto)"
    )
    links: Annotated[list[dict[str, Any]], EmptyListIfNone] = Field(
        default_factory=list, description="Зависимости между задачами (DependencyDto)"
    )
    resources: Annotated[list[dict[str, Any]], EmptyListIfNone] = Field(
        default_factory=list, description="Ресурсы проекта (ResourceDto)"
    )
    display_settings: dict[str, Any] | None = Field(
        default=None, description="Настройки отображения проекта (DisplaySettingsDto)"
    )
