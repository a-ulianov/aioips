"""Метод проверки применяемости записи IMBASE."""

from ...core import APIManager
from ...schemas.imbase import ImBaseApplicabilityCheckResult


class ImBaseObjectApplicabilityMixin(APIManager):
    """Реализует ``GET /core/api/imbase/object/{objectVersionId}/applicability``."""

    async def imbase_object_applicability(
        self: "ImBaseObjectApplicabilityMixin",
        object_version_id: int,
    ) -> ImBaseApplicabilityCheckResult | None:
        """Проверяет применяемость (ограничительный перечень) записи IMBASE.

        «Применяемость» определяет, разрешено ли использовать запись справочника
        (материал, стандартное изделие и т.п.) при формировании состава изделия.
        Метод возвращает статус применяемости и вспомогательный флаг для логики показа
        предупреждения.

        Когда применять: перед добавлением записи IMBASE в состав, чтобы убедиться, что
        использование не запрещено/ограничено. ВНИМАНИЕ: принимает id ВЕРСИИ объекта
        (``ID``/F_ID), а не id объекта (``ObjectID``). Кэш ограничительного перечня
        проверяется методом :meth:`imbase_restrictive_applicability_cache`. Ответ
        обёрнут в ``...NullableResultDto`` и разворачивается здесь.

        Args:
            object_version_id: Идентификатор ВЕРСИИ объекта IMBASE (id-пространство
                версий, не id объекта).

        Returns:
            Результат по схеме :class:`ImBaseApplicabilityCheckResult` либо ``None``,
            если запись не найдена/проверка неприменима (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                result = await ips.imbase_object_applicability(7700123)
                if result is not None:
                    print(result.applicability_status)

        Notes:
            operationId ``ImBase_CheckObjectApplicability``; путь
            ``GET /core/api/imbase/object/{objectVersionId}/applicability``.
            Ответ — ``ImBaseApplicabilityCheckResultDtoNullableResultDto``.
            См. [[ips-object-model]].
        """
        data = await self._request(
            "get", f"/core/api/imbase/object/{object_version_id}/applicability"
        )
        entity = data.get("entity") if isinstance(data, dict) else None
        if entity is None:
            return None
        return ImBaseApplicabilityCheckResult.model_validate(entity)
