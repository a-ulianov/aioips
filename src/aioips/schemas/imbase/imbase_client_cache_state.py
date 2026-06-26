"""Схема клиентского кэша справочной системы IMBASE.

References:
    ``GET /core/api/imbase/clientCacheState`` — ``ImBaseClientCacheStateDto``.
"""

from typing import Annotated, Any

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel
from .display_mode_option import DisplayModeOption
from .imbase_indexes_info import ImBaseIndexesInfo


class ImBaseClientCacheState(IPSModel):
    """Сводное состояние клиентского кэша справочной системы IMBASE.

    Один агрегированный снимок параметров и метаданных IMBASE, нужный клиенту для
    инициализации без серии отдельных запросов: режимы отображения, ролевые режимы,
    общие и пользовательские параметры, терминальные папки и информация об индексах.

    Когда применять: при старте клиента IMBASE для разовой загрузки всего необходимого
    состояния. Отдельные части доступны и точечно: режимы — :meth:`imbase_display_mode_options`,
    индексы — :meth:`imbase_indexes`. Предусловий нет (операция чтения).

    Поля ``common_params``, ``user_params`` и ``role_display_mode_options`` намеренно
    типизированы свободно (``dict[str, Any]`` / ``list[dict[str, Any]]``): это крупные
    вспомогательные DTO вне раздела imbase, причём у ``common_params`` один из ключей
    в swagger содержит повреждённый байт (``analуzeHiddenRecords`` с кириллической
    буквой). Жёсткая типизация дала бы хрупкость без пользы для основного сценария.

    Attributes:
        display_mode_options: Доступные режимы отображения каталога/таблицы IMBASE.
        role_display_mode_options: Ролевые режимы отображения (сырые DTO; вне раздела imbase).
        common_params: Общие параметры IMBASE (сырой DTO ``MainImBaseCommonParamsDto``).
        user_params: Пользовательские параметры IMBASE (сырой DTO ``MainImBaseUserParamsDto``).
        terminal_folder_ids: Идентификаторы терминальных (конечных) папок IMBASE.
        indexes_info: Информация об индексах IMBASE (каталоги и их индексы).
    """

    display_mode_options: Annotated[list[DisplayModeOption], EmptyListIfNone] = Field(
        default_factory=list, description="Доступные режимы отображения IMBASE"
    )
    role_display_mode_options: Annotated[list[dict[str, Any]], EmptyListIfNone] = Field(
        default_factory=list, description="Ролевые режимы отображения (сырые DTO)"
    )
    common_params: dict[str, Any] = Field(
        default_factory=dict, description="Общие параметры IMBASE (сырой DTO)"
    )
    user_params: dict[str, Any] = Field(
        default_factory=dict, description="Пользовательские параметры IMBASE (сырой DTO)"
    )
    terminal_folder_ids: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list, description="Идентификаторы терминальных папок IMBASE"
    )
    indexes_info: ImBaseIndexesInfo = Field(
        default_factory=ImBaseIndexesInfo, description="Информация об индексах IMBASE"
    )
