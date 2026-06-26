"""Методы раздела типов объектов (контроллер ``objectTypes``) IPS Web API.

Раздел отличается от ``metadata``: контроллер ``/core/api/objectTypes/*`` возвращает
ЭКЗЕМПЛЯРЫ объектов типа (id/перечень/сводку) и определение типа ``ObjectTypeDto``,
тогда как ``metadata`` описывает метамодель (``ImsObjectTypeDto``).
"""

from .object_type_all_child_guids import ObjectTypeAllChildGuidsMixin
from .object_type_composition import ObjectTypeCompositionMixin
from .object_type_definition import ObjectTypeDefinitionMixin
from .object_type_definition_by_guid import ObjectTypeDefinitionByGuidMixin
from .object_type_definition_by_name import ObjectTypeDefinitionByNameMixin
from .object_type_icons import ObjectTypeIconsMixin
from .object_type_object_ids import ObjectTypeObjectIdsMixin
from .object_type_objects import ObjectTypeObjectsMixin
from .object_type_objects_info import ObjectTypeObjectsInfoMixin
from .object_type_quick_info import ObjectTypeQuickInfoMixin
from .object_type_quick_info_by_guid import ObjectTypeQuickInfoByGuidMixin
from .object_types_tree import ObjectTypesTreeMixin


class ObjectTypesAPI(
    ObjectTypeObjectIdsMixin,
    ObjectTypeObjectsMixin,
    ObjectTypeObjectsInfoMixin,
    ObjectTypeDefinitionMixin,
    ObjectTypeDefinitionByGuidMixin,
    ObjectTypeDefinitionByNameMixin,
    ObjectTypeQuickInfoMixin,
    ObjectTypeQuickInfoByGuidMixin,
    ObjectTypeAllChildGuidsMixin,
    ObjectTypeIconsMixin,
    ObjectTypesTreeMixin,
    ObjectTypeCompositionMixin,
):
    """Объединяет методы раздела типов объектов.

    References:
        Эндпоинты ``/core/api/objectTypes/*`` IPS Server Web API.
    """


__all__ = ["ObjectTypesAPI"]
