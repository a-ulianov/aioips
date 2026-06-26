"""Метод получения имени шага жизненного цикла по GUID."""

from urllib.parse import quote

from ...core import APIManager


class LifeCycleStepNameByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/lifeCycleSteps/byGuid/{guid}/name``."""

    async def life_cycle_step_name_by_guid(
        self: "LifeCycleStepNameByGuidMixin",
        guid: str,
    ) -> str:
        """Возвращает название шага жизненного цикла по его GUID.

        Название шага ЖЦ — человекочитаемое имя состояния (например ``"В разработке"``).
        Ключ здесь — переносимый GUID, стабильный между базами данных. Ответ сервера —
        голая строка, без обёртки ``...NullableResultDto``.

        Когда применять: тот же результат, что у :meth:`life_cycle_step_name`, но по
        переносимому GUID — для кода, работающего с несколькими инсталляциями IPS, где
        числовой ``id`` различается.

        Args:
            guid: Глобальный идентификатор шага ЖЦ (строка вида
                ``"11111111-2222-3333-4444-555555555555"``). Кодируется в URL.

        Returns:
            Название шага ЖЦ строкой; пустая строка, если сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                name = await ips.life_cycle_step_name_by_guid(
                    "11111111-2222-3333-4444-555555555555"
                )
                print(name)  # "В разработке"

        Notes:
            operationId ``Metadata_GetLifeCycleStepNameByGuid``; путь
            ``GET /core/api/metadata/lifeCycleSteps/byGuid/{guid}/name``.
            Связанный метод по числовому id — :meth:`life_cycle_step_name`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/lifeCycleSteps/byGuid/{encoded_guid}/name"
        data = await self._request("get", path)
        return "" if data is None else str(data)
