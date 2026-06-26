"""Метод проверки, является ли тип объекта корневым в PDM."""

from ...core import APIManager


class PdmObjectTypeIsRootMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/pdm/objectTypes/{id}/isRoot``."""

    async def pdm_object_type_is_root(
        self: "PdmObjectTypeIsRootMixin",
        object_type_id: int,
    ) -> bool:
        """Проверяет, является ли тип объекта корневым в PDM (по идентификатору).

        Возвращает ``True``, если тип объекта в контуре PDM (управление данными об изделии)
        является корневым — то есть его экземпляры могут выступать вершиной дерева изделия
        (корнем конфигурируемой структуры). Ответ сервера — голое булево значение, без
        обёртки ``...NullableResultDto``.

        Когда применять: при определении допустимых точек входа в структуру изделия PDM
        (с каких типов можно начинать обход/построение конфигурации). Связанные PDM-флаги
        типа: :meth:`pdm_object_type_is_configurable`, :meth:`pdm_object_type_is_contextable`.

        Args:
            object_type_id: Идентификатор ТИПА объекта (id-пространство ТИПОВ объектов
                метаданных, не id объекта/версии).

        Returns:
            ``True`` — тип корневой в PDM; ``False`` — нет (в том числе если сервер вернул
            ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.pdm_object_type_is_root(42):
                    ...

        Notes:
            operationId ``Metadata_IsPdmRootObjectType``; путь
            ``GET /core/api/metadata/pdm/objectTypes/{id}/isRoot`` (ответ — ``boolean``).
            Связанные методы: :meth:`pdm_object_type_is_configurable`,
            :meth:`pdm_object_type_is_contextable`.
        """
        path = f"/core/api/metadata/pdm/objectTypes/{object_type_id}/isRoot"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
