"""Схема сведений о плагине IPS Bridge.

References:
    ``GET /core/api/Bridge/GetPlugins`` — массив ``PluginInfoDTO``.
"""

from pydantic import Field

from ..base import IPSModel


class PluginInfo(IPSModel):
    """Сведения о клиентском плагине, зарегистрированном в IPS Bridge.

    Плагины расширяют функциональность клиента IPS через мост. Схема описывает
    один зарегистрированный плагин: его объектный идентификатор, имя и сведения
    о сборке-носителе. Применяйте, чтобы перечислить доступные плагины и их
    версии (например, для диагностики совместимости).

    Attributes:
        object_id: Идентификатор объекта плагина в IPS.
        plugin_name: Имя плагина.
        assembly_name: Имя .NET-сборки, реализующей плагин.
        assembly_version: Версия сборки плагина.
    """

    object_id: int = Field(description="Идентификатор объекта плагина")
    plugin_name: str | None = Field(default=None, description="Имя плагина")
    assembly_name: str | None = Field(default=None, description="Имя сборки, реализующей плагин")
    assembly_version: str | None = Field(default=None, description="Версия сборки плагина")
