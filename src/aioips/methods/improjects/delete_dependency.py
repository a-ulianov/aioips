"""Метод удаления зависимости между задачами проекта (Improject, мутация)."""

from typing import Any

from ...core import APIManager


class DeleteDependencyMixin(APIManager):
    """Реализует ``DELETE /core/api/improjects/dependency/{dependencyId}``.

    ``operationId``: ``ImProject_DeleteDependency``.
    """

    async def delete_dependency(
        self: "DeleteDependencyMixin",
        dependency_id: int,
        *,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Удаляет зависимость между задачами проекта Improject (МУТАЦИЯ).

        Назначение: разорвать связь между двумя задачами на диаграмме Ганта.
        Парная операция к :meth:`create_dependency`. Идентификатор зависимости
        берут из результата :meth:`create_dependency` (``tid``) или из связей
        проекта :meth:`project` (поле ``links``).

        Предусловие: зависимость ``dependency_id`` существует; модуль Improject
        лицензирован.

        Обратимость: ОБРАТИМА — связь воссоздаётся :meth:`create_dependency` с
        теми же ``source``/``target`` (новый идентификатор зависимости).

        Защита: удаляет данные на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            dependency_id: Числовой идентификатор удаляемой зависимости
                (``dependencyId`` в пути).
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            Словарь результата ``GanttOperationResult``. Значимый ключ
            ``action`` — описание выполненной операции Ганта (``GanttAction``).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.delete_dependency(10, confirm=True)

        Notes:
            ``operationId``: ``ImProject_DeleteDependency``; путь
            ``DELETE /core/api/improjects/dependency/{dependencyId}`` (ответ
            ``GanttOperationResult``). Парный метод: :meth:`create_dependency`.
        """
        if confirm is not True:
            raise ValueError(
                "delete_dependency удаляет связь между задачами; передайте confirm=True",
            )
        data = await self._request("delete", f"/core/api/improjects/dependency/{dependency_id}")
        result: dict[str, Any] = data if isinstance(data, dict) else {}
        return result
