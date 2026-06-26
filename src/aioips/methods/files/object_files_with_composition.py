"""Метод получения дерева файлов объекта с учётом состава (ёлочка) IPS."""

from typing import Any

from ...core import APIManager
from ...schemas.files.object_files_tree import ObjectFilesTreeNodeDto


class ObjectFilesWithCompositionMixin(APIManager):
    """Реализует ``POST /core/api/files/objects/{objectId}/withComposition``.

    operationId ``Files_GetFileInfoForObjectWithComposition``.
    """

    async def object_files_with_composition(
        self: "ObjectFilesWithCompositionMixin",
        object_id: int,
        body: dict[str, Any] | None = None,
    ) -> ObjectFilesTreeNodeDto:
        """Возвращает дерево файлов объекта с рекурсивным разворачиванием состава.

        Применяют, чтобы получить файлы объекта ВМЕСТЕ с файлами входящих в его
        состав компонентов (сборка → детали) одним запросом, в виде дерева
        «ёлочка»: корневой узел — запрошенный объект, ``childNodes`` — узлы
        объектов состава (рекурсивно). В отличие от методов выборки таблиц
        (``get_files_table*``), которые плоски, здесь сохраняется иерархия состава.

        Это операция ЧТЕНИЯ. Несмотря на метод POST, данные не изменяются.

        Предусловие по id-пространству: ``object_id`` — ``ObjectID``
        (F_OBJECT_ID, общий для версий), а НЕ ``id`` версии.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``ObjectID`` / F_OBJECT_ID, int64),
                для которого строится дерево файлов (path ``objectId``).
            body: Необязательные параметры контекста
                (``FileInfoForObjectWithCompositionParamsDto``), задаваемые
                словарём с ключом ``contextRule`` (правило контекста версий:
                ``versionRuleObjectId``, ``editingContextId``,
                ``editingContextMode``). Структура вложенная, поэтому принимается
                как ``dict``. ``None`` — отправляется пустое тело ``{}`` (контекст
                по умолчанию).

        Returns:
            :class:`ObjectFilesTreeNodeDto` — корневой узел дерева: ``object_id``,
            ``caption``, ``file_info_collection`` (файлы объекта) и ``child_nodes``
            (узлы состава, рекурсивно). Пустой ``child_nodes`` — у объекта нет
            состава.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                tree = await ips.object_files_with_composition(102550)
                root_files = tree.file_info_collection
                child_ids = [n.object_id for n in tree.child_nodes]

        Notes:
            operationId ``Files_GetFileInfoForObjectWithComposition``. Элементы
            ``file_info_collection`` — ``BlobFileAttributeInfoDto`` (как dict).
            Связанные методы: :meth:`get_files_table_by_fields`,
            :meth:`file_attributes`. См. [[ips-object-model]].
        """
        data = await self._request(
            "post",
            f"/core/api/files/objects/{object_id}/withComposition",
            json=body if body is not None else {},
        )
        return ObjectFilesTreeNodeDto.model_validate(data if isinstance(data, dict) else {})
