"""Схема настроек документов для типа объекта IPS.

References:
    ``GET /api/documents/{objectTypeId}/settings`` — ``DocumentSettingsContract``.
"""

from typing import Annotated

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class DocumentSettingsSubscriber(IPSModel):
    """Подписчик (получатель копий) документа в настройках типа документа.

    Описывает адресата рассылки документа данного типа и число положенных ему
    копий. Используется как элемент списка ``subscribers`` в
    :class:`DocumentSettings`.

    Attributes:
        subscriber_id: Числовой идентификатор подписчика.
        subscriber_name: Наименование подписчика (получателя копий).
        copies_count: Количество копий документа, положенных подписчику.
    """

    subscriber_id: int = Field(description="Идентификатор подписчика")
    subscriber_name: str | None = Field(default=None, description="Наименование подписчика")
    copies_count: int = Field(default=0, description="Количество копий для подписчика")


class DocumentSettings(IPSModel):
    """Настройки документов, заданные для конкретного типа объекта IPS.

    Описывает правила работы с документами выбранного типа объекта: расширения
    файлов документа, имя и код типа документа, признаки оформления (вывод имени
    документа в штамп, включение кода в обозначение), типы объектов-результатов
    вывода, список подписчиков-получателей копий и идентификаторы доступных
    прототипов файлов. Получается методом :meth:`document_settings` по
    идентификатору типа объекта; прототипы из ``file_prototype_ids``
    сопоставляются с :class:`DocumentPrototype` (см.
    :meth:`document_prototypes_common` / :meth:`document_prototypes_private`).

    Все поля необязательны: IPS возвращает объект настроек целиком, но отдельные
    значения могут быть пустыми/``null`` (списки нормализуются в пустые). Это
    устойчиво к типам объектов без полностью заполненных настроек документов.

    Attributes:
        document_file_extension: Основное расширение файла документа (например, ``pdf``).
        additional_document_file_extension: Дополнительное расширение файла документа.
        document_type_name: Наименование типа документа.
        document_type_code: Код типа документа.
        is_show_document_name_in_stamp: Выводить имя документа в штамп.
        is_document_type_include_code_in_designation: Включать код типа в обозначение.
        output_object_type_ids: Идентификаторы типов объектов-результатов вывода.
        subscribers: Подписчики-получатели копий документа.
        file_prototype_ids: Идентификаторы прототипов файлов, доступных для типа.
    """

    document_file_extension: str | None = Field(
        default=None, description="Основное расширение файла документа"
    )
    additional_document_file_extension: str | None = Field(
        default=None, description="Дополнительное расширение файла документа"
    )
    document_type_name: str | None = Field(default=None, description="Наименование типа документа")
    document_type_code: str | None = Field(default=None, description="Код типа документа")
    is_show_document_name_in_stamp: bool = Field(
        default=False, description="Выводить имя документа в штамп"
    )
    is_document_type_include_code_in_designation: bool = Field(
        default=False, description="Включать код типа документа в обозначение"
    )
    output_object_type_ids: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list, description="Идентификаторы типов объектов-результатов вывода"
    )
    subscribers: Annotated[list[DocumentSettingsSubscriber], EmptyListIfNone] = Field(
        default_factory=list, description="Подписчики-получатели копий документа"
    )
    file_prototype_ids: Annotated[list[int], EmptyListIfNone] = Field(
        default_factory=list, description="Идентификаторы прототипов файлов для типа"
    )
