"""Схема данных безопасности пользователя IPS.

References:
    ``POST /core/api/settings/getSecurityData`` — массив ``UserSecurityData``.
"""

from pydantic import Field

from ..base import IPSModel
from .security_groups import ToolSecurityGroup


class UserSecurityData(IPSModel):
    """Данные безопасности пользователя: связка ``userId`` ↔ группа инструментов.

    Описывает, к какой группе безопасности инструментов
    (:class:`ToolSecurityGroup`) отнесён конкретный пользователь. Метод
    :meth:`~aioips.IPSClient.security_data` возвращает массив таких записей —
    по одной на пользователя, для которого заданы данные безопасности.

    Когда применять: чтобы перечислить пользователей и их группы инструментов
    либо найти группу конкретного пользователя по ``user_id``. Для группы и прав
    именно текущего пользователя есть отдельные методы
    :meth:`~aioips.IPSClient.user_group` и :meth:`~aioips.IPSClient.user_rights`.

    Attributes:
        user_id: Идентификатор пользователя IPS, к которому относится запись.
        security_group: Группа безопасности инструментов пользователя
            (:class:`ToolSecurityGroup`); ``None``, если не задана.
    """

    user_id: int = Field(description="Идентификатор пользователя")
    security_group: ToolSecurityGroup | None = Field(
        default=None, description="Группа безопасности инструментов пользователя"
    )
