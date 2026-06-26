"""Метод разрешения сборочного состава в imv-данные (POST, чтение/вычисление)."""

from typing import Any

from ...core import APIManager
from ...schemas.imviewer.assembly_composition import (
    ImViewerAssemblyCompositionTreeNode,
    SourceAssemblyCompositionTreeNode,
)


class ImViewerAssemblyCompositionMixin(APIManager):
    """Метод ``POST /core/api/imviewer/assemblyComposition``.

    operationId ``ImViewer_GetAssemblyComposition``.
    """

    async def imviewer_assembly_composition(
        self: "ImViewerAssemblyCompositionMixin",
        node: SourceAssemblyCompositionTreeNode,
    ) -> ImViewerAssemblyCompositionTreeNode:
        """Разрешает дерево сборочного состава в imv-данные для 3D-просмотрщика.

        Принимает дерево исходных объектов сборки (корневой узел с рекурсивными
        потомками) и возвращает соответствующее дерево, где каждый узел дополнен
        привязкой к imv-файлам (объект/blob/имя файла) и статусом актуальности. Это
        вычисление соответствия «исходный объект ПЛМ → imv-файлы», нужное перед загрузкой
        геометрии в просмотрщик ImViewer.

        Несмотря на POST-глагол, операция — ЧТЕНИЕ/вычисление без побочных эффектов:
        сервер ничего не сохраняет, лишь сопоставляет переданное дерево с состоянием
        imv-данных. Тело передаётся POST'ом из-за рекурсивной структуры (дерево), которую
        неудобно кодировать в query.

        Id-пространства (важно, разные): во входном дереве ``object_id`` — идентификатор
        ОБЪЕКТА ПЛМ (``F_OBJECT_ID``). В ответе ``source_object_id`` — тот же исходный
        объект, тогда как ``object_id``/``blob_id`` — идентификаторы imv-объекта и
        imv-файла соответственно (могут быть ``None``, если imv ещё не сопоставлен).

        Args:
            node: Корневой узел исходного дерева сборки
                (:class:`SourceAssemblyCompositionTreeNode`) с полями ``object_id``,
                ``caption`` и рекурсивным списком ``child_nodes``. Сериализуется как JSON
                с camelCase-алиасами; ``None``-поля исключаются.

        Returns:
            Корневой узел разрешённого дерева
            (:class:`ImViewerAssemblyCompositionTreeNode`) со статусами и привязкой к
            imv-файлам; потомки — в рекурсивном ``child_nodes``. Если сервер вернул не
            объект, возвращается узел со значениями по умолчанию.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                root = SourceAssemblyCompositionTreeNode(
                    object_id=102550,
                    caption="Сборка 550",
                    child_nodes=[
                        SourceAssemblyCompositionTreeNode(
                            object_id=102551, caption="Ребро"
                        )
                    ],
                )
                tree = await ips.imviewer_assembly_composition(root)
                first = tree.child_nodes[0]  # blob_id / file_name для загрузки геометрии

        Notes:
            ``operationId``: ``ImViewer_GetAssemblyComposition``; путь
            ``POST /core/api/imviewer/assemblyComposition``. См. также
            :meth:`imviewer_object_info`, :meth:`imviewer_assembly`, :meth:`imviewer_mesh`.
        """
        body = node.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request("post", "/core/api/imviewer/assemblyComposition", json=body)
        payload: dict[str, Any] = data if isinstance(data, dict) else {}
        return ImViewerAssemblyCompositionTreeNode.model_validate(payload)
