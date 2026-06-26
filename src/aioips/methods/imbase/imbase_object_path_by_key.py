"""Метод получения пути к объекту справочной системы IMBASE по id ключа."""

from ...core import APIManager
from ...schemas.imbase import ImBaseObjectPath


class ImBaseObjectPathByKeyMixin(APIManager):
    """Реализует ``GET /core/api/imbase/object/byKey/{keyId}/path``."""

    async def imbase_object_path_by_key(
        self: "ImBaseObjectPathByKeyMixin",
        key_id: int,
    ) -> ImBaseObjectPath | None:
        """Возвращает путь к объекту IMBASE по идентификатору ключа.

        Аналог :meth:`imbase_object_path`, но объект адресуется по идентификатору
        КЛЮЧА (узла дерева/связи), а не по id объекта. Отдаёт цепочку узлов от
        корневого каталога до объекта включительно.

        Когда применять: когда на руках id ключа дерева IMBASE (например, полученный
        из ``objects_path`` другого пути), а не id объекта. Путь по id объекта —
        :meth:`imbase_object_path`. Ответ обёрнут в ``...NullableResultDto`` и
        разворачивается здесь.

        Args:
            key_id: Идентификатор ключа узла дерева IMBASE (id-пространство ключей
                IMBASE, не id объекта и не id версии).

        Returns:
            Путь по схеме :class:`ImBaseObjectPath` либо ``None``, если ключ не найден
            (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                path = await ips.imbase_object_path_by_key(987654)
                if path is not None:
                    print(path.record_id, path.path)

        Notes:
            operationId ``ImBase_GetPathToImBaseObjectByKey``; путь
            ``GET /core/api/imbase/object/byKey/{keyId}/path``.
            Ответ — ``ImBaseObjectPathDtoNullableResultDto``. См. [[ips-object-model]].
        """
        data = await self._request("get", f"/core/api/imbase/object/byKey/{key_id}/path")
        entity = data.get("entity") if isinstance(data, dict) else None
        return ImBaseObjectPath.model_validate(entity) if entity is not None else None
