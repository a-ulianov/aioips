"""Метод получения шага жизненного цикла по идентификатору."""

from ...core import APIManager
from ...schemas.metadata import LifeCycleStep


class LifeCycleStepMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/lifeCycleSteps/{id}``."""

    async def life_cycle_step(
        self: "LifeCycleStepMixin",
        life_cycle_step_id: int,
    ) -> LifeCycleStep | None:
        """Возвращает описание шага (состояния) жизненного цикла по его идентификатору.

        Шаг жизненного цикла (ЖЦ) задаёт состояние объекта и режим правки его атрибутов
        на этом шаге (``object_modify_mode``: ``inBase``/``checkout``/``createVersion``/
        ``cantModify``). Ответ сервера обёрнут в ``...NullableResultDto``
        (``{entity, isEntityPresent}``); обёртка разворачивается здесь, наружу отдаётся
        либо схема, либо ``None``.

        Когда применять: чтобы по известному ``id`` шага получить его полное метаописание
        (имя, схема ЖЦ, режим правки). ``id`` берётся из :meth:`life_cycle_steps`,
        :meth:`object_type_life_cycle_steps` или из поля ``ObjectDto.lc_step``. Аналог по
        GUID — :meth:`life_cycle_step_by_guid`.

        Args:
            life_cycle_step_id: Идентификатор шага ЖЦ (id-пространство ШАГОВ жизненного
                цикла — глобальное, общее для всех схем; не ``ObjectTypeID`` и не
                ``ObjectID``/``ID`` объекта или его версии).

        Returns:
            Шаг ЖЦ по схеме :class:`LifeCycleStep` либо ``None``, если шаг с таким
            идентификатором не найден (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                step = await ips.life_cycle_step(10)
                if step is not None:
                    print(step.name, step.object_modify_mode)

        Notes:
            operationId ``Metadata_GetLifeCycleStepById``; путь
            ``GET /core/api/metadata/lifeCycleSteps/{id}``.
            Связанные методы: :meth:`life_cycle_steps`, :meth:`life_cycle_step_by_guid`,
            :meth:`object_type_life_cycle_steps`.
        """
        path = f"/core/api/metadata/lifeCycleSteps/{life_cycle_step_id}"
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        return LifeCycleStep.model_validate(entity) if entity is not None else None
