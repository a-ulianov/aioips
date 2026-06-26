"""Схемы дерева сборочного состава для 3D-просмотрщика (ImViewer) IPS.

References:
    ``POST /core/api/imviewer/assemblyComposition`` — ``SourceAssemblyCompositionTreeNodeDto``
    (тело запроса) и ``ImViewerAssemblyCompositionTreeNodeDto`` (ответ).
"""

from typing import Annotated

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class SourceAssemblyCompositionTreeNode(IPSModel):
    """Узел дерева исходного сборочного состава (тело запроса).

    Описывает один объект сборочного дерева в терминах ПЛМ-модели IPS (исходные данные,
    из которых сервер вычисляет соответствие imv-файлам). Тип запроса —
    :meth:`imviewer_assembly_composition`: клиент передаёт корень дерева сборки, сервер
    разрешает каждый узел в imv-файлы для 3D-просмотра. Структура рекурсивна: узел может
    содержать вложенные узлы-потомки (компоненты следующего уровня сборки).

    POST-глагол, но операция — чтение/вычисление без побочных эффектов: сервер ничего не
    меняет, лишь сопоставляет переданное дерево с состоянием imv-данных.

    Id-пространство (важно): ``object_id`` — идентификатор ОБЪЕКТА (``F_OBJECT_ID``,
    int64), а не версии. Дерево строится по объектам сборки.

    Attributes:
        object_id: Идентификатор ОБЪЕКТА узла сборки (``objectId`` / ``F_OBJECT_ID``,
            int64). Обязателен на стороне API (дефолт ``0`` — заглушка, задайте явно).
        caption: Наименование объекта (``caption``). Не должно быть пустым.
        child_nodes: Потомки узла (``childNodes``) — список вложенных узлов того же типа
            (рекурсия). ``null`` от сервера нормализуется в пустой список.
    """

    object_id: int = Field(default=0, description="Идентификатор объекта узла (objectId)")
    caption: str = Field(default="", description="Наименование объекта")
    child_nodes: Annotated[list["SourceAssemblyCompositionTreeNode"], EmptyListIfNone] = Field(
        default_factory=list, description="Потомки узла (рекурсивно)"
    )


class ImViewerAssemblyCompositionTreeNode(IPSModel):
    """Узел дерева сборочного состава для 3D-просмотрщика (ответ).

    Результат разрешения исходного дерева сборки в imv-данные: для каждого исходного
    объекта указывает статус и привязку к imv-файлу (объект/blob/имя файла). Возвращается
    методом :meth:`imviewer_assembly_composition`. Структура рекурсивна: ``child_nodes``
    повторяет форму родителя (компоненты/подузлы сборки).

    Id-пространства (важно, разные): ``source_object_id`` — идентификатор ИСХОДНОГО
    объекта ПЛМ (``F_OBJECT_ID``, int64), по которому строилось дерево; ``object_id`` —
    идентификатор imv-объекта (int64, может быть ``None``); ``blob_id`` — идентификатор
    imv-файла/blob (int64, может быть ``None``). Их не следует путать между собой.

    Attributes:
        source_object_id: Идентификатор исходного объекта (``sourceObjectId``, int64), для
            которого подбирался imv-файл.
        source_object_caption: Наименование исходного объекта (``sourceObjectCaption``).
        object_status: Статус imv-объекта (``objectStatus``). Значения
            ``ImViewerObjectContentStatusDto``: ``"notSet"`` (не задан), ``"actual"``
            (актуален), ``"outdated"`` (устарел). Может быть ``None``.
        object_id: Идентификатор imv-объекта (``objectId``, int64) или ``None``, если imv
            не сопоставлен.
        blob_id: Идентификатор imv-файла/blob (``blobId``, int64) или ``None``.
        file_name: Имя imv-файла (``fileName``) или ``None``.
        child_nodes: Потомки узла (``childNodes``) — список вложенных узлов того же типа
            (рекурсия). ``null`` от сервера нормализуется в пустой список.
    """

    source_object_id: int = Field(
        default=0, description="Идентификатор исходного объекта (sourceObjectId)"
    )
    source_object_caption: str = Field(default="", description="Наименование исходного объекта")
    object_status: str | None = Field(
        default=None, description="Статус imv-объекта: 'notSet' | 'actual' | 'outdated'"
    )
    object_id: int | None = Field(default=None, description="Идентификатор imv-объекта")
    blob_id: int | None = Field(default=None, description="Идентификатор imv-файла/blob")
    file_name: str | None = Field(default=None, description="Имя imv-файла")
    child_nodes: Annotated[list["ImViewerAssemblyCompositionTreeNode"], EmptyListIfNone] = Field(
        default_factory=list, description="Потомки узла (рекурсивно)"
    )


SourceAssemblyCompositionTreeNode.model_rebuild()
ImViewerAssemblyCompositionTreeNode.model_rebuild()
