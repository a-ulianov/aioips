"""Схемы настроек графических подписей (штампов ЭЦП) для рангов.

References:
    ``GET /api/ranks/{rankId}/graphSigns`` — массив ``RankGraphSignsContract``.
"""

from typing import Annotated

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class RankGraphSignsSettings(IPSModel):
    """Настройка одного графа подписания для ранга (правила штампа ЭЦП).

    Описывает, как конкретный граф подписания (``graph_id`` — строковый ключ графа из
    справочника :meth:`~aioips.IPSClient.sign_graphs`) разрешён к применению для ранга:
    допустимость простой и/или усиленной (криптографической) подписи и запрет
    множественного подписания.

    Все поля необязательны с дефолтами — устойчиво к различиям между графами и версиями
    API; идентификатор графа может прийти ``None``, если граф не задан.

    Attributes:
        graph_id: Строковый ключ графа подписания (ссылка на ``id`` из ``sign_graphs``).
        is_ban_multiple_sign: Запрет множественного (повторного) подписания этим графом.
        is_allow_simple_sign: Разрешена простая электронная подпись.
        is_allow_crypto_sign: Разрешена усиленная (криптографическая) электронная подпись.
    """

    graph_id: str | None = Field(default=None, description="Строковый ключ графа подписания")
    is_ban_multiple_sign: bool = Field(
        default=False, description="Запрет множественного подписания"
    )
    is_allow_simple_sign: bool = Field(default=False, description="Разрешена простая подпись")
    is_allow_crypto_sign: bool = Field(
        default=False, description="Разрешена криптографическая подпись"
    )


class RankGraphSigns(IPSModel):
    """Настройки графических подписей ранга, сгруппированные по типу объекта.

    Связывает тип объекта (``object_type_id``) с набором настроек графов подписания
    (``graphs``), применимых к объектам этого типа в рамках ранга. Список доступных для
    добавления типов объектов отдаёт
    :meth:`~aioips.IPSClient.rank_graph_sign_object_types`, а сам набор настроек ранга —
    :meth:`~aioips.IPSClient.rank_graph_signs`.

    Attributes:
        object_type_id: Идентификатор типа объекта, к которому относятся настройки.
        graphs: Список настроек графов подписания для данного типа объекта. ``null`` в
            ответе нормализуется в пустой список.
    """

    object_type_id: int = Field(description="Идентификатор типа объекта")
    graphs: Annotated[list[RankGraphSignsSettings], EmptyListIfNone] = Field(
        default_factory=list, description="Настройки графов подписания для типа объекта"
    )
