"""Схема назначений ресурсов проектов IPS (Improject).

References:
    ``GET /core/api/improjects/resourceAssignments`` — ``ResourceAssignmentsDto``.
"""

from typing import Annotated, Any

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class ResourceAssignments(IPSModel):
    """Назначения ресурсов на задачи проектов (загрузка ресурсов по задачам).

    Возвращается методом :meth:`resource_assignments`. Сводит вместе задачи
    (``data``), участвующие ресурсы (``resources``) и идентификаторы пользователей
    (``users``), позволяя оценить занятость ресурсов по задачам проектов.

    Коллекции ``data`` и ``resources`` типизированы как «сырые» структуры
    (``list[dict[str, Any]]``): соответствующие DTO (``TaskDto``, ``ResourceDto``)
    обширны и нестабильны между версиями API; для раздела READ достаточно доступа к
    ним без жёсткой схемы. ``users`` — простой список идентификаторов пользователей.

    Обязательных полей нет — все коллекции по умолчанию пусты.

    Attributes:
        data: Задачи, по которым считаются назначения (элементы ``TaskDto``).
        resources: Назначенные ресурсы (элементы ``ResourceDto``).
        users: Идентификаторы пользователей, участвующих в назначениях.
    """

    data: Annotated[list[dict[str, Any]], EmptyListIfNone] = Field(
        default_factory=list, description="Задачи назначений (TaskDto)"
    )
    resources: Annotated[list[dict[str, Any]], EmptyListIfNone] = Field(
        default_factory=list, description="Назначенные ресурсы (ResourceDto)"
    )
    users: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list, description="Идентификаторы пользователей назначений"
    )
