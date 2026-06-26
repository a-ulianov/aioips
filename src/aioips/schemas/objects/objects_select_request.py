"""Схемы legacy search-контроллера ``Objects`` (выборка объектов по фильтру-запросу).

Этот модуль описывает запрос и ответы АЛЬТЕРНАТИВНЫХ search-эндпоинтов с заглавной
буквы пути: ``POST /core/api/Objects/ObjectsSelect`` и
``POST /core/api/Objects/ObjectsSelectById``. Они НЕ совпадают с lowercase-поиском
``objects/select`` (см. :mod:`aioips.schemas.objects.select`): тело запроса здесь —
:class:`ObjectSelectRequest` (список id объектов + перечень обязательных системных
атрибутов), а результат — «сырые» наборы значений атрибутов на объект
(:class:`ObjectSelectDTO` / :class:`ObjectSelectByIdDTO`).

Пространство идентификаторов (критично, см. [[ips-object-model]]):
    ``objectId`` в запросе и ответах — идентификатор ОБЪЕКТА (F_OBJECT_ID), общий для
    всех версий, а НЕ идентификатор версии (F_ID). Системный атрибут ``f_OBJECT_ID``
    повторяет id объекта, ``f_ID`` — id версии, ``f_VERSION_ID`` — номер версии.

References:
    ``POST /core/api/Objects/ObjectsSelect`` — ``Objects_ObjectsSelect``.
    ``POST /core/api/Objects/ObjectsSelectById`` — ``Objects_ObjectsSelectById``.
"""

from typing import Annotated, Any

from pydantic import BeforeValidator, Field

from ..base import EmptyListIfNone, IPSModel


def _coerce_none_to_dict(value: Any) -> Any:
    """Преобразует ``None`` в пустой словарь (IPS отдаёт ``null`` вместо ``{}``)."""
    return {} if value is None else value


_EmptyDictIfNone = BeforeValidator(_coerce_none_to_dict)


class ObjectSelectRequest(IPSModel):
    """Запрос выборки атрибутов у заданных объектов (тело ``Objects/ObjectsSelect*``).

    Адресует выборку напрямую списком id объектов (``object_ids``) и указывает, какие
    системные атрибуты вернуть (``attributes`` — имена из набора «обязательных»
    системных атрибутов IPS, напр. ``f_OBJECT_NAME``, ``f_OWNER_CAPTION``,
    ``f_VERSIONS_COUNT``). Применяется как АЛЬТЕРНАТИВА lowercase-поиску
    ``objects/select`` (там фильтр по условиям-атрибутам через ``SelectCondition``):
    здесь объекты уже известны по id, а нужны их системные поля одним запросом.

    Предусловие по id-пространству: ``object_ids`` — идентификаторы ОБЪЕКТОВ
    (F_OBJECT_ID), не версий.

    Важно (проверено на проде): значения ``attributes`` берутся ТОЛЬКО из перечня
    ``ObligatoryObjectAttributes`` (69 значений: ``f_OBJECT_NAME``, ``f_OWNER_CAPTION``,
    ``f_RELATIONS_COUNT``, ``f_VERSIONS_COUNT``, ``f_FILENAME`` и т.д.). Произвольные
    имена (напр. ``"caption"``) сервер отвергает с ошибкой 400.

    Attributes:
        object_ids: Список id ОБЪЕКТОВ, для которых вернуть атрибуты. Пустой список —
            без объектов (по умолчанию).
        attributes: Имена обязательных системных атрибутов для выборки — строки из
            перечня ``ObligatoryObjectAttributes`` swagger (напр. ``"f_OBJECT_NAME"``,
            ``"f_OWNER_CAPTION"``). Пустой список — атрибуты на усмотрение сервера.
    """

    object_ids: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list, description="Список id ОБЪЕКТОВ (F_OBJECT_ID), не версий"
    )
    attributes: Annotated[list[str], EmptyListIfNone] = Field(
        default_factory=list,
        description="Имена системных атрибутов для выборки (ObligatoryObjectAttributes)",
    )


class ObjectSelectDTO(IPSModel):
    """Результат ``Objects/ObjectsSelect`` — атрибуты объекта с ключами-именами.

    Один элемент массива ответа ``POST /core/api/Objects/ObjectsSelect``. Значения
    атрибутов сгруппированы в словарь ``object_attributes``, где КЛЮЧ — имя системного
    атрибута (``f_OBJECT_NAME``, ``f_OWNER_CAPTION``, ``f_VERSIONS_COUNT`` и т.п.), а
    значение — его содержимое. Отличие от :class:`ObjectSelectByIdDTO`: там ключи —
    числовые
    id типов атрибутов, а здесь — символьные имена.

    Пространство идентификаторов: ``object_id`` — id ОБЪЕКТА (F_OBJECT_ID), общий для
    версий. Среди ключей ``object_attributes`` ``f_OBJECT_ID`` дублирует id объекта,
    ``f_ID`` — id ВЕРСИИ, ``f_VERSION_ID`` — номер версии. См. [[ips-object-model]].

    Attributes:
        object_id: Идентификатор ОБЪЕКТА (F_OBJECT_ID).
        object_attributes: Значения атрибутов как ``{имя_атрибута: значение}`` (может
            быть пустым; IPS способен отдать ``null`` → пустой словарь).
    """

    object_id: int = Field(default=0, description="Идентификатор ОБЪЕКТА (F_OBJECT_ID)")
    object_attributes: Annotated[dict[str, Any], _EmptyDictIfNone] = Field(
        default_factory=dict,
        description="Атрибуты как {имя_атрибута: значение}",
    )


class ObjectSelectByIdDTO(IPSModel):
    """Результат ``Objects/ObjectsSelectById`` — атрибуты объекта с ключами-id.

    Один элемент массива ответа ``POST /core/api/Objects/ObjectsSelectById``. Как и
    :class:`ObjectSelectDTO`, несёт id объекта и словарь значений атрибутов, но КЛЮЧ
    словаря ``object_attributes`` — это числовой id ТИПА атрибута (в JSON приходит
    строкой), а не его символьное имя. Применяйте, когда удобнее адресовать значения
    по id атрибута, а не по имени.

    Пространство идентификаторов: ``object_id`` — id ОБЪЕКТА (F_OBJECT_ID), не версии.
    См. [[ips-object-model]].

    Attributes:
        object_id: Идентификатор ОБЪЕКТА (F_OBJECT_ID).
        object_attributes: Значения атрибутов как ``{id_атрибута: значение}`` (ключи —
            строки; может быть пустым).
    """

    object_id: int = Field(default=0, description="Идентификатор ОБЪЕКТА (F_OBJECT_ID)")
    object_attributes: Annotated[dict[str, Any], _EmptyDictIfNone] = Field(
        default_factory=dict,
        description="Атрибуты как {id_атрибута(str): значение}",
    )
