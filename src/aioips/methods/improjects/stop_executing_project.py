"""Метод остановки исполнения проекта (Improject, мутация)."""

from typing import Any

from ...core import APIManager


class StopExecutingProjectMixin(APIManager):
    """Реализует ``POST /core/api/improjects/project/{projectId}stopExecuting``.

    ``operationId``: ``ImProject_StopExecutingProject``. ВНИМАНИЕ: в swagger путь
    задан без разделяющего слеша перед ``stopExecuting`` — используется точно.
    """

    async def stop_executing_project(
        self: "StopExecutingProjectMixin",
        project_id: int,
        *,
        is_need_to_log_modification_history: bool | None = None,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Останавливает исполнение проекта Improject (приостанавливает работы) (МУТАЦИЯ).

        Назначение: вывести проект из состояния исполнения — приостановить
        выполнение план-графика. Парная операция к
        :meth:`start_executing_project`. Применяйте для паузы/отмены запуска.
        Завершить проект совсем — :meth:`complete_project`.

        Предусловие: проект ``project_id`` существует и находится в исполнении;
        модуль Improject лицензирован.

        Обратимость: ОБРАТИМА — исполнение снова запускается парным
        :meth:`start_executing_project`.

        Защита: меняет состояние на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            project_id: Числовой идентификатор проекта (``projectId`` в пути).
            is_need_to_log_modification_history: Логировать ли изменение
                (query ``isNeedToLogModificationHistory``). ``None`` — не передаётся.
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            Словарь результата статуса ``TaskStatusResult`` (распакован из обёртки
            ``TaskStatusResultProcessResultWithLogInfoDto`` по ключу ``result``).
            Значимый ключ ``status`` — текущий статус (``TaskStatus``).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                res = await ips.stop_executing_project(1500, confirm=True)

        Notes:
            ``operationId``: ``ImProject_StopExecutingProject``; путь
            ``POST /core/api/improjects/project/{projectId}stopExecuting`` (БЕЗ
            слеша перед ``stopExecuting`` — особенность swagger; query
            ``isNeedToLogModificationHistory``; тело ``{}`` против 415; ответ
            ``TaskStatusResultProcessResultWithLogInfoDto``). Парный метод:
            :meth:`start_executing_project`.
        """
        if confirm is not True:
            raise ValueError(
                "stop_executing_project останавливает исполнение проекта; передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if is_need_to_log_modification_history is not None:
            params["isNeedToLogModificationHistory"] = str(
                is_need_to_log_modification_history
            ).lower()
        data = await self._request(
            "post",
            f"/core/api/improjects/project/{project_id}stopExecuting",
            params=params,
            json={},
        )
        if isinstance(data, dict):
            result: dict[str, Any] = data.get("result", data) or {}
            return result
        return {}
