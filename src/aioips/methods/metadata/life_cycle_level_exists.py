"""Метод проверки существования уровня жизненного цикла по идентификатору."""

from ...core import APIManager


class LifeCycleLevelExistsMixin(APIManager):
    """Реализует ``GET /core/api/metadata/lifeCycleLevels/{id}/exists``."""

    async def life_cycle_level_exists(
        self: "LifeCycleLevelExistsMixin",
        life_cycle_level_id: int,
    ) -> bool:
        """Проверяет, существует ли уровень жизненного цикла с указанным идентификатором.

        Дешёвый булев аксессор поверх «пространства уровней ЖЦ»: подтверждает, что в
        метаданных есть уровень с данным ``LifeCycleLevelID``, не загружая его полное
        описание. Ответ сервера — голое булево значение, без обёртки
        ``...NullableResultDto``.

        Когда применять: как предварительный фильтр перед :meth:`life_cycle_level` или
        другими запросами по id уровня, чтобы не дёргать тяжёлые методы для заведомо
        отсутствующих идентификаторов. Аналог по GUID —
        :meth:`life_cycle_level_exists_by_guid`.

        Args:
            life_cycle_level_id: Идентификатор уровня ЖЦ (``LifeCycleLevelID`` —
                id-пространство УРОВНЕЙ ЖЦ, не шаг ЖЦ и не ``ObjectTypeID``).

        Returns:
            ``True`` — уровень ЖЦ с таким идентификатором существует; ``False`` — нет
            (в том числе если сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.life_cycle_level_exists(3):
                    level = await ips.life_cycle_level(3)

        Notes:
            operationId ``Metadata_ExistsLifeCycleLevelById``; путь
            ``GET /core/api/metadata/lifeCycleLevels/{id}/exists`` (ответ — ``boolean``).
            Связанные методы: :meth:`life_cycle_level`,
            :meth:`life_cycle_level_exists_by_guid`.
        """
        path = f"/core/api/metadata/lifeCycleLevels/{life_cycle_level_id}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
