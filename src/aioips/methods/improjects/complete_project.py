"""Метод завершения проекта (Improject, мутация)."""

from typing import Any

from ...core import APIManager


class CompleteProjectMixin(APIManager):
    """Реализует ``POST /core/api/improjects/{projectId}/completeProject``.

    ``operationId``: ``ImProject_CompleteProject``.
    """

    async def complete_project(
        self: "CompleteProjectMixin",
        project_id: int,
        *,
        is_need_to_log_modification_history: bool | None = None,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Завершает проект Improject (переводит в финальное состояние) (МУТАЦИЯ).

        Назначение: закрыть проект — отметить план-график как завершённый.
        Применяйте по окончании всех работ. В отличие от
        :meth:`stop_executing_project` (пауза, обратима), завершение — финальный
        шаг жизненного цикла проекта.

        Предусловие: проект ``project_id`` существует и готов к завершению по
        своему шагу ЖЦ; модуль Improject лицензирован.

        Обратимость: завершение — финальный шаг ЖЦ; прямого «обратного» вызова
        в API НЕТ. Возврат проекта в работу зависит от настроенного процесса
        (вне этого метода).

        Защита: меняет состояние на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            project_id: Числовой идентификатор проекта (``projectId`` в пути).
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
                await ips.complete_project(1500, confirm=True)

        Notes:
            ``operationId``: ``ImProject_CompleteProject``; путь
            ``POST /core/api/improjects/{projectId}/completeProject`` (query
            ``isNeedToLogModificationHistory``; тело ``{}`` против 415; ответ
            ``TaskInfoDtoProcessResultWithLogInfoDto``). Связанные методы:
            :meth:`start_executing_project`, :meth:`stop_executing_project`.
        """
        if confirm is not True:
            raise ValueError(
                "complete_project завершает проект; передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if is_need_to_log_modification_history is not None:
            params["isNeedToLogModificationHistory"] = str(
                is_need_to_log_modification_history
            ).lower()
        data = await self._request(
            "post",
            f"/core/api/improjects/{project_id}/completeProject",
            params=params,
            json={},
        )
        if isinstance(data, dict):
            result: dict[str, Any] = data.get("result", data) or {}
            return result
        return {}
