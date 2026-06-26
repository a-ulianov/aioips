"""Схема информации об объекте, создаваемом на основе данных IMBASE.

References:
    ``GET /core/api/imbase/object/{baseId}/createInfo`` — ``ImBaseObjectCreateInfoDto``
    (без result-обёртки).
"""

from typing import Annotated

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class ImBaseObjectCreateInfo(IPSModel):
    """Информация об объекте, создаваемом на основе элемента (записи) IMBASE.

    Подсказывает клиенту, как поступить при создании объекта по элементу IMBASE:
    создавать ли новый объект, какого типа, и какие объекты уже были созданы на
    основе этого же элемента ранее (чтобы предложить переиспользование вместо
    дублирования).

    Когда применять: перед созданием объекта из записи IMBASE — чтобы определить тип
    создаваемого объекта и проверить наличие уже существующих объектов по тому же
    элементу. ``base_id`` — идентификатор элемента IMBASE, ``object_type_id`` —
    id-пространство ТИПОВ объектов, ``existing_objects`` — id-пространство объектов
    (``ObjectID``).

    Attributes:
        should_create_new_object: Нужно ли создавать новый объект (``True``) или можно
            переиспользовать существующий.
        object_type_id: Идентификатор типа объекта, который следует создать
            (``ObjectTypeID``).
        existing_objects: Идентификаторы объектов, уже созданных на основе этого
            элемента IMBASE (``ObjectID``); пустой список — таких объектов нет.
    """

    should_create_new_object: bool = Field(description="Нужно ли создавать новый объект")
    object_type_id: int = Field(description="Идентификатор типа создаваемого объекта")
    existing_objects: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list,
        description="Id объектов, уже созданных на основе этого элемента IMBASE",
    )
