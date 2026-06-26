"""Метод проверки наличия записи IMBASE в кэше ограничительного перечня."""

from ...core import APIManager


class ImBaseRestrictiveApplicabilityCacheMixin(APIManager):
    """Реализует ``.../applicability/restrictiveCache`` (проверка кэша)."""

    async def imbase_restrictive_applicability_cache(
        self: "ImBaseRestrictiveApplicabilityCacheMixin",
        object_version_id: int,
    ) -> bool:
        """Проверяет наличие записи IMBASE в кэше ограничительного перечня.

        Сообщает, присутствует ли версия записи IMBASE в кэше ограничительного перечня
        применяемости. Дополняет :meth:`imbase_object_applicability`: используется,
        чтобы решить, показывать ли сообщение об ограничении (флаг
        ``position_in_restriction_list`` в результате проверки применяемости). Ответ —
        булево значение.

        Когда применять: вместе с проверкой применяемости при статусе ограниченного
        использования (``limitedUse``), чтобы избежать повторного предупреждения.
        ВНИМАНИЕ: принимает id ВЕРСИИ объекта, а не id объекта.

        Args:
            object_version_id: Идентификатор ВЕРСИИ объекта IMBASE (id-пространство
                версий, не id объекта).

        Returns:
            ``True``, если запись есть в кэше ограничительного перечня, иначе
            ``False``. Сервер не возвращает ``None``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                cached = await ips.imbase_restrictive_applicability_cache(7700123)
                print("в кэше:", cached)

        Notes:
            operationId ``ImBase_CheckRestrictiveApplicabilityCacheKey``; путь
            ``GET /core/api/imbase/object/{objectVersionId}/applicability/``
            ``restrictiveCache`` (возвращает ``bool``).
        """
        path = f"/core/api/imbase/object/{object_version_id}/applicability/restrictiveCache"
        data = await self._request("get", path)
        return bool(data)
