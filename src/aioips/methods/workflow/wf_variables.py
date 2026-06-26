"""Метод получения переменных процесса для активности."""

from typing import Any

from ...core import APIManager
from ...schemas.workflow import Variable


class WFVariablesMixin(APIManager):
    """Реализует ``GET /core/api/wfVariables/{activityId}/loadVariables``.

    operationId ``WFVariables_LoadVariables``.
    """

    async def wf_variables(
        self: "WFVariablesMixin",
        activity_id: int,
        *,
        is_global_variable: bool | None = None,
    ) -> list[Variable]:
        """Возвращает переменные процесса, доступные на активности (задаче) workflow.

        Переменные процесса хранят данные, передаваемые между шагами маршрута
        (входные параметры, результаты, глобальные значения экземпляра). Метод
        перечисляет переменные с их именами, типами и идентификаторами; применяйте,
        чтобы прочитать состав переменных задачи перед их сохранением. Вложения той же
        активности даёт :meth:`wf_attachments`.

        Предусловие по id-пространству: ``activity_id`` — идентификатор АКТИВНОСТИ
        (задачи) экземпляра процесса, а не объекта или версии.

        Args:
            activity_id: Идентификатор активности (задачи) экземпляра процесса workflow.
            is_global_variable: Фильтр области видимости переменных. ``None`` (по
                умолчанию) — параметр не передаётся, сервер применяет своё значение по
                умолчанию (``False``). ``True`` — только глобальные переменные
                экземпляра процесса; ``False`` — только локальные переменные активности.

        Returns:
            Список переменных по схеме :class:`Variable` (поля ``variable_name``,
            ``variable_id``, ``variable_type``, ``short_name``). Пустой список означает,
            что у активности нет переменных под заданный фильтр.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                local_vars = await ips.wf_variables(48210)
                global_vars = await ips.wf_variables(48210, is_global_variable=True)
                for var in local_vars:
                    print(var.variable_name, var.variable_type)

        Notes:
            operationId ``WFVariables_LoadVariables``; путь
            ``GET /core/api/wfVariables/{activityId}/loadVariables`` (голый массив
            ``VariableDto``). Query ``isGlobalVariable`` отправляется только при заданном
            ``is_global_variable`` (значение сериализуется как ``true``/``false``).
        """
        params: dict[str, Any] | None = None
        if is_global_variable is not None:
            params = {"isGlobalVariable": str(is_global_variable).lower()}
        path = f"/core/api/wfVariables/{activity_id}/loadVariables"
        data = await self._request("get", path, params=params)
        return [Variable.model_validate(item) for item in data]
