"""Схема информации о файле-прототипе атрибута ``ftFile``.

References:
    ``GET /core/api/files/getFilesProptotypes/{objectId}`` — массив
    ``PrototypeInfoDto`` (operationId ``Files_GetFilesPrototypes``).
"""

from pydantic import Field

from ..base import IPSModel


class PrototypeInfo(IPSModel):
    """Описание файла-прототипа, привязанного к файловому атрибуту объекта.

    Прототип задаёт «болванку» (шаблон) файла, который может быть создан или
    подставлен в файловый атрибут (``ftFile``) объекта. Используется при
    подготовке файлового атрибута к заполнению: список прототипов показывает,
    какие шаблоны доступны для данного объекта и к какому атрибуту они
    относятся.

    Обязательны только идентификатор прототипа и его имя; ``attribute_id``
    может отсутствовать, если прототип не привязан к конкретному атрибуту.

    Attributes:
        prototype_id: Идентификатор прототипа (DTO ``prototypeId``).
        name: Наименование прототипа (DTO ``name``).
        attribute_id: Идентификатор файлового атрибута, к которому относится
            прототип (DTO ``attributeId``); ``None``, если не задан.
    """

    prototype_id: int = Field(description="Идентификатор прототипа")
    name: str = Field(description="Наименование прототипа")
    attribute_id: int | None = Field(
        default=None, description="Идентификатор файлового атрибута прототипа"
    )
