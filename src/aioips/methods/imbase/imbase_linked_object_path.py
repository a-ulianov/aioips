"""Метод получения пути к связанному объекту справочной системы IMBASE."""

from ...core import APIManager
from ...schemas.imbase import ImBaseObjectPath


class ImBaseLinkedObjectPathMixin(APIManager):
    """Реализует ``GET /core/api/imbase/linkedObject/{objectId}/path``."""

    async def imbase_linked_object_path(
        self: "ImBaseLinkedObjectPathMixin",
        object_id: int,
    ) -> ImBaseObjectPath | None:
        """Возвращает путь к СВЯЗАННОМУ объекту IMBASE в иерархии справочника.

        Аналог :meth:`imbase_object_path`, но строит путь для объекта, связанного с
        указанным (например, для записи, на которую ссылается атрибут). Отдаёт цепочку
        узлов от корневого каталога до связанного объекта включительно.

        Когда применять: чтобы показать местоположение в дереве IMBASE для объекта,
        достижимого по связи, а не напрямую. Прямой путь по id объекта —
        :meth:`imbase_object_path`; путь по id ключа — :meth:`imbase_object_path_by_key`.
        Ответ обёрнут в ``...NullableResultDto`` и разворачивается здесь.

        Args:
            object_id: Идентификатор объекта IMBASE, для связанного объекта которого
                строится путь (id-пространство объектов IMBASE).

        Returns:
            Путь по схеме :class:`ImBaseObjectPath` либо ``None``, если связанный
            объект не найден (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                path = await ips.imbase_linked_object_path(123456)
                if path is not None:
                    print(path.object_id, path.path)

        Notes:
            operationId ``ImBase_GetPathToRelatedImBaseObject``; путь
            ``GET /core/api/imbase/linkedObject/{objectId}/path``.
            Ответ — ``ImBaseObjectPathDtoNullableResultDto``. См. [[ips-object-model]].
        """
        data = await self._request("get", f"/core/api/imbase/linkedObject/{object_id}/path")
        entity = data.get("entity") if isinstance(data, dict) else None
        return ImBaseObjectPath.model_validate(entity) if entity is not None else None
