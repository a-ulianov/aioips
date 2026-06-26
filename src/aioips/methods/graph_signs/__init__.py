"""Методы раздела графических подписей (штампов ЭЦП) IPS Web API."""

from .archive_sign_settings import ArchiveSignSettingsMixin
from .lifecycle_level_sign_settings import LifecycleLevelSignSettingsMixin
from .lifecycle_step_sign_settings import LifecycleStepSignSettingsMixin
from .object_type_lifecycle_step_sign_settings import (
    ObjectTypeLifecycleStepSignSettingsMixin,
)
from .rank_graph_sign_object_types import RankGraphSignObjectTypesMixin
from .rank_graph_signs import RankGraphSignsMixin
from .save_rank_graph_signs import SaveRankGraphSignsMixin
from .update_archive_sign_settings import UpdateArchiveSignSettingsMixin
from .update_lifecycle_level_sign_settings import UpdateLifecycleLevelSignSettingsMixin
from .update_lifecycle_step_sign_settings import UpdateLifecycleStepSignSettingsMixin
from .update_object_type_lifecycle_step_sign_settings import (
    UpdateObjectTypeLifecycleStepSignSettingsMixin,
)


class GraphSignsAPI(
    RankGraphSignObjectTypesMixin,
    RankGraphSignsMixin,
    ArchiveSignSettingsMixin,
    LifecycleLevelSignSettingsMixin,
    LifecycleStepSignSettingsMixin,
    ObjectTypeLifecycleStepSignSettingsMixin,
    UpdateArchiveSignSettingsMixin,
    UpdateLifecycleLevelSignSettingsMixin,
    UpdateLifecycleStepSignSettingsMixin,
    UpdateObjectTypeLifecycleStepSignSettingsMixin,
    SaveRankGraphSignsMixin,
):
    """Объединяет методы раздела графических подписей (настройки штампов ЭЦП).

    Настройки графических подписей задаются для рангов, архивов и уровней/шагов
    жизненного цикла. Раздел тесно связан со справочниками раздела ``signs``
    (графы и ранги подписания).

    References:
        Эндпоинты ``/api/ranks/*/graphSigns``, ``/api/archives/*/signs``,
        ``/api/lifecycleLevels/*/signs``, ``/api/lifecycleSteps/*/signs``
        IPS Server Web API.
    """


__all__ = ["GraphSignsAPI"]
