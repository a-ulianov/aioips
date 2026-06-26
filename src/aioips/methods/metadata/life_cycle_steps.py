"""Метод получения списка всех шагов жизненного цикла метаданных."""

from ...core import APIManager
from ...schemas.metadata import LifeCycleStep


class LifeCycleStepsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/lifeCycleSteps``."""

    async def life_cycle_steps(self: "LifeCycleStepsMixin") -> list[LifeCycleStep]:
        """Возвращает полный список шагов (состояний) жизненного цикла из метаданных.

        Шаг жизненного цикла (ЖЦ) — это состояние, в котором может находиться объект, с
        режимом правки атрибутов (``object_modify_mode``: ``inBase``/``checkout``/
        ``createVersion``/``cantModify``) и типом контроля прав. Этот метод отдаёт
        ГЛОБАЛЬНЫЙ справочник всех шагов всех схем ЖЦ разом, а не шаги конкретного типа
        объекта. Ответ сервера — голый массив ``ImsLifeCycleStepDto`` (без обёртки
        ``...NullableResultDto``).

        Когда применять: чтобы построить общий словарь шагов (например, отображение
        ``id → name`` или ``id → object_modify_mode``) для интерпретации поля
        ``ObjectDto.lc_step`` у объектов любого типа. Для шагов ЖЦ конкретного типа
        объекта используйте :meth:`object_type_life_cycle_steps` (другой эндпоинт,
        фильтр по типу); для точечного запроса по одному шагу —
        :meth:`life_cycle_step` / :meth:`life_cycle_step_by_guid`.

        Returns:
            Список шагов ЖЦ по схеме :class:`LifeCycleStep`. Пустой список означает, что
            в базе не определено ни одного шага ЖЦ.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                steps = await ips.life_cycle_steps()
                by_id = {s.id: s.name for s in steps}

        Notes:
            operationId ``Metadata_GetLifeCycleStepList``; путь
            ``GET /core/api/metadata/lifeCycleSteps`` (массив ``ImsLifeCycleStepDto``).
            Связанные методы: :meth:`object_type_life_cycle_steps`,
            :meth:`life_cycle_step`. См. [[ips-object-model]] (раздел «Жизненный цикл»).
        """
        data = await self._request("get", "/core/api/metadata/lifeCycleSteps")
        return [LifeCycleStep.model_validate(item) for item in data]
