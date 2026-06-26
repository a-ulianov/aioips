"""Схема сведений о действии запуска IPS Bridge.

References:
    ``GET /core/api/Bridge/Launch/GetUserDefinedLaunchAction``,
    ``GET /core/api/Bridge/Launch/GetLaunchActionInfo`` — ``LaunchActionInfo``.
"""

from uuid import UUID

from pydantic import Field

from ..base import IPSModel


class LaunchActionInfo(IPSModel):
    """Сведения о действии запуска (launch action) IPS Bridge.

    Действие запуска описывает операцию, которую IPS Bridge выполняет над
    объектом на стороне клиента (например, открыть документ внешним приложением).
    Схема несёт идентификатор действия, идентификатор его обработчика и
    отображаемое имя. Применяйте, чтобы определить действие перед запуском или
    получить его данные через :meth:`bridge_launch_action_data`.

    Attributes:
        action_id: Глобальный идентификатор действия запуска.
        handler_id: Глобальный идентификатор обработчика действия.
        display_name: Отображаемое имя действия для пользователя.
    """

    action_id: UUID = Field(description="Идентификатор действия запуска")
    handler_id: UUID = Field(description="Идентификатор обработчика действия")
    display_name: str | None = Field(default=None, description="Отображаемое имя действия")
