"""Схема общих настроек IPS Bridge.

References:
    ``GET /core/api/Bridge/commonSettings`` — ``CommonBridgeSettingsDTO``.
"""

from pydantic import Field

from ..base import IPSModel


class CommonBridgeSettings(IPSModel):
    """Общие настройки клиентского моста IPS Bridge.

    IPS Bridge — локальный мост между толстым клиентом IPS и сервером. Эти
    настройки описывают параметры подключения к нему. Используйте схему, чтобы
    узнать, на каком порту мост принимает локальные подключения, перед запуском
    клиентских действий, делегируемых мосту.

    Attributes:
        ips_bridge_port: TCP-порт, на котором IPS Bridge принимает подключения.
            ``0`` означает, что порт не задан/мост не настроен.
    """

    ips_bridge_port: int = Field(default=0, description="Порт подключения к IPS Bridge")
