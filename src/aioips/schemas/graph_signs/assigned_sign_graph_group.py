"""Схемы назначенных графов подписания для архивов и шагов/уровней ЖЦ.

References:
    ``GET /api/archives/{archiveId}/signs``,
    ``GET /api/lifecycleLevels/{lifecycleLevelId}/signs``,
    ``GET /api/lifecycleSteps/{lifecycleStepId}/signs`` — массив
    ``AssignedSignGraphGroupContract``.
"""

from typing import Annotated

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class AssignedSignGraph(IPSModel):
    """Назначенный граф подписания (штамп ЭЦП) в составе группы.

    Описывает один граф подписания, назначенный архиву или уровню/шагу жизненного цикла:
    строковый идентификатор подписи (``sign_id``), её описание и признак строгой проверки
    подписи при контроле подлинности.

    Все поля необязательны с дефолтами; идентификатор и описание могут прийти ``None``.

    Attributes:
        sign_id: Строковый идентификатор графа/настройки подписи.
        sign_description: Человекочитаемое описание подписи.
        is_strong_check: Признак строгой проверки подписи (усиленный контроль подлинности).
    """

    sign_id: str | None = Field(default=None, description="Строковый идентификатор подписи")
    sign_description: str | None = Field(default=None, description="Описание подписи")
    is_strong_check: bool = Field(default=False, description="Строгая проверка подписи")


class AssignedSignGraphGroup(IPSModel):
    """Группа назначенных графов подписания (штампов ЭЦП).

    Объединяет под именованным заголовком (``name``) набор назначенных графов подписания
    (``graphs``). Возвращается для архива
    (:meth:`~aioips.IPSClient.archive_sign_settings`), уровня
    (:meth:`~aioips.IPSClient.lifecycle_level_sign_settings`) и шага
    (:meth:`~aioips.IPSClient.lifecycle_step_sign_settings`) жизненного цикла. Связан с
    разделом ``signs`` (справочники графов/рангов подписания).

    Attributes:
        name: Наименование группы подписей (может быть ``None``).
        graphs: Список назначенных графов подписания. ``null`` в ответе нормализуется в
            пустой список.
    """

    name: str | None = Field(default=None, description="Наименование группы подписей")
    graphs: Annotated[list[AssignedSignGraph], EmptyListIfNone] = Field(
        default_factory=list, description="Назначенные графы подписания"
    )
