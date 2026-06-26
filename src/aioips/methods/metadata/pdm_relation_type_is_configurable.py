"""Метод проверки конфигурируемости типа связи в PDM."""

from ...core import APIManager


class PdmRelationTypeIsConfigurableMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/pdm/relationTypes/{id}/isConfigurable``."""

    async def pdm_relation_type_is_configurable(
        self: "PdmRelationTypeIsConfigurableMixin",
        relation_type_id: int,
    ) -> bool:
        """Проверяет, является ли тип связи конфигурируемым в PDM (по идентификатору).

        Возвращает ``True``, если тип связи в контуре PDM (управление данными об изделии)
        полностью конфигурируем — то есть вхождение потомка по этой связи целиком зависит
        от выбранной конфигурации изделия. Ответ сервера — голое булево значение, без
        обёртки ``...NullableResultDto``.

        Когда применять: при анализе структуры изделия, чтобы понять, управляется ли состав
        по данной связи конфигурацией. Частичный аналог (связь конфигурируема лишь
        отчасти) — :meth:`pdm_relation_type_is_partially_configurable`.

        Args:
            relation_type_id: Идентификатор ТИПА связи (id-пространство ТИПОВ связей
                метаданных, не RelationID конкретной связи).

        Returns:
            ``True`` — тип связи конфигурируем в PDM; ``False`` — нет (в том числе если
            сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.pdm_relation_type_is_configurable(7):
                    ...

        Notes:
            operationId ``Metadata_IsPdmConfigurableRelationType``; путь
            ``GET /core/api/metadata/pdm/relationTypes/{id}/isConfigurable`` (ответ —
            ``boolean``). Связанный метод:
            :meth:`pdm_relation_type_is_partially_configurable`.
        """
        path = f"/core/api/metadata/pdm/relationTypes/{relation_type_id}/isConfigurable"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
