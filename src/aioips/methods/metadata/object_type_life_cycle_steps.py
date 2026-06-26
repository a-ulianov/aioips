"""Метод получения шагов жизненного цикла типа объекта."""

from ...core import APIManager
from ...schemas.metadata import LifeCycleStep


class ObjectTypeLifeCycleStepsMixin(APIManager):
    """Реализует ``GET /core/api/metadata/objectTypes/{objectTypeId}/lifeCycleSteps``."""

    async def object_type_life_cycle_steps(
        self: "ObjectTypeLifeCycleStepsMixin",
        object_type_id: int,
    ) -> list[LifeCycleStep] | None:
        """Возвращает список шагов жизненного цикла для типа объекта.

        Шаги ЖЦ задают для типа объекта набор состояний и режим правки атрибутов на
        каждом из них (``object_modify_mode``). Ответ сервера обёрнут в
        ``...ListNullableResultDto`` (``{entity, isEntityPresent}``, где ``entity`` —
        массив или ``null``); обёртка разворачивается здесь, наружу отдаётся либо
        список схем, либо ``None``.

        Когда применять: чтобы понять, в каком режиме (``inBase``/``checkout``/
        ``createVersion``/``cantModify``) разрешено редактирование на конкретном шаге
        ЖЦ, прежде чем выполнять запись атрибутов (S3/S4-методы). Текущий шаг объекта —
        в ``ObjectDto.lc_step``; сопоставляйте его с ``LifeCycleStep.id`` из результата.
        ``object_type_id`` берётся из :meth:`object_types` или
        :meth:`object_type_id_by_name`.

        Args:
            object_type_id: Идентификатор типа объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID`` объекта/версии).

        Returns:
            Список :class:`LifeCycleStep` либо ``None``, если для типа нет схемы ЖЦ
            (``isEntityPresent == false`` / ``entity == null``). Пустой список —
            схема ЖЦ есть, но без шагов.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                steps = await ips.object_type_life_cycle_steps(1742)
                if steps is not None:
                    for step in steps:
                        print(step.name, step.object_modify_mode)

        Notes:
            operationId ``Metadata_GetObjectTypeLifeCycleStepList``; путь
            ``GET /core/api/metadata/objectTypes/{objectTypeId}/lifeCycleSteps``
            (массив ``ImsLifeCycleStepDto`` в обёртке). См. объектной модели IPS
            (раздел «Жизненный цикл»).
        """
        path = f"/core/api/metadata/objectTypes/{object_type_id}/lifeCycleSteps"
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        if entity is None:
            return None
        return [LifeCycleStep.model_validate(item) for item in entity]
