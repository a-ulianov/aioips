"""Перечисления метаданных IPS.

Значения соответствуют строковым enum'ам ``ObjectVersionModes``,
``InheritModes`` и ``ObjectsClassifyType`` из OpenAPI-описания IPS Web API.
Классы наследуют ``str``, поэтому сравниваются и сериализуются как строки.
"""

from enum import StrEnum


class ObjectVersionMode(StrEnum):
    """Режим версионирования типа объекта (``ObjectVersionModes``).

    Свойство типа объекта (метаданные), определяющее, поддерживает ли тип
    версии. Влияет на доступность операций жизненного цикла (checkout/версии).

    Семантика членов:
        ABSTRACT: ``abstract`` — абстрактный тип, экземпляры не создаются.
        SINGLE_VERSION: ``singleVersion`` — у объекта только одна версия.
        MULTI_VERSION: ``multiVersion`` — объект поддерживает несколько версий.
    """

    ABSTRACT = "abstract"
    SINGLE_VERSION = "singleVersion"
    MULTI_VERSION = "multiVersion"


class InheritMode(StrEnum):
    """Режим наследования настройки типа объекта (``InheritModes``).

    Определяет, как настройка (например, схема жизненного цикла) распространяется
    по иерархии типов: задаётся локально, публикуется потомкам или наследуется
    от родителя.

    Семантика членов:
        PRIVATE: ``private`` — настройка только для данного типа.
        PUBLIC: ``public`` — настройка задаётся здесь и доступна потомкам.
        INHERITED: ``inherited`` — настройка унаследована от родительского типа.
    """

    PRIVATE = "private"
    PUBLIC = "public"
    INHERITED = "inherited"


class ObjectsClassifyType(StrEnum):
    """Тип обязательности классификации объектов (``ObjectsClassifyType``).

    Указывает, требуется ли относить объекты типа к классификатору и насколько
    это обязательно.

    Семантика членов:
        NONE: ``none`` — классификация не применяется.
        SELECTIVE: ``selective`` — классификация выборочная (по выбору).
        OBLIGATORY: ``obligatory`` — классификация обязательна.
    """

    NONE = "none"
    SELECTIVE = "selective"
    OBLIGATORY = "obligatory"
