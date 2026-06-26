"""Схемы тел запросов действий запуска IPS Bridge.

References:
    ``POST /core/api/Bridge/Launch/GetActionList`` — ``LaunchActionDto``;
    ``POST /core/api/Bridge/Launch/CreateLaunchAction`` — ``CreateLaunchActionDto``.
"""

from enum import StrEnum
from uuid import UUID

from pydantic import Field

from ..base import IPSModel


class LaunchType(StrEnum):
    """Режим запуска объекта действием IPS Bridge.

    Описывает, для какого сценария предназначено действие запуска (launch
    action): редактирование, просмотр или печать объекта на стороне клиента.

    Attributes:
        EDIT: Открыть объект на редактирование.
        VIEW: Открыть объект на просмотр.
        PRINT: Отправить объект на печать.
    """

    EDIT = "edit"
    VIEW = "view"
    PRINT = "print"


class LaunchActionDto(IPSModel):
    """Тело запроса фильтра списка действий запуска IPS Bridge.

    Задаёт критерии выборки действий запуска для метода
    :meth:`bridge_get_action_list`: тип объекта, пользователь и режим запуска.
    Любое поле необязательно; незаданные критерии не сужают выборку.

    Attributes:
        object_type_id: Идентификатор типа объекта, для которого нужны действия.
        user_id: Идентификатор пользователя (``None`` — текущий/любой).
        launch_type: Режим запуска :class:`LaunchType` (``None`` — любой).
    """

    object_type_id: int | None = Field(default=None, description="Идентификатор типа объекта")
    user_id: int | None = Field(default=None, description="Идентификатор пользователя")
    launch_type: LaunchType | None = Field(default=None, description="Режим запуска")


class CreateLaunchActionDto(IPSModel):
    """Тело запроса создания действия запуска IPS Bridge.

    Описывает новое действие запуска (launch action) для метода
    :meth:`bridge_create_launch_action`: обработчик, его XML-настройки, тип
    объекта, пользователя и режим запуска.

    Attributes:
        handler_id: GUID обработчика действия (обязателен).
        settings_xml: XML-настройки действия (``None`` — без настроек).
        object_type_id: Идентификатор типа объекта, к которому привязано действие.
        user_id: Идентификатор пользователя-владельца (``None`` — общесистемное).
        launch_type: Режим запуска :class:`LaunchType` (``None`` — не задан).
    """

    handler_id: UUID = Field(description="GUID обработчика действия")
    settings_xml: str | None = Field(default=None, description="XML-настройки действия")
    object_type_id: int | None = Field(default=None, description="Идентификатор типа объекта")
    user_id: int | None = Field(default=None, description="Идентификатор пользователя")
    launch_type: LaunchType | None = Field(default=None, description="Режим запуска")
