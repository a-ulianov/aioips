"""Метод проверки частичной конфигурируемости типа связи в PDM."""

from ...core import APIManager


class PdmRelationTypeIsPartiallyConfigurableMixin(APIManager):
    """Реализует ``GET /core/api/metadata/pdm/relationTypes/{id}/isPartiallyConfigurable``."""

    async def pdm_relation_type_is_partially_configurable(
        self: "PdmRelationTypeIsPartiallyConfigurableMixin",
        relation_type_id: int,
    ) -> bool:
        """Проверяет, частично ли конфигурируем тип связи в PDM (по идентификатору).

        Возвращает ``True``, если тип связи в контуре PDM (управление данными об изделии)
        конфигурируем частично — то есть от конфигурации изделия зависят лишь некоторые
        свойства вхождения по этой связи, а не сам факт вхождения целиком. Ответ сервера —
        голое булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: при тонком анализе того, как конфигурация влияет на состав по
        связи (полностью либо частично). Полный аналог (связь конфигурируема целиком) —
        :meth:`pdm_relation_type_is_configurable`.

        Args:
            relation_type_id: Идентификатор ТИПА связи (id-пространство ТИПОВ связей
                метаданных, не RelationID конкретной связи).

        Returns:
            ``True`` — тип связи частично конфигурируем в PDM; ``False`` — нет (в том числе
            если сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.pdm_relation_type_is_partially_configurable(7):
                    ...

        Notes:
            operationId ``Metadata_IsPdmPartiallyConfigurableRelationType``; путь
            ``GET /core/api/metadata/pdm/relationTypes/{id}/isPartiallyConfigurable``
            (ответ — ``boolean``). Связанный метод:
            :meth:`pdm_relation_type_is_configurable`.
        """
        path = f"/core/api/metadata/pdm/relationTypes/{relation_type_id}/isPartiallyConfigurable"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
