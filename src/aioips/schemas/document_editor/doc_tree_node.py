"""Схема узла дерева документа редактора документов IPS.

References:
    ``GET /core/api/documentEditor/getBuffer`` — массив ``DocTreeNode``.
"""

from typing import Annotated, Any

from pydantic import Field

from ..base import EmptyListIfNone, IPSModel


class DocTreeNode(IPSModel):
    """Узел дерева структуры документа в буфере редактора документов IPS.

    Описывает один элемент иерархической структуры документа (страница, контейнер,
    таблица, ячейка, надпись и т.п.) вместе с его потомками. Узлы образуют рекурсивное
    дерево: каждый узел содержит описание самого элемента (``element``) и список
    дочерних узлов (``childs``) той же схемы.

    Когда применять: для чтения и обхода структуры документа, помещённого в буфер
    редактора (например, чтобы перечислить элементы документа или построить навигацию).
    Метод-источник — :meth:`doc_editor_buffer`.

    Послабление схемы (обосновано): поле ``element`` ссылается на крупную
    полиморфную структуру ``ElementsInfo`` (document/page/container/polyline/label/
    textBox/table), а ``childs`` рекурсивно ссылается на ту же схему ``DocTreeNode``.
    Чтобы не дублировать всю объёмную модель элементов и избежать жёсткой связки с
    нестабильными деталями, ``element`` типизирован как ``dict[str, Any]``, а ``childs``
    — как ``list[Any]`` (узлы того же вида). Это устойчиво к различиям версий API.

    Attributes:
        last_change_time_ticks: Метка времени последнего изменения узла (тики .NET).
        element: Описание самого элемента документа (полиморфная структура
            ``ElementsInfo``); сохранено как «сырой» словарь.
        childs: Дочерние узлы дерева (рекурсивно той же структуры ``DocTreeNode``).
        is_first_cell_in_parent_data_flow: Признак первой ячейки в потоке данных
            родителя.
        is_last_cell_in_parent_data_flow: Признак последней ячейки в потоке данных
            родителя.
    """

    last_change_time_ticks: int | None = Field(
        default=None, description="Время последнего изменения узла (тики .NET)"
    )
    element: dict[str, Any] = Field(
        default_factory=dict, description="Описание элемента документа (ElementsInfo)"
    )
    childs: Annotated[list[Any], EmptyListIfNone] = Field(
        default_factory=list, description="Дочерние узлы дерева (рекурсивно DocTreeNode)"
    )
    is_first_cell_in_parent_data_flow: bool | None = Field(
        default=None, description="Первая ячейка в потоке данных родителя"
    )
    is_last_cell_in_parent_data_flow: bool | None = Field(
        default=None, description="Последняя ячейка в потоке данных родителя"
    )
