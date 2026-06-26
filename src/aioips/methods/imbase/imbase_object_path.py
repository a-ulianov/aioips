"""Метод получения пути к объекту справочной системы IMBASE по id объекта."""

from ...core import APIManager
from ...schemas.imbase import ImBaseObjectPath


class ImBaseObjectPathMixin(APIManager):
    """Реализует ``GET /core/api/imbase/object/{objectId}/path``."""

    async def imbase_object_path(
        self: "ImBaseObjectPathMixin",
        object_id: int,
    ) -> ImBaseObjectPath | None:
        """Возвращает путь к объекту IMBASE в иерархии каталогов справочной системы.

        Отдаёт цепочку узлов дерева IMBASE от корневого каталога верхнего уровня до
        указанного объекта (включительно). Применяется для навигации и построения
        «хлебных крошек» в справочной системе.

        Когда применять: чтобы показать местоположение записи/папки IMBASE в дереве.
        Для пути по id КЛЮЧА используйте :meth:`imbase_object_path_by_key`, для
        связанного объекта — :meth:`imbase_linked_object_path`. Ответ обёрнут в
        ``...NullableResultDto`` и разворачивается здесь.

        Args:
            object_id: Идентификатор объекта IMBASE (id-пространство объектов IMBASE).

        Returns:
            Путь по схеме :class:`ImBaseObjectPath` либо ``None``, если объект не
            найден (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                path = await ips.imbase_object_path(123456)
                if path is not None:
                    print(path.top_parent_object_id, path.path)

        Notes:
            operationId ``ImBase_GetPathToImBaseObject``; путь
            ``GET /core/api/imbase/object/{objectId}/path``.
            Ответ — ``ImBaseObjectPathDtoNullableResultDto``. См. объектной модели IPS.
        """
        data = await self._request("get", f"/core/api/imbase/object/{object_id}/path")
        entity = data.get("entity") if isinstance(data, dict) else None
        return ImBaseObjectPath.model_validate(entity) if entity is not None else None
