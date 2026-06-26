"""Метод сохранения колонок грида проекта (Improject, мутация)."""

from typing import Any

from ...core import APIManager


class UpdateGridColumnsMixin(APIManager):
    """Реализует ``POST /core/api/improjects/update-grid-columns``.

    ``operationId``: ``ImProject_UpdateGridColumns``.
    """

    async def update_grid_columns(
        self: "UpdateGridColumnsMixin",
        request: dict[str, Any],
        *,
        confirm: bool = False,
    ) -> None:
        """Сохраняет состав и порядок колонок грида (таблицы) проектов Improject (МУТАЦИЯ).

        Назначение: записать настройку отображаемых колонок табличного
        представления проектов. Это настройка вида, не данные проекта. Парная
        операция чтения — :meth:`grid_columns`. Настройка общая (не привязана к
        конкретному проекту).

        Предусловие: модуль Improject лицензирован. Тело ``request``
        соответствует DTO ``UpdateGridColumnsDto`` (ключи ``camelCase``):
        ``columns`` — список колонок (``ColumnDto``: ``id``, ``width``).

        Обратимость: ОБРАТИМА по смыслу — повторным :meth:`update_grid_columns`
        с прежним составом колонок (предварительно прочитанным
        :meth:`grid_columns`).

        Защита: меняет настройку на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            request: Тело ``UpdateGridColumnsDto`` (словарь, ключи ``camelCase``):
                ``columns`` — список ``ColumnDto``.
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие
            ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.update_grid_columns(
                    {"columns": [{"id": "text", "width": 200}]},
                    confirm=True,
                )

        Notes:
            ``operationId``: ``ImProject_UpdateGridColumns``; путь
            ``POST /core/api/improjects/update-grid-columns`` (тело
            ``UpdateGridColumnsDto``, ответ void). Парный метод: :meth:`grid_columns`.
        """
        if confirm is not True:
            raise ValueError(
                "update_grid_columns меняет настройку колонок грида; передайте confirm=True",
            )
        await self._request("post", "/core/api/improjects/update-grid-columns", json=request)
        return None
