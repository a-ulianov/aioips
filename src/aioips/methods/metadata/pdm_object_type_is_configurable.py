"""Метод проверки конфигурируемости типа объекта в PDM."""

from ...core import APIManager


class PdmObjectTypeIsConfigurableMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/pdm/objectTypes/{id}/isConfigurable``."""

    async def pdm_object_type_is_configurable(
        self: "PdmObjectTypeIsConfigurableMixin",
        object_type_id: int,
    ) -> bool:
        """Проверяет, является ли тип объекта конфигурируемым в PDM (по идентификатору).

        Возвращает ``True``, если тип объекта в контуре PDM (управление данными об изделии)
        помечен как конфигурируемый — то есть его экземпляры могут участвовать в
        конфигурациях изделия. Ответ сервера — голое булево значение, без обёртки
        ``...NullableResultDto``.

        Когда применять: при анализе конфигурируемости изделия в PDM, чтобы понять, можно
        ли строить конфигурации на базе данного типа. Связанные PDM-флаги типа:
        :meth:`pdm_object_type_is_contextable`, :meth:`pdm_object_type_is_root`.

        Args:
            object_type_id: Идентификатор ТИПА объекта (id-пространство ТИПОВ объектов
                метаданных, не id объекта/версии).

        Returns:
            ``True`` — тип конфигурируем в PDM; ``False`` — нет (в том числе если сервер
            вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.pdm_object_type_is_configurable(42):
                    ...

        Notes:
            operationId ``Metadata_IsPdmConfigurableObjectType``; путь
            ``GET /core/api/metadata/pdm/objectTypes/{id}/isConfigurable`` (ответ —
            ``boolean``). Связанные методы: :meth:`pdm_object_type_is_contextable`,
            :meth:`pdm_object_type_is_root`.
        """
        path = f"/core/api/metadata/pdm/objectTypes/{object_type_id}/isConfigurable"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
