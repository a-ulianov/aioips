"""Метод запуска исполнения проекта (Improject, мутация)."""

from typing import Any

from ...core import APIManager


class StartExecutingProjectMixin(APIManager):
    """Реализует ``POST /core/api/improjects/project/{projectId}/startExecuting``.

    ``operationId``: ``ImProject_StartExecutingProject``.
    """

    async def start_executing_project(
        self: "StartExecutingProjectMixin",
        project_id: int,
        *,
        is_need_to_log_modification_history: bool | None = None,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Запускает исполнение проекта Improject (переводит план-график в работу) (МУТАЦИЯ).

        Назначение: перевести проект целиком в состояние исполнения — стартовать
        выполнение план-графика. Применяйте, когда проект спланирован и готов к
        запуску. Остановить — :meth:`stop_executing_project`, завершить —
        :meth:`complete_project`. Запуск отдельной задачи —
        :meth:`start_executing_task`.

        Предусловие: проект ``project_id`` существует и готов к запуску по
        своему шагу ЖЦ; модуль Improject лицензирован.

        Обратимость: ОБРАТИМА — исполнение останавливается парным
        :meth:`stop_executing_project`.

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
                res = await ips.start_executing_project(1500, confirm=True)
                print(res.get("status"))

        Notes:
            ``operationId``: ``ImProject_StartExecutingProject``; путь
            ``POST /core/api/improjects/project/{projectId}/startExecuting`` (query
            ``isNeedToLogModificationHistory``; тело ``{}`` против 415; ответ
            ``TaskStatusResultProcessResultWithLogInfoDto``). Парный метод:
            :meth:`stop_executing_project`.
        """
        if confirm is not True:
            raise ValueError(
                "start_executing_project запускает исполнение проекта; передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if is_need_to_log_modification_history is not None:
            params["isNeedToLogModificationHistory"] = str(
                is_need_to_log_modification_history
            ).lower()
        data = await self._request(
            "post",
            f"/core/api/improjects/project/{project_id}/startExecuting",
            params=params,
            json={},
        )
        if isinstance(data, dict):
            result: dict[str, Any] = data.get("result", data) or {}
            return result
        return {}
