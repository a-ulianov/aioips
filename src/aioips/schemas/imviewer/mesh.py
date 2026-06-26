"""Схема триангуляционной сетки (mesh) объекта для 3D-просмотрщика IPS.

References:
    ``GET /core/api/imviewer/mesh/{objectId}/{blobId}`` — ``MeshDto``.
"""

from typing import Any

from pydantic import Field

from ..base import IPSModel


class Mesh(IPSModel):
    """Триангуляционная сетка детали (mesh) для 3D-просмотрщика ImViewer.

    Описывает геометрию одной детали (part), извлечённую из файлового blob модели:
    метаданные объекта, информацию о текущей конфигурации и набор геометрических тел
    (триангуляция). Возвращается методом :meth:`imviewer_mesh`. Для сборок (asm)
    структура иная — см. :class:`Assembly`; тип объекта в blob заранее определяется
    через :meth:`imviewer_object_info` (:class:`ImViewerObjectInfo`).

    Поля ``metadata``, ``config_info`` и ``bodies`` намеренно оставлены непрозрачными
    (``dict[str, Any]`` / ``list[Any]``): это крупные вложенные геометрические структуры
    просмотрщика (координаты вершин, нормали, индексы треугольников, граф конфигураций),
    их форма зависит от CAD-источника и версии ImViewer. Жёсткая типизация была бы
    хрупкой и не несла бы практической ценности для потребителя API — данные
    предназначены для прямой передачи в рендер 3D-вьювера, а не для разбора по полям.

    Attributes:
        metadata: Метаданные объекта (непрозрачная структура просмотрщика).
        config_info: Информация о текущей конфигурации модели (непрозрачная структура).
        bodies: Геометрические тела триангуляции (непрозрачные структуры просмотрщика).
    """

    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Метаданные объекта (непрозрачная структура)"
    )
    config_info: dict[str, Any] = Field(
        default_factory=dict, description="Информация о текущей конфигурации модели"
    )
    bodies: list[Any] = Field(default_factory=list, description="Геометрические тела триангуляции")
