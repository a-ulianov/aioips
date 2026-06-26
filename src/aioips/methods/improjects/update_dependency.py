"""Метод обновления зависимости между задачами проекта (Improject, мутация)."""

from typing import Any

from ...core import APIManager


class UpdateDependencyMixin(APIManager):
    """Реализует ``PUT /core/api/improjects/dependency/{dependencyId}``.

    ``operationId``: ``ImProject_UpdateDependency``.
    """

    async def update_dependency(
        self: "UpdateDependencyMixin",
        dependency_id: int,
        request: dict[str, Any],
        *,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Обновляет существующую зависимость между задачами проекта Improject (МУТАЦИЯ).

        Назначение: изменить параметры связи между задачами на диаграмме Ганта
        (источник, приёмник, тип, задержку). Применяйте для редактирования
        связи, созданной :meth:`create_dependency`.

        Предусловие: зависимость ``dependency_id`` существует; модуль Improject
        лицензирован. Тело ``request`` соответствует DTO ``DependencyDto`` (ключи
        ``camelCase``): ``source``, ``target``, ``type``, ``lag``.

        Обратимость: ОБРАТИМА по смыслу — повторным :meth:`update_dependency` с
        прежними значениями полей.

        Защита: меняет данные на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            dependency_id: Числовой идентификатор зависимости (``dependencyId``
                в пути). Пространство id зависимостей отдельно от задач/проектов.
            request: Тело ``DependencyDto`` (словарь, ключи ``camelCase``).
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            Словарь результата ``GanttOperationResult``. Значимый ключ
            ``action`` — описание выполненной операции Ганта (``GanttAction``).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.update_dependency(
                    10,
                    {"source": 1, "target": 3, "type": "0", "lag": 1},
                    confirm=True,
                )

        Notes:
            ``operationId``: ``ImProject_UpdateDependency``; путь
            ``PUT /core/api/improjects/dependency/{dependencyId}`` (тело
            ``DependencyDto``, ответ ``GanttOperationResult``). Связанные методы:
            :meth:`create_dependency`, :meth:`delete_dependency`.
        """
        if confirm is not True:
            raise ValueError(
                "update_dependency изменяет связь между задачами; передайте confirm=True",
            )
        data = await self._request(
            "put", f"/core/api/improjects/dependency/{dependency_id}", json=request
        )
        result: dict[str, Any] = data if isinstance(data, dict) else {}
        return result
