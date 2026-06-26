"""Метод проверки контекстируемости типа объекта в PDM."""

from ...core import APIManager


class PdmObjectTypeIsContextableMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/pdm/objectTypes/{id}/isContextable``."""

    async def pdm_object_type_is_contextable(
        self: "PdmObjectTypeIsContextableMixin",
        object_type_id: int,
    ) -> bool:
        """Проверяет, является ли тип объекта контекстируемым в PDM (по идентификатору).

        Возвращает ``True``, если тип объекта в контуре PDM (управление данными об изделии)
        помечен как контекстируемый — то есть его экземпляры могут разрешаться в контексте
        конкретной конфигурации изделия. Ответ сервера — голое булево значение, без обёртки
        ``...NullableResultDto``.

        Когда применять: при анализе того, зависит ли представление экземпляров типа от
        выбранного контекста конфигурации в PDM. Связанные PDM-флаги типа:
        :meth:`pdm_object_type_is_configurable`, :meth:`pdm_object_type_is_root`.

        Args:
            object_type_id: Идентификатор ТИПА объекта (id-пространство ТИПОВ объектов
                метаданных, не id объекта/версии).

        Returns:
            ``True`` — тип контекстируем в PDM; ``False`` — нет (в том числе если сервер
            вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.pdm_object_type_is_contextable(42):
                    ...

        Notes:
            operationId ``Metadata_IsPdmContextableObjectType``; путь
            ``GET /core/api/metadata/pdm/objectTypes/{id}/isContextable`` (ответ —
            ``boolean``). Связанные методы: :meth:`pdm_object_type_is_configurable`,
            :meth:`pdm_object_type_is_root`.
        """
        path = f"/core/api/metadata/pdm/objectTypes/{object_type_id}/isContextable"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
