"""Схема сборки (assembly) объекта для 3D-просмотрщика IPS.

References:
    ``GET /core/api/imviewer/assembly/{objectId}/{blobId}`` — ``AssemblyDto``.
"""

from typing import Any

from pydantic import Field

from ..base import IPSModel


class Assembly(IPSModel):
    """Сборка (assembly) для 3D-просмотрщика ImViewer.

    Описывает сборочную единицу (asm), извлечённую из файлового blob модели:
    метаданные объекта и информацию о текущей конфигурации сборки. Возвращается методом
    :meth:`imviewer_assembly`. Для отдельной детали (part) структура иная — см.
    :class:`Mesh`; тип объекта в blob заранее определяется через
    :meth:`imviewer_object_info` (:class:`ImViewerObjectInfo`).

    Поля ``metadata`` и ``config_info`` намеренно оставлены непрозрачными
    (``dict[str, Any]``): это крупные вложенные структуры просмотрщика (дерево
    компонентов сборки, граф конфигураций, матрицы размещения), форма которых зависит
    от CAD-источника и версии ImViewer. Жёсткая типизация была бы хрупкой и не несла бы
    практической ценности — данные предназначены для прямой передачи в 3D-вьювер.

    Attributes:
        metadata: Метаданные объекта (непрозрачная структура просмотрщика).
        config_info: Информация о текущей конфигурации сборки (непрозрачная структура).
    """

    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Метаданные объекта (непрозрачная структура)"
    )
    config_info: dict[str, Any] = Field(
        default_factory=dict, description="Информация о текущей конфигурации сборки"
    )
