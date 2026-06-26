"""Метод создания зависимости между задачами проекта (Improject, мутация)."""

from typing import Any

from ...core import APIManager


class CreateDependencyMixin(APIManager):
    """Реализует ``POST /core/api/improjects/{projectId}/dependency``.

    ``operationId``: ``ImProject_CreateDependency``.
    """

    async def create_dependency(
        self: "CreateDependencyMixin",
        project_id: int,
        request: dict[str, Any],
        *,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Создаёт зависимость (связь) между задачами проекта Improject (МУТАЦИЯ).

        Назначение: связать две задачи проекта отношением предшествования на
        диаграмме Ганта (например «финиш-старт»). Применяйте после
        :meth:`create_task`, когда задачи уже заведены, чтобы выстроить
        логику план-графика.

        Предусловие: проект ``project_id`` и обе связываемые задачи существуют;
        модуль Improject лицензирован. Тело ``request`` соответствует DTO
        ``DependencyDto`` (ключи ``camelCase``): ``source`` — id задачи-источника,
        ``target`` — id задачи-приёмника, ``type`` — тип связи, ``lag`` —
        задержка (опционально).

        Обратимость: ОБРАТИМА — связь удаляется парным :meth:`delete_dependency`
        по идентификатору зависимости.

        Защита: создаёт связь на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            project_id: Числовой идентификатор проекта (``projectId`` в пути).
            request: Тело ``DependencyDto`` (словарь, ключи ``camelCase``):
                ``source``, ``target``, ``type``, ``lag``.
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            Словарь результата ``CreateTaskResult``. Значимые ключи: ``tid`` —
            идентификатор созданной зависимости (для :meth:`delete_dependency`),
            ``action`` — описание операции Ганта (``GanttAction``).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                res = await ips.create_dependency(
                    1500,
                    {"source": 1, "target": 2, "type": "0"},
                    confirm=True,
                )
                dependency_id = res["tid"]

        Notes:
            ``operationId``: ``ImProject_CreateDependency``; путь
            ``POST /core/api/improjects/{projectId}/dependency`` (тело
            ``DependencyDto``, ответ ``CreateTaskResult``). Связанные методы:
            :meth:`delete_dependency`, :meth:`update_dependency`.
        """
        if confirm is not True:
            raise ValueError(
                "create_dependency создаёт связь между задачами; передайте confirm=True",
            )
        data = await self._request(
            "post", f"/core/api/improjects/{project_id}/dependency", json=request
        )
        result: dict[str, Any] = data if isinstance(data, dict) else {}
        return result
