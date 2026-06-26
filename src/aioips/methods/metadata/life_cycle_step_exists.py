"""Метод проверки существования шага жизненного цикла по идентификатору."""

from ...core import APIManager


class LifeCycleStepExistsMixin(APIManager):
    """Реализует ``GET /core/api/metadata/lifeCycleSteps/{id}/exists``."""

    async def life_cycle_step_exists(
        self: "LifeCycleStepExistsMixin",
        life_cycle_step_id: int,
    ) -> bool:
        """Проверяет, существует ли шаг жизненного цикла с указанным идентификатором.

        Дешёвый булев аксессор поверх «пространства шагов жизненного цикла»: подтверждает,
        что в метаданных есть шаг ЖЦ с данным ``id``, не загружая его полное описание.
        Ответ сервера — голое булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: как предварительный фильтр перед :meth:`life_cycle_step` или
        другими запросами по id шага, чтобы не дёргать тяжёлые методы для заведомо
        отсутствующих идентификаторов. Аналог по GUID —
        :meth:`life_cycle_step_exists_by_guid`.

        Args:
            life_cycle_step_id: Идентификатор шага ЖЦ (id-пространство ШАГОВ жизненного
                цикла — глобальное, общее для всех схем; не ``ObjectTypeID`` и не
                ``ObjectID``/``ID``).

        Returns:
            ``True`` — шаг ЖЦ с таким идентификатором существует; ``False`` — нет (в том
            числе если сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.life_cycle_step_exists(10):
                    step = await ips.life_cycle_step(10)

        Notes:
            operationId ``Metadata_ExistsLifeCycleStepById``; путь
            ``GET /core/api/metadata/lifeCycleSteps/{id}/exists`` (ответ — ``boolean``).
            Связанные методы: :meth:`life_cycle_step`,
            :meth:`life_cycle_step_exists_by_guid`.
        """
        path = f"/core/api/metadata/lifeCycleSteps/{life_cycle_step_id}/exists"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
