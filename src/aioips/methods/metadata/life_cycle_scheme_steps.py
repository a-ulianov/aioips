"""Метод получения шагов схемы жизненного цикла."""

from ...core import APIManager
from ...schemas.metadata import LifeCycleStep


class LifeCycleSchemeStepsMixin(APIManager):
    """Реализует ``GET /core/api/metadata/lifeCycleSchemes/{schemeId}/steps``."""

    async def life_cycle_scheme_steps(
        self: "LifeCycleSchemeStepsMixin",
        scheme_id: int,
    ) -> list[LifeCycleStep]:
        """Возвращает список шагов указанной схемы жизненного цикла.

        Шаги ЖЦ задают для схемы набор состояний и режим правки атрибутов на каждом из
        них (``object_modify_mode``). В отличие от :meth:`object_type_life_cycle_steps`
        (шаги в контексте конкретного типа объекта), здесь шаги запрашиваются прямо по
        идентификатору самой схемы. Ответ сервера — голый массив ``ImsLifeCycleStepDto``,
        без обёртки ``...NullableResultDto``.

        Когда применять: чтобы понять, в каком режиме (``inBase``/``checkout``/
        ``createVersion``/``cantModify``) разрешено редактирование на конкретном шаге
        схемы, прежде чем выполнять запись атрибутов (S3/S4-методы). ``scheme_id``
        берётся из :meth:`life_cycle_schemes` или :meth:`life_cycle_scheme_id_by_guid`.

        Args:
            scheme_id: Идентификатор схемы ЖЦ (id-пространство СХЕМ жизненного цикла,
                не ``ObjectTypeID`` и не идентификатор отдельного шага ЖЦ).

        Returns:
            Список :class:`LifeCycleStep`. Пустой список означает, что у схемы нет шагов
            (либо схема с таким ``id`` не найдена — сервер отдаёт пустой массив).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                steps = await ips.life_cycle_scheme_steps(100)
                for step in steps:
                    print(step.name, step.object_modify_mode)

        Notes:
            operationId ``Metadata_GetLifeCycleSchemeStepList``; путь
            ``GET /core/api/metadata/lifeCycleSchemes/{schemeId}/steps`` (массив
            ``ImsLifeCycleStepDto``). См. объектной модели IPS (раздел «Жизненный цикл»).
            Связанный метод по типу объекта — :meth:`object_type_life_cycle_steps`.
        """
        path = f"/core/api/metadata/lifeCycleSchemes/{scheme_id}/steps"
        data = await self._request("get", path)
        return [LifeCycleStep.model_validate(item) for item in data]
