"""Схема краткой информации об объекте 3D-просмотрщика IPS.

References:
    ``GET /core/api/imviewer/objectInfo/{objectId}/{blobId}`` — ``ImViewerObjectInfoDto``.
"""

from pydantic import Field

from ..base import IPSModel


class ImViewerObjectInfo(IPSModel):
    """Краткая информация о 3D-объекте в файловом blob (деталь или сборка).

    Лёгкий «заголовок» геометрии: позволяет до загрузки тяжёлых данных определить тип
    объекта в blob и выбрать корректный метод чтения геометрии. Возвращается методом
    :meth:`imviewer_object_info`. По значению ``type`` выбирается дальнейший вызов:
    ``"part"`` → :meth:`imviewer_mesh` (:class:`Mesh`); ``"asm"`` →
    :meth:`imviewer_assembly` (:class:`Assembly`); ``"unknown"`` — тип не распознан.

    Attributes:
        type: Тип объекта-геометрии в blob. Возможные значения (``ImViewerObjectTypeDto``):
            ``"unknown"`` (не распознан), ``"part"`` (деталь), ``"asm"`` (сборка). Может
            быть ``None``, если сервер не вернул тип.
    """

    type: str | None = Field(
        default=None,
        description="Тип объекта-геометрии: 'unknown' | 'part' | 'asm'",
    )
