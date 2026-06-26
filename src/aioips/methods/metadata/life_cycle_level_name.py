"""Метод получения имени уровня жизненного цикла по идентификатору."""

from ...core import APIManager


class LifeCycleLevelNameMixin(APIManager):
    """Реализует ``GET /core/api/metadata/lifeCycleLevels/{id}/name``."""

    async def life_cycle_level_name(
        self: "LifeCycleLevelNameMixin",
        life_cycle_level_id: int,
    ) -> str:
        """Возвращает имя уровня жизненного цикла по его идентификатору.

        Мост «id → имя»: переводит числовой ``id`` уровня ЖЦ в человекочитаемое имя из
        метаданных (например «Утверждено») для логов, UI и отчётов. Ответ сервера —
        строка (имя), а не объект-обёртка.

        Когда применять: чтобы показать понятное имя по уже известному ``id`` (например,
        из :meth:`life_cycle_levels` или из ``LifeCycleStep.level_id``), не загружая
        полное метаописание (:meth:`life_cycle_level`). Аналог по GUID —
        :meth:`life_cycle_level_name_by_guid`.

        Args:
            life_cycle_level_id: Идентификатор уровня ЖЦ (``LifeCycleLevelID`` —
                id-пространство УРОВНЕЙ ЖЦ, не шаг ЖЦ и не ``ObjectTypeID``).

        Returns:
            Имя уровня ЖЦ как строка. Пустая строка, если сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера (в том числе если уровень с таким
                ``id`` не найден).

        Example:
            async with IPSClient(config=config) as ips:
                name = await ips.life_cycle_level_name(3)

        Notes:
            operationId ``Metadata_GetLifeCycleLevelNameById``; путь
            ``GET /core/api/metadata/lifeCycleLevels/{id}/name``. Связанные методы:
            :meth:`life_cycle_level_name_by_guid`, :meth:`life_cycle_level`.
        """
        path = f"/core/api/metadata/lifeCycleLevels/{life_cycle_level_id}/name"
        data = await self._request("get", path)
        return "" if data is None else str(data)
