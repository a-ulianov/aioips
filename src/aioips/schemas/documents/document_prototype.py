"""Схема прототипа документа IPS.

References:
    ``GET /api/documents/prototypes/common`` и
    ``GET /api/documents/prototypes/private`` — массивы
    ``DocumentPrototypeOutContract``.
"""

from pydantic import Field

from ..base import IPSModel


class DocumentPrototype(IPSModel):
    """Прототип (шаблон-заготовка) документа в настройках типов документов IPS.

    Прототип задаёт файл-образец, на основе которого создаётся новый документ
    выбранного типа: имя шаблона и имя/паттерн файла-заготовки. Прототипы бывают
    общими (доступны всем типам, см. :meth:`document_prototypes_common`) и
    приватными (привязаны к конкретным типам, см.
    :meth:`document_prototypes_private`). Идентификаторы прототипов используются
    в настройках типа документа (поле ``file_prototype_ids`` схемы
    :class:`DocumentSettings`).

    Обязателен только идентификатор прототипа; остальные поля необязательны и
    могут отсутствовать (``null``), что устойчиво к различиям между прототипами и
    версиями API.

    Attributes:
        prototype_id: Числовой идентификатор прототипа документа.
        prototype_name: Отображаемое наименование прототипа.
        prototype_file_pattern_name: Паттерн имени файла-заготовки (шаблон имени).
        prototype_file_name: Имя файла-заготовки прототипа.
    """

    prototype_id: int = Field(description="Идентификатор прототипа документа")
    prototype_name: str | None = Field(default=None, description="Наименование прототипа документа")
    prototype_file_pattern_name: str | None = Field(
        default=None, description="Паттерн имени файла-заготовки прототипа"
    )
    prototype_file_name: str | None = Field(
        default=None, description="Имя файла-заготовки прототипа"
    )
