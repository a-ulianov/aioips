"""Схема сведений о структуре условий поисковой выборки IPS.

References:
    ``GET /core/api/searchSchemes/{selectionId}/getConditionStructureInfo`` —
    массив ``ConditionStructureInfoDto``.
"""

from pydantic import Field

from ..base import IPSModel
from .search_scheme import AttributeSourceType


class ConditionStructureInfo(IPSModel):
    """Сведения об одном атрибуте в структуре условий выборки (``ConditionStructureInfoDto``).

    Описывает, какой атрибут участвует в условиях фильтрации заданной выборки и из
    какого источника берётся его значение. Полный список таких элементов задаёт
    набор атрибутов, по которым выборка строит условия (``ConditionStructure``).
    Используется при анализе/построении условий поиска вместе с самой схемой
    (см. :class:`SearchScheme`).

    Attributes:
        attribute_id: Идентификатор атрибута, участвующего в условии.
        attribute_source_types: Источник значения атрибута (см. :class:`AttributeSourceType`).
    """

    attribute_id: int = Field(description="Идентификатор атрибута условия")
    attribute_source_types: AttributeSourceType | None = Field(
        default=None, description="Источник значения атрибута"
    )
