"""Метод сохранения переменных процесса для активности."""

from ...core import APIManager
from ...schemas.workflow import Variable


class WFSaveVariablesMixin(APIManager):
    """Реализует ``POST /core/api/wfVariables/{activityId}/saveVariables``.

    operationId ``WFVariables_SaveVariables``.
    """

    async def wf_save_variables(
        self: "WFSaveVariablesMixin",
        activity_id: int,
        variables: list[Variable],
    ) -> bool:
        """Сохраняет (записывает) переменные процесса на активности (задаче) workflow.

        Переменные процесса хранят данные, передаваемые между шагами маршрута: входные
        параметры активности, результаты, глобальные значения экземпляра процесса. Этот
        метод записывает переданный набор переменных в активность — МУТИРУЮЩАЯ операция.
        Применяйте после редактирования значений, полученных через :meth:`wf_variables`
        (его и используйте, чтобы прочитать текущий состав переменных перед записью).
        Вложения той же активности изменяются методами :meth:`wf_add_attachments` /
        :meth:`wf_remove_attachments`.

        Предусловие по id-пространству: ``activity_id`` — идентификатор АКТИВНОСТИ
        (задачи) экземпляра процесса, а не идентификатор объекта или версии.

        Args:
            activity_id: Идентификатор активности (задачи) экземпляра процесса workflow.
            variables: Переменные для записи (:class:`Variable`), как их возвращает
                :meth:`wf_variables`. У каждой обязательны ``variable_name``,
                ``variable_id`` и ``variable_type``. Сериализуются в тело-массив запроса
                (голый JSON-массив ``VariableDto``).

        Returns:
            ``True``, если сервер подтвердил сохранение; ``False`` — если ответ пуст
            или отрицателен.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.workflow import Variable

            async with IPSClient(config=config) as ips:
                current = await ips.wf_variables(48210)  # 48210 = activityId
                await ips.wf_save_variables(
                    48210,
                    [Variable(
                        variable_name="Approved",
                        variable_id=7,
                        variable_type="boolean",
                    )],
                )

        Notes:
            operationId ``WFVariables_SaveVariables``; путь
            ``POST /core/api/wfVariables/{activityId}/saveVariables`` (тело — голый
            JSON-массив ``VariableDto``; ответ — булево). Связанный метод чтения —
            :meth:`wf_variables`.
        """
        body = [v.model_dump(mode="json", by_alias=True, exclude_none=True) for v in variables]
        path = f"/core/api/wfVariables/{activity_id}/saveVariables"
        data = await self._request("post", path, json=body)
        return bool(data) if data is not None else False
