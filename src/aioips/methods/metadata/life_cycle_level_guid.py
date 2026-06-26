"""Метод получения GUID уровня жизненного цикла по идентификатору."""

from ...core import APIManager


class LifeCycleLevelGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/lifeCycleLevels/{id}/guid``."""

    async def life_cycle_level_guid(
        self: "LifeCycleLevelGuidMixin",
        life_cycle_level_id: int,
    ) -> str:
        """Возвращает GUID уровня жизненного цикла по его числовому идентификатору.

        Мост «локальный id → переносимый GUID»: числовой ``LifeCycleLevelID`` различается
        между инсталляциями, а GUID уровня ЖЦ стабилен между базами данных и удобен как
        переносимый ключ метаданных. Ответ сервера — голая строка GUID, без обёртки
        ``...NullableResultDto``.

        Когда применять: чтобы по локальному ``id`` уровня получить его GUID для хранения
        переносимых ссылок или последующих вызовов ``...ByGuid`` (например
        :meth:`life_cycle_level_by_guid`, :meth:`life_cycle_level_id_by_guid`). Обратное
        преобразование — :meth:`life_cycle_level_id_by_guid`.

        Args:
            life_cycle_level_id: Идентификатор уровня ЖЦ (``LifeCycleLevelID`` —
                id-пространство УРОВНЕЙ ЖЦ, не шаг ЖЦ и не ``ObjectTypeID``).

        Returns:
            GUID уровня ЖЦ строкой (например
            ``"cad001c5-306c-11d8-b4e9-00304f19f545"``); пустая строка, если сервер
            вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guid = await ips.life_cycle_level_guid(3)
                print(guid)

        Notes:
            operationId ``Metadata_GetLifeCycleLevelGuid``; путь
            ``GET /core/api/metadata/lifeCycleLevels/{id}/guid``.
            Обратное преобразование — :meth:`life_cycle_level_id_by_guid`.
        """
        path = f"/core/api/metadata/lifeCycleLevels/{life_cycle_level_id}/guid"
        data = await self._request("get", path)
        return "" if data is None else str(data)
