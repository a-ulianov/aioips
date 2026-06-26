"""Перечисления справочной системы IMBASE IPS Web API."""

from enum import StrEnum


class SearchesAccuracy(StrEnum):
    """Точность индексного поиска IMBASE (``SearchesAccuracy``).

    Используется в :meth:`~aioips.IPSClient.imbase_find_by_index`
    (поле ``search_accuracy`` тела ``ImBaseIndexSearchParams``).

    Attributes:
        START: Совпадение с начала строки (``start``).
        CONTAIN: Вхождение подстроки (``contain``).
        END: Совпадение с конца строки (``end``).
        EXACT: Точное совпадение (``exact``).
        TEMPLATE: По шаблону (``template``).
    """

    START = "start"
    CONTAIN = "contain"
    END = "end"
    EXACT = "exact"
    TEMPLATE = "template"
