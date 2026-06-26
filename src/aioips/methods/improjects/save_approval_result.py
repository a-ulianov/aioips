"""Метод сохранения результата согласования задачи (Improject, мутация)."""

from typing import Any

from ...core import APIManager


class SaveApprovalResultMixin(APIManager):
    """Реализует ``POST /core/api/improjects/tasks/{taskId}/saveApprovalResult``.

    ``operationId``: ``ImProject_SaveApprovalResult``.
    """

    async def save_approval_result(
        self: "SaveApprovalResultMixin",
        task_id: int,
        request: dict[str, Any],
        *,
        is_need_to_log_modification_history: bool | None = None,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Сохраняет результат согласования (резолюцию) задачи проекта Improject (МУТАЦИЯ).

        Назначение: зафиксировать решение руководителя по задаче, требующей
        согласования — утвердить или отклонить, с комментарием. Применяйте на
        шаге согласования диаграммы Ганта. Прочитать текущую резолюцию —
        :meth:`task` (поле ``manager_answer``).

        Предусловие: задача ``task_id`` существует и находится на шаге
        согласования; модуль Improject лицензирован. Тело ``request``
        соответствует DTO ``ApprovalResultDto`` (ключи ``camelCase``):
        ``isApproved`` (bool) — утверждено/отклонено, ``managerMessage`` —
        комментарий руководителя (опционально).

        Обратимость: ОБРАТИМА по смыслу — повторным :meth:`save_approval_result`
        с другим решением (если шаг ЖЦ это допускает).

        Защита: меняет данные на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            task_id: Числовой идентификатор задачи (``taskId`` в пути).
            request: Тело ``ApprovalResultDto`` (словарь, ключи ``camelCase``):
                ``isApproved``, ``managerMessage``.
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
                info = await ips.save_approval_result(
                    7200,
                    {"isApproved": True, "managerMessage": "Согласовано"},
                    confirm=True,
                )

        Notes:
            ``operationId``: ``ImProject_SaveApprovalResult``; путь
            ``POST /core/api/improjects/tasks/{taskId}/saveApprovalResult`` (query
            ``isNeedToLogModificationHistory``; тело ``ApprovalResultDto``; ответ
            ``TaskInfoDtoProcessResultWithLogInfoDto``). Связанный метод: :meth:`task`.
        """
        if confirm is not True:
            raise ValueError(
                "save_approval_result сохраняет резолюцию задачи; передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if is_need_to_log_modification_history is not None:
            params["isNeedToLogModificationHistory"] = str(
                is_need_to_log_modification_history
            ).lower()
        data = await self._request(
            "post",
            f"/core/api/improjects/tasks/{task_id}/saveApprovalResult",
            params=params,
            json=request,
        )
        if isinstance(data, dict):
            result: dict[str, Any] = data.get("result", data) or {}
            return result
        return {}
