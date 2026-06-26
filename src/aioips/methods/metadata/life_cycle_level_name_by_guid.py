"""Метод получения имени уровня жизненного цикла по GUID."""

from urllib.parse import quote

from ...core import APIManager


class LifeCycleLevelNameByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/lifeCycleLevels/byGuid/{guid}/name``."""

    async def life_cycle_level_name_by_guid(
        self: "LifeCycleLevelNameByGuidMixin",
        guid: str,
    ) -> str:
        """Возвращает имя уровня жизненного цикла по его GUID.

        Мост «переносимый GUID → имя»: GUID уровня ЖЦ стабилен между базами данных,
        поэтому удобен, когда числовой ``id`` между инсталляциями различается. Ответ
        сервера — голая строка (имя), без обёртки ``...NullableResultDto``.

        Когда применять: тот же результат, что у :meth:`life_cycle_level_name`, но по
        переносимому GUID — для кода, работающего с несколькими инсталляциями IPS.

        Args:
            guid: Глобальный идентификатор уровня ЖЦ (строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Кодируется в URL.

        Returns:
            Имя уровня ЖЦ строкой; пустая строка, если сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                name = await ips.life_cycle_level_name_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(name)

        Notes:
            operationId ``Metadata_GetLifeCycleLevelNameByGuid``; путь
            ``GET /core/api/metadata/lifeCycleLevels/byGuid/{guid}/name``.
            Связанный метод по числовому id — :meth:`life_cycle_level_name`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/lifeCycleLevels/byGuid/{encoded_guid}/name"
        data = await self._request("get", path)
        return "" if data is None else str(data)
