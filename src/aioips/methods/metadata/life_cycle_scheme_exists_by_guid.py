"""Метод проверки существования схемы жизненного цикла по GUID."""

from urllib.parse import quote

from ...core import APIManager


class LifeCycleSchemeExistsByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/lifeCycleSchemes/byGuid/{guid}/exists``."""

    async def life_cycle_scheme_exists_by_guid(
        self: "LifeCycleSchemeExistsByGuidMixin",
        guid: str,
    ) -> bool:
        """Проверяет, существует ли схема жизненного цикла с указанным GUID.

        Дешёвый булев аксессор по переносимому ключу метаданных: GUID схемы ЖЦ
        стабилен между базами данных, поэтому удобен, когда числовой ``id`` между
        инсталляциями различается. Ответ сервера — голое булево значение, без обёртки
        ``...NullableResultDto``.

        Когда применять: как предварительный фильтр перед
        :meth:`life_cycle_scheme_by_guid` для кода, работающего с несколькими
        инсталляциями IPS. Аналог по числовому id — :meth:`life_cycle_scheme_exists`.

        Args:
            guid: Глобальный идентификатор схемы ЖЦ (строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Кодируется в URL.

        Returns:
            ``True`` — схема ЖЦ с таким GUID существует; ``False`` — нет (в том числе
            если сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guid = "cad001c5-306c-11d8-b4e9-00304f19f545"
                if await ips.life_cycle_scheme_exists_by_guid(guid):
                    scheme = await ips.life_cycle_scheme_by_guid(guid)

        Notes:
            operationId ``Metadata_ExistsLifeCycleSchemeByGuid``; путь
            ``GET /core/api/metadata/lifeCycleSchemes/byGuid/{guid}/exists`` (ответ —
            ``boolean``). Связанные методы: :meth:`life_cycle_scheme_by_guid`,
            :meth:`life_cycle_scheme_exists`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/lifeCycleSchemes/byGuid/{encoded_guid}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
