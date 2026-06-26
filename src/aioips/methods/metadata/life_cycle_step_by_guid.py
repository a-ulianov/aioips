"""Метод получения шага жизненного цикла по GUID."""

from uuid import UUID

from ...core import APIManager
from ...schemas.metadata import LifeCycleStep


class LifeCycleStepByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/lifeCycleSteps/byGuid/{guid}``."""

    async def life_cycle_step_by_guid(
        self: "LifeCycleStepByGuidMixin",
        guid: UUID | str,
    ) -> LifeCycleStep | None:
        """Возвращает описание шага жизненного цикла по его глобальному GUID.

        GUID шага жизненного цикла (ЖЦ) стабилен между базами данных, поэтому удобен как
        переносимый ключ метаданных. Шаг ЖЦ задаёт состояние объекта и режим правки его
        атрибутов (``object_modify_mode``). Ответ сервера обёрнут в ``...NullableResultDto``
        (``{entity, isEntityPresent}``); обёртка разворачивается здесь, наружу отдаётся
        либо схема, либо ``None``.

        Когда применять: тот же результат, что у :meth:`life_cycle_step`, но ключ —
        переносимый GUID (когда числовой ``id`` между базами различается). Список всех
        шагов даёт :meth:`life_cycle_steps`.

        Args:
            guid: Глобальный идентификатор шага ЖЦ (``UUID`` или строка вида
                ``"11111111-2222-3333-4444-555555555555"``). Подставляется в URL как есть.

        Returns:
            Шаг ЖЦ по схеме :class:`LifeCycleStep` либо ``None``, если шаг с таким GUID не
            найден (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                step = await ips.life_cycle_step_by_guid(
                    "11111111-2222-3333-4444-555555555555"
                )
                if step is not None:
                    print(step.id, step.name)

        Notes:
            operationId ``Metadata_GetLifeCycleStepByGuid``; путь
            ``GET /core/api/metadata/lifeCycleSteps/byGuid/{guid}``.
            Связанный метод по числовому id — :meth:`life_cycle_step`.
        """
        data = await self._request("get", f"/core/api/metadata/lifeCycleSteps/byGuid/{guid}")
        entity = data.get("entity") if isinstance(data, dict) else None
        return LifeCycleStep.model_validate(entity) if entity is not None else None
