"""Метод получения имени шага жизненного цикла по идентификатору."""

from ...core import APIManager


class LifeCycleStepNameMixin(APIManager):
    """Реализует ``GET /core/api/metadata/lifeCycleSteps/{id}/name``."""

    async def life_cycle_step_name(
        self: "LifeCycleStepNameMixin",
        life_cycle_step_id: int,
    ) -> str:
        """Возвращает название шага жизненного цикла по его идентификатору.

        Мост «id → имя»: переводит числовой ``id`` шага ЖЦ в человекочитаемое название
        состояния (например ``"В разработке"``) из метаданных — для логов, UI, отчётов.
        Ответ сервера — строка (имя), а не объект-обёртка.

        Когда применять: чтобы показать понятное название по уже известному ``id``
        (например, из :meth:`life_cycle_steps`, :meth:`object_type_life_cycle_steps` или
        поля ``ObjectDto.lc_step``), не загружая полное метаописание
        (:meth:`life_cycle_step`). Аналог по GUID — :meth:`life_cycle_step_name_by_guid`.

        Args:
            life_cycle_step_id: Идентификатор шага ЖЦ (id-пространство ШАГОВ жизненного
                цикла — глобальное, общее для всех схем; не ``ObjectTypeID`` и не
                ``ObjectID``/``ID``).

        Returns:
            Название шага ЖЦ как строка. Пустая строка, если сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера (в том числе если шаг с таким ``id``
                не найден).

        Example:
            async with IPSClient(config=config) as ips:
                name = await ips.life_cycle_step_name(10)

        Notes:
            operationId ``Metadata_GetLifeCycleStepNameById``; путь
            ``GET /core/api/metadata/lifeCycleSteps/{id}/name``. Связанные методы:
            :meth:`life_cycle_step_name_by_guid`, :meth:`life_cycle_step`.
        """
        path = f"/core/api/metadata/lifeCycleSteps/{life_cycle_step_id}/name"
        data = await self._request("get", path)
        return "" if data is None else str(data)
