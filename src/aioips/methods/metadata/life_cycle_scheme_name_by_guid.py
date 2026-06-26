"""Метод получения имени схемы жизненного цикла по GUID."""

from urllib.parse import quote

from ...core import APIManager


class LifeCycleSchemeNameByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/lifeCycleSchemes/byGuid/{guid}/name``."""

    async def life_cycle_scheme_name_by_guid(
        self: "LifeCycleSchemeNameByGuidMixin",
        guid: str,
    ) -> str:
        """Возвращает имя схемы жизненного цикла по её GUID.

        Мост «переносимый GUID → имя»: GUID схемы ЖЦ стабилен между базами данных,
        а имя удобно для логов/UI. Ответ сервера — голая строка, без обёртки
        ``...NullableResultDto``.

        Когда применять: тот же результат, что у :meth:`life_cycle_scheme_name`, но по
        переносимому GUID — для кода, работающего с несколькими инсталляциями IPS, где
        числовой ``id`` различается.

        Args:
            guid: Глобальный идентификатор схемы ЖЦ (строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Кодируется в URL.

        Returns:
            Имя схемы ЖЦ строкой; пустая строка, если сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                name = await ips.life_cycle_scheme_name_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(name)

        Notes:
            operationId ``Metadata_GetLifeCycleSchemeNameByGuid``; путь
            ``GET /core/api/metadata/lifeCycleSchemes/byGuid/{guid}/name``.
            Связанный метод по числовому id — :meth:`life_cycle_scheme_name`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/lifeCycleSchemes/byGuid/{encoded_guid}/name"
        data = await self._request("get", path)
        return "" if data is None else str(data)
