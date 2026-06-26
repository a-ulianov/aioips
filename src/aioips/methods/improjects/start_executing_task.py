"""Метод запуска исполнения задачи проекта (Improject, мутация)."""

from typing import Any

from ...core import APIManager


class StartExecutingTaskMixin(APIManager):
    """Реализует ``POST /core/api/improjects/tasks/{taskId}/startExecuting``.

    ``operationId``: ``ImProject_StartExecutingTask``.
    """

    async def start_executing_task(
        self: "StartExecutingTaskMixin",
        task_id: int,
        *,
        is_need_to_log_modification_history: bool | None = None,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Запускает исполнение задачи проекта Improject (переводит в работу) (МУТАЦИЯ).

        Назначение: перевести задачу диаграммы Ганта в состояние исполнения
        (запустить связанный с ней процесс/работу). Применяйте на старте работ
        по задаче. Прогресс затем обновляют :meth:`change_task_progress`.

        Предусловие: задача ``task_id`` существует и готова к запуску по своему
        шагу ЖЦ; модуль Improject лицензирован.

        Обратимость: запуск исполнения — действие по шагу жизненного цикла;
        прямого «обратного» вызова нет. Отмена/откат зависят от настроенного
        процесса задачи (вне этого метода).

        Защита: меняет состояние на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            task_id: Числовой идентификатор задачи (``taskId`` в пути).
            is_need_to_log_modification_history: Логировать ли изменение
                (query ``isNeedToLogModificationHistory``). ``None`` — не передаётся.
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            Словарь карточки задачи ``TaskInfoDto`` (распакован из обёртки
            ``TaskInfoDtoProcessResultWithLogInfoDto`` по ключу ``result``).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                info = await ips.start_executing_task(7200, confirm=True)

        Notes:
            ``operationId``: ``ImProject_StartExecutingTask``; путь
            ``POST /core/api/improjects/tasks/{taskId}/startExecuting`` (query
            ``isNeedToLogModificationHistory``; тело ``{}`` против 415; ответ
            ``TaskInfoDtoProcessResultWithLogInfoDto``). Связанные методы:
            :meth:`change_task_progress`, :meth:`start_executing_project`.
        """
        if confirm is not True:
            raise ValueError(
                "start_executing_task запускает исполнение задачи; передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if is_need_to_log_modification_history is not None:
            params["isNeedToLogModificationHistory"] = str(
                is_need_to_log_modification_history
            ).lower()
        data = await self._request(
            "post",
            f"/core/api/improjects/tasks/{task_id}/startExecuting",
            params=params,
            json={},
        )
        if isinstance(data, dict):
            result: dict[str, Any] = data.get("result", data) or {}
            return result
        return {}
