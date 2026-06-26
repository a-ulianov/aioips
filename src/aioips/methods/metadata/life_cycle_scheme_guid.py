"""Метод получения GUID схемы жизненного цикла по идентификатору."""

from ...core import APIManager


class LifeCycleSchemeGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/lifeCycleSchemes/{id}/guid``."""

    async def life_cycle_scheme_guid(
        self: "LifeCycleSchemeGuidMixin",
        scheme_id: int,
    ) -> str:
        """Возвращает GUID схемы жизненного цикла по её числовому идентификатору.

        Мост «локальный id → переносимый GUID»: числовой ``id`` схемы ЖЦ различается
        между инсталляциями, а GUID стабилен между базами данных и удобен как
        переносимый ключ метаданных. Ответ сервера — голая строка GUID, без обёртки
        ``...NullableResultDto``.

        Когда применять: чтобы по локальному ``id`` схемы получить её GUID для хранения
        переносимых ссылок или последующих вызовов ``...ByGuid`` (например
        :meth:`life_cycle_scheme_by_guid`, :meth:`life_cycle_scheme_id_by_guid`).
        Обратное преобразование — :meth:`life_cycle_scheme_id_by_guid`.

        Args:
            scheme_id: Идентификатор схемы ЖЦ (id-пространство СХЕМ жизненного цикла,
                не ``ObjectTypeID`` и не идентификатор шага ЖЦ).

        Returns:
            GUID схемы ЖЦ строкой (например
            ``"cad001c5-306c-11d8-b4e9-00304f19f545"``); пустая строка, если сервер
            вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guid = await ips.life_cycle_scheme_guid(100)
                print(guid)

        Notes:
            operationId ``Metadata_GetLifeCycleSchemeGuid``; путь
            ``GET /core/api/metadata/lifeCycleSchemes/{id}/guid``.
            Обратное преобразование — :meth:`life_cycle_scheme_id_by_guid`.
        """
        path = f"/core/api/metadata/lifeCycleSchemes/{scheme_id}/guid"
        data = await self._request("get", path)
        return "" if data is None else str(data)
