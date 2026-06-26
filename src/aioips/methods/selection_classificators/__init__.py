"""Методы раздела классификаторов выбора IPS Web API."""

from .classificator_attributes import ClassificatorAttributesMixin
from .classifiers_for_object_type import ClassifiersForObjectTypeMixin
from .classify_object import ClassifyObjectMixin
from .exclude_object_from_classificators import ExcludeObjectFromClassificatorsMixin
from .exclude_objects_from_classificator import ExcludeObjectsFromClassificatorMixin
from .include_object_in_classificators import IncludeObjectInClassificatorsMixin
from .include_objects_in_classificator import IncludeObjectsInClassificatorMixin
from .is_multi_select_classifier import IsMultiSelectClassifierMixin


class SelectionClassificatorsAPI(
    ClassifiersForObjectTypeMixin,
    ClassificatorAttributesMixin,
    IsMultiSelectClassifierMixin,
    IncludeObjectInClassificatorsMixin,
    IncludeObjectsInClassificatorMixin,
    ExcludeObjectFromClassificatorsMixin,
    ExcludeObjectsFromClassificatorMixin,
    ClassifyObjectMixin,
):
    """Объединяет методы раздела классификаторов выбора.

    Классификатор выбора ограничивает выбор значений атрибута объекта заранее заданным
    классифицированным набором.

    References:
        Эндпоинты ``/core/api/selectionClassificators/*`` IPS Server Web API.
    """


__all__ = ["SelectionClassificatorsAPI"]
