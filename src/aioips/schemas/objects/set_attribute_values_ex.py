"""Схема тела расширенной записи значений атрибутов объекта.

DTO запроса для ``POST /core/api/objects/{objectId}/attributeValuesEx``
(``ObjectAttributes_SetAttributeValuesEx``). Расширенный вариант записи: помимо
самих значений и флагов поведения, позволяет задать набор режимов извлечения
``modes`` (``GetAttributeValuesModes``), управляющих формой возвращаемых данных.

References:
    ``POST /core/api/objects/{objectId}/attributeValuesEx`` —
    ``ObjectAttributes_SetAttributeValuesEx``.
"""

from typing import Annotated, Any

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel
from .attribute import AttributeValues


class SetAttributeValuesExBody(IPSModel):
    """Параметры расширенной записи значений атрибутов (тело ``..._set_attribute_values_ex``).

    Несёт список значений атрибутов (:class:`AttributeValues`) и флаги поведения записи
    (как в обычном ``SetAttributeValues``), а также необязательный список режимов
    извлечения ``modes`` (``GetAttributeValuesModes``), влияющих на форму ответа.
    Применяйте, когда нужно тонко управлять составом возвращаемых данных; иначе
    достаточно :meth:`object_set_attribute_values`.

    Attributes:
        attribute_values: Значения атрибутов для записи (см. :class:`AttributeValues`).
            ``None`` — поле не передаётся.
        delete_not_existing: Если ``True``, атрибуты, не указанные в наборе, удаляются
            (полная замена). ``None`` — серверное значение по умолчанию.
        dont_delete_blobs: Если ``True``, не удалять значения blob-атрибутов с диска.
            ``None`` — серверное значение по умолчанию.
        return_delta: Если ``True``, вернуть только изменившиеся значения (дельту);
            иначе сервер вернёт ``null``. ``None`` — серверное значение по умолчанию.
        modes: Режимы извлечения значений (``GetAttributeValuesModes``) как «сырые»
            словари серверного enum-DTO; ``None`` — поле не передаётся.
    """

    attribute_values: Annotated[list[AttributeValues] | None, EmptyListIfNone] = Field(
        default=None,
        alias="attributeValues",
        description="Значения атрибутов для записи (AttributeValues) или None",
    )
    delete_not_existing: bool | None = Field(
        default=None,
        alias="deleteNotExistingAttribute",
        description="True — удалить атрибуты вне набора (полная замена)",
    )
    dont_delete_blobs: bool | None = Field(
        default=None,
        alias="dontDeleteBlobs",
        description="True — не удалять blob-значения с диска при перезаписи",
    )
    return_delta: bool | None = Field(
        default=None,
        alias="returnDelta",
        description="True — вернуть только изменившиеся значения (дельту)",
    )
    modes: list[dict[str, Any]] | None = Field(
        default=None,
        description="Режимы извлечения значений (GetAttributeValuesModes) как словари",
    )
