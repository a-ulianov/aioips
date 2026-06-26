"""Методы раздела запросов состава/вхождения IPS Web API.

Раздел соответствует контроллеру ``/core/api/Relations/...`` (с ЗАГЛАВНОЙ ``R``)
и реализует запросы состава («из чего состоит»), вхождения («куда входит»),
справочник типов связей и выборку объектов узла классификатора. Это READ-раздел;
он НЕ совпадает с разделом ``relations`` (строчная ``r``), управляющим отдельными
записями связей и их жизненным циклом.
"""

from .classifier_objects import ClassifierObjectsMixin
from .consist_from import ConsistFromMixin
from .enters_in_version import EntersInVersionMixin
from .relation_queries_relation_types import RelationQueriesRelationTypesMixin


class RelationQueriesAPI(
    ConsistFromMixin,
    EntersInVersionMixin,
    RelationQueriesRelationTypesMixin,
    ClassifierObjectsMixin,
):
    """Объединяет методы раздела запросов состава/вхождения.

    References:
        Эндпоинты ``/core/api/Relations/*`` IPS Server Web API.
    """


__all__ = ["RelationQueriesAPI"]
