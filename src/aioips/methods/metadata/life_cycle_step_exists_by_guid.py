"""Метод проверки существования шага жизненного цикла по GUID."""

from urllib.parse import quote

from ...core import APIManager


class LifeCycleStepExistsByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/lifeCycleSteps/byGuid/{guid}/exists``."""

    async def life_cycle_step_exists_by_guid(
        self: "LifeCycleStepExistsByGuidMixin",
        guid: str,
    ) -> bool:
        """Проверяет, существует ли шаг жизненного цикла с указанным GUID.

        Дешёвый булев аксессор по переносимому ключу метаданных: GUID шага ЖЦ стабилен
        между базами данных, поэтому удобен, когда числовой ``id`` между инсталляциями
        различается. Ответ сервера — голое булево значение, без обёртки
        ``...NullableResultDto``.

        Когда применять: как предварительный фильтр перед :meth:`life_cycle_step_by_guid`
        для кода, работающего с несколькими инсталляциями IPS. Аналог по числовому id —
        :meth:`life_cycle_step_exists`.

        Args:
            guid: Глобальный идентификатор шага ЖЦ (строка вида
                ``"11111111-2222-3333-4444-555555555555"``). Кодируется в URL.

        Returns:
            ``True`` — шаг ЖЦ с таким GUID существует; ``False`` — нет (в том числе если
            сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guid = "11111111-2222-3333-4444-555555555555"
                if await ips.life_cycle_step_exists_by_guid(guid):
                    step = await ips.life_cycle_step_by_guid(guid)

        Notes:
            operationId ``Metadata_ExistsLifeCycleStepByGuid``; путь
            ``GET /core/api/metadata/lifeCycleSteps/byGuid/{guid}/exists`` (ответ —
            ``boolean``). Связанные методы: :meth:`life_cycle_step_by_guid`,
            :meth:`life_cycle_step_exists`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/lifeCycleSteps/byGuid/{encoded_guid}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
