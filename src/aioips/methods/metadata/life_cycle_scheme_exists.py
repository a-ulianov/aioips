"""Метод проверки существования схемы жизненного цикла по идентификатору."""

from ...core import APIManager


class LifeCycleSchemeExistsMixin(APIManager):
    """Реализует ``GET /core/api/metadata/lifeCycleSchemes/{id}/exists``."""

    async def life_cycle_scheme_exists(
        self: "LifeCycleSchemeExistsMixin",
        scheme_id: int,
    ) -> bool:
        """Проверяет, существует ли схема жизненного цикла с указанным идентификатором.

        Дешёвый булев аксессор поверх «пространства схем ЖЦ»: подтверждает, что в
        метаданных есть схема с данным ``id``, не загружая её описание. Ответ сервера —
        голое булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: как предварительный фильтр перед :meth:`life_cycle_scheme` или
        :meth:`life_cycle_scheme_steps`, чтобы не дёргать тяжёлые методы для заведомо
        отсутствующих идентификаторов. Аналог по GUID —
        :meth:`life_cycle_scheme_exists_by_guid`.

        Args:
            scheme_id: Идентификатор схемы ЖЦ (id-пространство СХЕМ жизненного цикла,
                не ``ObjectTypeID`` и не идентификатор шага ЖЦ).

        Returns:
            ``True`` — схема ЖЦ с таким идентификатором существует; ``False`` — нет
            (в том числе если сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.life_cycle_scheme_exists(100):
                    scheme = await ips.life_cycle_scheme(100)

        Notes:
            operationId ``Metadata_ExistsLifeCycleSchemeById``; путь
            ``GET /core/api/metadata/lifeCycleSchemes/{id}/exists`` (ответ — ``boolean``).
            Связанные методы: :meth:`life_cycle_scheme`,
            :meth:`life_cycle_scheme_exists_by_guid`.
        """
        path = f"/core/api/metadata/lifeCycleSchemes/{scheme_id}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
